"""
CachyOS repository support.

linux-cachyos is only published in the CachyOS repositories, which are signed with a
key the Arch keyring does not know about. pacstrap verifies packages against a keyring
it creates inside the target, so the CachyOS kernel cannot be strapped together with
the rest of the system. Instead the repository is added to the target after pacstrap,
its key is trusted from inside the chroot, and the kernel is installed from there.
"""

import re
from pathlib import Path
from typing import Final

from archinstall.lib.models.package_types import Kernel

CACHYOS_KEY_ID: Final = 'F3B607488DB35A47'
CACHYOS_KEYSERVER: Final = 'keyserver.ubuntu.com'
CACHYOS_KEYRING_PACKAGE: Final = 'cachyos-keyring'
CACHYOS_MIRRORLIST: Final = Path('/etc/pacman.d/cachyos-mirrorlist')
CACHYOS_SERVER: Final = 'https://mirror.cachyos.org/repo/$arch/$repo'

CACHYOS_KERNELS: Final[frozenset[str]] = frozenset({Kernel.LINUX_CACHYOS.value})


def is_cachyos_kernel(kernel: str) -> bool:
	return kernel in CACHYOS_KERNELS


def cachyos_mirrorlist() -> str:
	return f'# Managed by archinstall\nServer = {CACHYOS_SERVER}\n'


def insert_cachyos_repo(pacman_conf: str) -> str:
	"""
	Adds the [cachyos] repository above [core] so its packages take precedence
	over the Arch ones. Returns the config unchanged if the repository is already there.
	"""
	if re.search(r'^\[cachyos\]', pacman_conf, re.MULTILINE):
		return pacman_conf

	block = f'[cachyos]\nInclude = {CACHYOS_MIRRORLIST}\n\n'

	match = re.search(r'^\[core\]', pacman_conf, re.MULTILINE)
	if match:
		return pacman_conf[: match.start()] + block + pacman_conf[match.start() :]

	return pacman_conf + '\n' + block
