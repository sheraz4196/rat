"""CI helper: create a fresh environment, install a built wheel and smoke it."""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
import venv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('wheel', type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='rat-wheel-') as directory:
        root = Path(directory) / 'venv'
        venv.EnvBuilder(with_pip=True).create(root)
        bindir = root / ('Scripts' if sys.platform == 'win32' else 'bin')
        python = bindir / ('python.exe' if sys.platform == 'win32' else 'python')
        rat = bindir / ('rat.exe' if sys.platform == 'win32' else 'rat')
        subprocess.run([str(python), '-m', 'pip', 'install', str(args.wheel.resolve())], check=True)
        subprocess.run([sys.executable, str(Path(__file__).with_name('smoke_installed.py')), '--python', str(python), '--rat', str(rat)], check=True)


if __name__ == '__main__':
    main()
