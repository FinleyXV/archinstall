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

from pathlib import Path
from typing import Final

from archinstall.lib.models.package_types import Kernel

CACHYOS_REPO_TARBALL: Final = 'https://mirror.cachyos.org/cachyos-repo.tar.xz'
CACHYOS_SCRIPT_NAME: Final = 'cachyos-repo.sh'

CACHYOS_KERNELS: Final[frozenset[str]] = frozenset({Kernel.LINUX_CACHYOS.value})


def is_cachyos_kernel(kernel: str) -> bool:
	return kernel in CACHYOS_KERNELS


def find_cachyos_script(extracted: Path) -> Path | None:
	"""
	Returns the path of cachyos-repo.sh inside an extracted tarball, or None if it isn't there.
	"""
	return next(extracted.rglob(CACHYOS_SCRIPT_NAME), None)


def cachyos_script_shell(script_in_chroot: str) -> str:
	"""
	The shell snippet run inside the chroot (wrap it in `bash -c`). The script must run from
	its own directory because it reads its awk helpers relative to the working directory. It ends
	with a `pacman -Syu`, which asks for confirmation, so `yes` answers the prompts.
	"""
	script_dir = script_in_chroot.rsplit('/', 1)[0]
	return f'cd {script_dir} && yes | bash {script_in_chroot} --install'
