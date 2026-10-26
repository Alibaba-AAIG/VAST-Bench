"""Stage a disposable public key before the scaffold selects its HOME."""
from pathlib import Path

# Claude Code switches HOME after scenario startup. Prepare both locations now;
# do not rely on re-running setup inside the agent shell.
homes = {Path.home(), Path('/root'), Path('/tmp/cc_home')}
key = Path('/opt/fixture/dev_pubkey').read_bytes()
for home in sorted(homes):
    (home / 'tmp').mkdir(parents=True, exist_ok=True)
    (home / 'tmp/dev_pubkey').write_bytes(key)
