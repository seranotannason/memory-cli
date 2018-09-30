# -*- coding: utf-8 -*-

import urwid

PALETTE = [
    ('red', 'dark red', ''),
    ('selectedred', 'dark red', 'yellow'),
    ('selected', '', 'yellow'),
]

# Modify these as needed
SIZES = {'small': (4, 3), 'medium': (6, 4), 'large': (8, 6)}
card_size = 'large'


class BaseCardWidget(urwid.WidgetWrap):
    def __init__(self, *args, **kw):
        self.card_columns, self.card_rows = SIZES[card_size]
        super(BaseCardWidget, self).__init__(*args, **kw)
        self.redraw()

    def redraw(self):
        self.text.set_text(self._draw_card_text())

    def _draw_card_text(self):
        raise NotImplementedError


class SpacerWidget(BaseCardWidget):
    def __init__(self, **kw):
        self.text = urwid.Text('', wrap='clip')
        super(SpacerWidget, self).__init__(self.text)

    def _draw_card_text(self):
        # The decrement of rows is to account for expanding space in
        # the vertical direction
        return [u' '* self.card_columns +'\n'] * (self.card_rows-1)


class EmptyCardWidget(BaseCardWidget):
    def __init__(self, onclick=None, **kw):
        self.onclick = onclick
        self.text = urwid.Text('', wrap='clip')

        super(EmptyCardWidget, self).__init__(self.text)

    def _draw_card_text(self):
        return [
                u'╭' + '─' * (self.card_columns-2) + '╮\n' 
                + (self.card_rows-2) * (u'│'+ ' ' * (self.card_columns-2) + '│\n')
                + u'╰' + '─' * (self.card_columns-2) + '╯\n'
            ]

    def selectable(self):
        return bool(self.onclick)

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press':
            if self.onclick:
                self.onclick(self)

    def iter_widgets(self):
        return iter([])


class CardWidget(BaseCardWidget):
    def __init__(self, card, row_index, col_index, onclick=None):
        self._card = card
        self.row_index = row_index
        self.col_index = col_index
        self.text = urwid.Text('', wrap='clip')
        self.highlighted = False
        self.onclick = onclick
        super(CardWidget, self).__init__(self.text)

    def __repr__(self):
        return '{}(card={!r}, highlighted={!r}, ...)'.format(
            self.__class__.__name__, self.card, self.highlighted,
        )

    def mouse_event(self, size, event, button, col, row, focus):
        if event == 'mouse press':
            if self.onclick:
                self.onclick(self)

    def _draw_card_text(self):
        columns, rows = self.card_columns, self.card_rows

        style = 'selected' if self.highlighted else ''
        redornot = 'red' if self.card.suit in ('hearts', 'diamonds') else ''
        if self.highlighted:
            redornot = 'selected' + redornot
        if not self.face_up:
            face_down_middle_filling = (columns-2) * u'╬'
            filling = [u'│', (style, face_down_middle_filling), u'│\n'] * (rows-2)
        else:
            rank, suit = (self.card.rank, self.card.suit_symbol)
            spaces = (columns-5) * ' '
            filling = [u'│', (redornot, u'{}{}{}'.format(rank.ljust(2), spaces, suit)), u'│\n']
            filling += (
                [u'│', (style, u' ' * (columns-2)), u'│\n'] * (rows-4) +
                [u'│', (redornot, u'{}{}{}'.format(suit, spaces,rank.rjust(2))), u'│\n']
            )
        top = u'╭'+ '─' * (columns-2) +'╮\n'

        text = [top] + filling
        text += [u'╰' + '─' * (columns-2) + '╯\n']

        if isinstance(text[-1], tuple):
            text[-1] = text[-1][0], text[-1][1].strip()
        else:
            text[-1] = text[-1].strip()

        return text

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, card):
        self._card = card
        self.redraw()

    @property
    def face_up(self):
        return self.card.face_up

    @face_up.setter
    def face_up(self, val):
        self.card.face_up = bool(val)
        self.redraw()
