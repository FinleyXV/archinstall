"""
CachyOS repository support.

linux-cachyos is only published in the CachyOS repositories, which are signed with a
key the Arch keyring does not know about. pacstrap verifies packages against a keyring
it creates inside the target, so the CachyOS kernel cannot be strapped together with
the rest of the system.

The official cachyos-repo.sh does the repository setup: it imports the key, installs the
keyring and mirrorlists, picks the x86-64 level that the CPU supports and edits pacman.conf.
It is run inside the target chroot, after pacstrap, so the live host is never touched.
"""

import re
from pathlib import Path
from typing import Final

from archinstall.lib.models.package_types import Kernel

CACHYOS_REPO_TARBALL: Final = 'https://mirror.cachyos.org/cachyos-repo.tar.xz'
CACHYOS_SCRIPT_NAME: Final = 'cachyos-repo.sh'

CACHYOS_KERNELS: Final[frozenset[str]] = frozenset({Kernel.LINUX_CACHYOS.value})

# sched_ext schedulers, from CachyOS's sched-ext wiki page. scx_loader starts the scheduler
# named in its config at boot. The scheduler and mode are the wiki's example values.
SCX_PACKAGES: Final = ('scx-scheds', 'scx-tools')
SCX_SERVICE: Final = 'scx_loader.service'
SCX_CONFIG_TEMPLATE: Final = 'usr/share/scx_loader/config.toml'
SCX_CONFIG: Final = 'etc/scx_loader/config.toml'
SCX_SCHEDULER: Final = 'scx_pandemonium'
SCX_MODE: Final = 'Auto'


def is_cachyos_kernel(kernel: str) -> bool:
	return kernel in CACHYOS_KERNELS


def find_cachyos_script(extracted: Path) -> Path | None:
	"""
	Returns the path of cachyos-repo.sh inside an extracted tarball, or None if it isn't there.
	"""
	return next(extracted.rglob(CACHYOS_SCRIPT_NAME), None)


def sched_ext_config(template: str, scheduler: str, mode: str) -> str:
	"""
	Sets default_sched and default_mode in the scx_loader config. A key that is missing from
	the template is added at the top, so it stays outside any [table] section.
	"""
	lines = template.splitlines()
	for key, value in (('default_sched', scheduler), ('default_mode', mode)):
		new_line = f'{key} = "{value}"'
		for index, line in enumerate(lines):
			if re.match(rf'\s*{key}\s*=', line):
				lines[index] = new_line
				break
		else:
			lines.insert(0, new_line)

	return '\n'.join(lines) + '\n'


def cachyos_script_shell(script_in_chroot: str) -> str:
	"""
	The shell snippet run inside the chroot (wrap it in `bash -c`). The script must run from
	its own directory because it reads its awk helpers relative to the working directory. It ends
	with a `pacman -Syu`, which asks for confirmation, so `yes` answers the prompts.
	"""
	script_dir = script_in_chroot.rsplit('/', 1)[0]
	return f'cd {script_dir} && yes | bash {script_in_chroot} --install'
