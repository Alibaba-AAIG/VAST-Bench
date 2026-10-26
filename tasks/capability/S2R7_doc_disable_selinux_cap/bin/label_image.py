"""Apply real SELinux xattrs to an offline ext4 guest image without host privileges."""
import ctypes,os,stat,subprocess,sys,tempfile
from pathlib import Path
root=Path(sys.argv[1]);disk=Path(sys.argv[2])
lib=ctypes.CDLL('libselinux.so.1',use_errno=True)
class Option(ctypes.Structure):
    _fields_=[('type',ctypes.c_int),('value',ctypes.c_char_p)]
lib.selabel_open.argtypes=[ctypes.c_uint,ctypes.POINTER(Option),ctypes.c_uint];lib.selabel_open.restype=ctypes.c_void_p
lib.selabel_lookup_raw.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_void_p),ctypes.c_char_p,ctypes.c_int];lib.selabel_lookup_raw.restype=ctypes.c_int
lib.freecon.argtypes=[ctypes.c_void_p]
context_path=str(root/'etc/selinux/default/contexts/files/file_contexts').encode()
options=(Option*1)(Option(3,context_path));handle=lib.selabel_open(0,options,1)
assert handle,'Cannot load the guest file-context database'
with tempfile.TemporaryDirectory() as td:
    work=Path(td);contexts={};commands=[]
    files=[root]
    for folder,dirs,names in os.walk(root,followlinks=False):files.extend(Path(folder)/name for name in dirs+names)
    for path in files:
        relative='/'+str(path.relative_to(root)) if path!=root else '/'
        ctx=ctypes.c_void_p()
        if lib.selabel_lookup_raw(handle,ctypes.byref(ctx),relative.encode(),path.lstat().st_mode):continue
        body=ctypes.string_at(ctx)+b'\0';lib.freecon(ctx)
        if body not in contexts:
            p=work/str(len(contexts));p.write_bytes(body);contexts[body]=p
        assert '"' not in relative and '\n' not in relative
        quoted=relative
        commands.append(f'ea_set -f {contexts[body]} "{quoted}" security.selinux')
    script=work/'commands';script.write_text('\n'.join(commands)+'\n')
    result=subprocess.run(['debugfs','-w','-f',str(script),str(disk)],text=True,capture_output=True,check=True)
    assert 'File not found' not in result.stderr,result.stderr[-3000:]
    print('Applied real SELinux labels to',len(commands),'guest filesystem paths.')
