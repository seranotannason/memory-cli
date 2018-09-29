# -*- coding: utf-8 -*-

import urwid
import sys
from ui import PALETTE, EmptyCardWidget, CardWidget, SpacerWidget
from game import Game
from time import sleep

class GameApp(object):
    def __init__(self):
        self.game = Game()
        self.current_selection = None
        self._rows = [
            urwid.Columns([EmptyCardWidget() for _ in range(13)]) for _ in range(4)
        ]
        self._update_rows()

        self.main_layout = urwid.Pile([
            self._rows[0],
            urwid.Divider(),
            self._rows[1],
            urwid.Divider(),
            self._rows[2],
            urwid.Divider(),
            self._rows[3],
        ])

    def _update_rows(self): 
        for i, card in enumerate(self.game.cards):
            row = i/13
            col = i%13
            self._rows[row].contents[col] = (
                CardWidget(card, row, col, onclick=self._card_clicked),
                self._rows[row].options()
            )

    def iter_allcards(self):
        """Iterate through all card widgets in the game"""
        for row in self._rows:
            for card_widget in row.contents:
                yield card_widget


    def _card_clicked(self, card_widget):
        # Show first card
        if self.current_selection is None:
            card_widget.face_up = True
            self.current_selection = card_widget
            return

        # Card has been selected, deselecting is not an option
        if self.current_selection == card_widget:
            return

        # 2 cards have been selected. Check if they have the same rank
        card_widget.face_up = True
          
        if self.current_selection.card.rank == card_widget.card.rank:    
            # Player has guessed both cards correctly
            # Remove these two cards from view
            row_1 = self.current_selection.row_index
            col_1 = self.current_selection.col_index
            row_2 = card_widget.row_index
            col_2 = card_widget.col_index  
            self._rows[row_1].contents[col_1] = (
                SpacerWidget(),
                self._rows[row_1].options()
            )
            self._rows[row_2].contents[col_2] = (
                SpacerWidget(),
                self._rows[row_2].options()
            )
            
        else:
            self.current_selection.face_up = False
            card_widget.face_up = False
            self.current_selection = None


def exit_game(key):
    if key in ('q', 'Q', 'esc'):
        raise urwid.ExitMainLoop()


def main():
    reload(sys)
    sys.setdefaultencoding('utf8')
    app = GameApp()
    loop = urwid.MainLoop(
        urwid.Filler(app.main_layout, valign='top'),
        PALETTE,
        unhandled_input=exit_game,
    )
    loop.run()


if __name__ == "__main__":
    main()