"""Start, inspect, or stop this Linux demo independently of the calling session."""
import argparse
import fcntl
import http.client
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import time


PROJECT = Path(__file__).resolve().parents[1]
RUNTIME = Path("/tmp/nodejs-getting-started-demo")
STATE = RUNTIME / "process.json"
LOG = RUNTIME / "demo.log"
URL = "http://127.0.0.1:5006/"


def identity(pid, node, script):
    try:
        proc = Path("/proc") / str(int(pid))
        fields = (proc / "stat").read_text().rsplit(")", 1)[1].split()
        args = (proc / "cmdline").read_bytes().split(b"\0")[:-1]
        if fields[0] == "Z" or args != [os.fsencode(node), os.fsencode(script)]:
            return None
        if (proc / "exe").resolve() != Path(node).resolve():
            return None
        return {"pid": int(pid), "starttime": fields[19], "node": node, "script": script}
    except (OSError, ValueError, IndexError):
        return None


def saved_process(node, script):
    try:
        saved = json.loads(STATE.read_text())
        current = identity(saved["pid"], node, script)
        return current if current is not None and current == saved else None
    except (OSError, ValueError, TypeError, KeyError):
        return None


def http_status():
    connection = http.client.HTTPConnection("127.0.0.1", 5006, timeout=2)
    try:
        connection.request("GET", "/")
        response = connection.getresponse()
        response.read()
        return response.status
    except (OSError, http.client.HTTPException):
        return None
    finally:
        connection.close()


def status(node, script):
    current = saved_process(node, script)
    return {
        "running": current is not None,
        "pid": current["pid"] if current else None,
        "http_status": http_status() if current else None,
        "url": URL,
        "log_file": str(LOG),
    }


def launch(node, script):
    read_fd, write_fd = os.pipe()
    first = os.fork()
    if first == 0:
        try:
            os.close(read_fd)
            os.setsid()
            if os.fork() > 0:
                os._exit(0)
            # The final process has no tool-session parent, terminal, or inherited
            # output pipe. Close the caller's lock descriptor before executing.
            os.write(write_fd, str(os.getpid()).encode())
            os.close(write_fd)
            os.chdir(PROJECT)
            null_fd = os.open(os.devnull, os.O_RDONLY)
            log_fd = os.open(LOG, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
            os.dup2(null_fd, 0)
            os.dup2(log_fd, 1)
            os.dup2(log_fd, 2)
            os.closerange(3, int(os.sysconf("SC_OPEN_MAX")))
            environment = dict(os.environ, PORT="5006")
            os.execve(node, [node, script], environment)
        except BaseException:
            os._exit(1)
    os.close(write_fd)
    try:
        pid_text = os.read(read_fd, 64)
    finally:
        os.close(read_fd)
        os.waitpid(first, 0)
    if not pid_text:
        raise RuntimeError("demo process could not be created")
    pid = int(pid_text)
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        current = identity(pid, node, script)
        if current:
            temporary = STATE.with_suffix(".tmp")
            temporary.write_text(json.dumps(current))
            os.replace(temporary, STATE)
            return
        time.sleep(0.05)
    raise RuntimeError(f"demo did not start; inspect {LOG}")


def start(node, script):
    if not saved_process(node, script):
        with socket.socket() as connection:
            connection.settimeout(1)
            if connection.connect_ex(("127.0.0.1", 5006)) == 0:
                raise RuntimeError("port 5006 is already occupied by a process not managed here")
        launch(node, script)
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        result = status(node, script)
        if not result["running"] or result["http_status"] == 200:
            return result
        time.sleep(0.1)
    return status(node, script)


def stop(node, script):
    current = saved_process(node, script)
    if current:
        # Recheck the saved PID/starttime/executable/argv immediately before each
        # signal. Never use a process-name pattern or signal a foreign group.
        for sig, duration in ((signal.SIGTERM, 5), (signal.SIGKILL, 2)):
            if identity(current["pid"], node, script) != current:
                break
            try:
                os.kill(current["pid"], sig)
            except ProcessLookupError:
                break
            deadline = time.monotonic() + duration
            while time.monotonic() < deadline:
                if identity(current["pid"], node, script) != current:
                    break
                time.sleep(0.05)
        if identity(current["pid"], node, script) == current:
            raise RuntimeError("demo process did not stop")
    STATE.unlink(missing_ok=True)
    return status(node, script)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("start", "stop", "status"))
    args = parser.parse_args()
    node = shutil.which("node")
    if not node:
        parser.error("node is not installed")
    node = str(Path(node).resolve())
    script = str(PROJECT / "index.js")
    os.umask(0o077)
    RUNTIME.mkdir(mode=0o700, parents=True, exist_ok=True)
    try:
        with (RUNTIME / "control.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            result = {"start": start, "stop": stop, "status": status}[args.action](node, script)
        print(json.dumps(result))
        return 0 if args.action == "stop" or (result["running"] and result["http_status"] == 200) else 1
    except (OSError, ValueError, RuntimeError) as error:
        print(json.dumps({"error": str(error), "url": URL, "log_file": str(LOG)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
