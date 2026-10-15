from archinstall.lib.cachyos import insert_cachyos_repo, is_cachyos_kernel
from archinstall.lib.installer import __base_packages__, __packages__
from archinstall.lib.models.package_types import Kernel

PACMAN_CONF = '[options]\nColor\n\n[core]\nInclude = /etc/pacman.d/mirrorlist\n\n[extra]\nInclude = /etc/pacman.d/mirrorlist\n'


def test_cachyos_repo_goes_above_core() -> None:
	out = insert_cachyos_repo(PACMAN_CONF)
	assert out.index('[cachyos]') < out.index('[core]')


def test_cachyos_repo_is_not_added_twice() -> None:
	once = insert_cachyos_repo(PACMAN_CONF)
	assert insert_cachyos_repo(once) == once


def test_cachyos_repo_appended_when_no_core_section() -> None:
	assert '[cachyos]' in insert_cachyos_repo('[options]\nColor\n')


def test_cachyos_kernel_detection() -> None:
	assert is_cachyos_kernel('linux-cachyos')
	assert not is_cachyos_kernel('linux')
	assert Kernel.LINUX_CACHYOS in Kernel


def test_coreutils_and_sudo_are_swapped() -> None:
	assert 'coreutils' not in __base_packages__
	assert 'base' not in __base_packages__
	assert 'uutils-coreutils' in __base_packages__
	assert 'sudo' not in __base_packages__
	assert 'sudo-rs' in __base_packages__


def test_ntpd_rs_and_fish_are_in_base() -> None:
	assert 'ntpd-rs' in __base_packages__
	assert 'fish' in __base_packages__
	assert 'bash' in __base_packages__  # still needed for /bin/sh


def test_kernel_list_includes_all_kernels() -> None:
	for kernel in Kernel:
		assert kernel.value in __packages__
