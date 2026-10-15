from pathlib import Path

from archinstall.lib.cachyos import cachyos_script_shell, find_cachyos_script, is_cachyos_kernel
from archinstall.lib.installer import __base_packages__, __packages__
from archinstall.lib.models.package_types import Kernel


def test_cachyos_kernel_detection() -> None:
	assert is_cachyos_kernel('linux-cachyos')
	assert not is_cachyos_kernel('linux')
	assert Kernel.LINUX_CACHYOS in Kernel


def test_find_cachyos_script_in_nested_tarball(tmp_path: Path) -> None:
	script = tmp_path / 'cachyos-repo' / 'cachyos-repo.sh'
	script.parent.mkdir()
	script.write_text('#!/bin/bash\n')

	assert find_cachyos_script(tmp_path) == script


def test_find_cachyos_script_missing(tmp_path: Path) -> None:
	assert find_cachyos_script(tmp_path) is None


def test_cachyos_script_runs_from_its_own_directory() -> None:
	shell = cachyos_script_shell('/var/tmp/cachyos-repo/cachyos-repo/cachyos-repo.sh')
	assert shell.startswith('cd /var/tmp/cachyos-repo/cachyos-repo && ')
	assert 'bash /var/tmp/cachyos-repo/cachyos-repo/cachyos-repo.sh --install' in shell
	assert 'yes |' in shell


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
