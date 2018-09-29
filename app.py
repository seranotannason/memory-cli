import urwid
from .ui import PALETTE


def exit_game(key):
	if key in ('q', 'Q', 'esc'):
		raise urwid.ExitMainLoop()
		

def main():
	app = GameApp()
	loop = urwid.MainLoop(
		urwid.Filler(app.main_layout, valign='top'),
		PALETTE,
		unhandled_input=exit_game,
	)
	loop.run()


if __name__ == "__main__":
	main()