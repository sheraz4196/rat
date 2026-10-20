"""Read-only integration health; shell detection is an environment inference."""
import os
import shutil
import sys
from pathlib import Path
from rat import __version__
from rat.core.shell import detect_shell, profile_path
from rat.integrations.manager import read_profile, START, block


def integration_health(shell=None, profile=None):
    shell = shell or detect_shell()
    supported = shell in ('bash', 'zsh', 'powershell')
    report = {'shell': shell, 'supported': supported, 'profile': None, 'status': 'unsupported', 'native_wrappers': False, 'prompt_preserved': False, 'guidance': None}
    if not supported:
        report['guidance'] = 'Use namespaced rat commands; automatic Fish/cmd integration is unavailable.'
        return report
    try:
        path = Path(profile) if profile else profile_path(shell)
        report['profile'] = str(path)
        text = read_profile(path)
        installed = START in text
        report['status'] = 'installed' if installed else 'not installed'
        report['native_wrappers'] = installed and '# rat: native-wrappers=enabled' in text
        report['prompt_preserved'] = installed and '# rat: prompt=preserved' in text
        if not installed:
            report['guidance'] = f'Preview rat install --shell {shell} --profile "{path}" --dry-run.'
        elif 'unalias git ls tree cat' in text or '$global:RatNativeGit' in text:
            report['status'] = 'legacy integration'
            report['guidance'] = 'Rerun rat install without --enhance-commands and reopen the shell to preserve native commands.'
        elif block(shell, report['native_wrappers'], report['prompt_preserved']).strip() not in text:
            report['status'] = 'modified integration'
            report['guidance'] = 'Inspect the marked block and preview rat install before updating it.'
    except (OSError, ValueError) as exc:
        report['status'] = 'invalid' if report['profile'] else 'profile required'
        report['guidance'] = str(exc)
    return report


def installation_info():
    prefix = str(Path(sys.prefix))
    method = 'pipx' if 'pipx' in Path(prefix).parts else 'isolated installer' if Path(prefix).parts[-2:] == ('rat', 'venv') else 'unknown (source or Python environment)'
    return {'version': __version__, 'executable': shutil.which('rat'), 'python': sys.executable, 'package_path': str(Path(__file__).resolve().parents[1]), 'prefix': prefix, 'method': method}


def gnome_prerequisites():
    active = bool(os.environ.get('GNOME_TERMINAL_SERVICE'))
    return {'session': active, 'gsettings': bool(shutil.which('gsettings')), 'dconf': bool(shutil.which('dconf'))}
