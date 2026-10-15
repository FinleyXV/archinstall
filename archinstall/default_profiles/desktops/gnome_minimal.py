from typing import override

from archinstall.default_profiles.profile import DisplayServerType, GreeterType, Profile, ProfileType


class GnomeMinimalProfile(Profile):
	"""
	GNOME with only the shell, the keyring, the login manager and the settings app.
	No GNOME applications, no GNOME Tweaks.
	"""

	def __init__(self) -> None:
		super().__init__(
			'GNOME (minimal)',
			ProfileType.DesktopEnv,
			support_gfx_driver=True,
			display_server=DisplayServerType.Wayland,
		)

	@property
	@override
	def packages(self) -> list[str]:
		return [
			'gnome-shell',
			'gnome-keyring',
			'gdm',
			'gnome-control-center',
		]

	@property
	@override
	def default_greeter_type(self) -> GreeterType:
		return GreeterType.Gdm
