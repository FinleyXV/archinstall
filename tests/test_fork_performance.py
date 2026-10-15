from archinstall.lib.cachyos import SCX_MODE, SCX_SCHEDULER, sched_ext_config
from archinstall.lib.models.package_types import DEFAULT_KERNEL, Kernel
from archinstall.lib.models.pacman import DEFAULT_PARALLEL_DOWNLOADS

SCX_TEMPLATE = '[general]\n# default_sched = "scx_rusty"\nlog_level = "info"\n\n[advanced]\nstarts = 1\n'


def test_default_kernel_is_cachyos() -> None:
	assert DEFAULT_KERNEL == Kernel.LINUX_CACHYOS


def test_parallel_downloads_default() -> None:
	assert DEFAULT_PARALLEL_DOWNLOADS == 10


def test_sched_ext_sets_existing_keys_in_place() -> None:
	template = 'default_sched = "old"\ndefault_mode = "PowerSave"\nlog_level = "info"\n'
	out = sched_ext_config(template, 'scx_pandemonium', 'Auto')

	assert 'default_sched = "scx_pandemonium"' in out.splitlines()
	assert 'default_mode = "Auto"' in out.splitlines()
	assert out.count('default_sched') == 1
	assert 'log_level = "info"' in out


def test_sched_ext_adds_missing_keys_at_top_outside_tables() -> None:
	out = sched_ext_config(SCX_TEMPLATE, SCX_SCHEDULER, SCX_MODE)
	lines = out.splitlines()

	assert lines[0] == 'default_mode = "Auto"'
	assert lines[1] == 'default_sched = "scx_pandemonium"'
	assert lines.index('[general]') > lines.index('default_sched = "scx_pandemonium"')


def test_sched_ext_ignores_commented_keys() -> None:
	out = sched_ext_config(SCX_TEMPLATE, SCX_SCHEDULER, SCX_MODE)
	assert '# default_sched = "scx_rusty"' in out
	assert out.count('default_sched') == 2  # the comment and the added line
