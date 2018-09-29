# -*- coding: utf-8 -*-
import urwid


PALETTE = [
	('red', 'dark red', ''),
	('selectedred', 'dark red', 'yellow'),
	('selected', '', 'yellow'),
]

SIZES = {'small': (4, 3), 'medium': (8, 6)}


class BaseCardWidget(urwid.WidgetWrap):
    def __init__(self, *args, card_size='small', **kw):
        self.card_columns, self.card_rows = SIZE_MOD[card_size]
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
        return [u' '* self.card_columns +'\n'] * self.card_rows


class CardWidget(BaseCardWidget):
    highlighted = False

    def __init__(self, card, onclick=None):
        self._card = card
        self.text = urwid.Text('', wrap='clip')
        self.highlighted = False
        self.onclick = onclick
        super(CardWidget, self).__init__(self.text)

    def __repr__(self):
        return '{}(card={!r}, highlighted={!r}, ...)'.format(
            self.__class__.__name__, self.card, self.highlighted,
        )

    def mouse_event(self, size, event, button, col, row, focus):
        if self.playable and event == 'mouse press':
            now = time.time()
            if (self.last_time_clicked and (now - self.last_time_clicked < 0.5)):
                if self.on_double_click:
                    self.on_double_click(self)
            else:
                if self.onclick:
                    self.onclick(self)
            self.last_time_clicked = now

    def _draw_card_text(self):
        columns, rows = self.card_columns, self.card_rows

        style = 'selected' if self.highlighted else ''
        redornot = 'red' if self.card.suit in ('hearts', 'diamonds') else ''
        if self.highlighted:
            redornot = 'selected' + redornot
        if not self.face_up:
            face_down_middle_filling = (columns-2) * u'╬'
            if self.on_pile and not self.top_of_pile:
                filling = [u'│', (style, face_down_middle_filling), u'│\n']
            else:
                filling = [u'│', (style, face_down_middle_filling), u'│\n'] * (rows-2)
        else:
            rank, suit = (self.card.rank, self.card.suit_symbol)
            spaces = (columns-5) * ' '
            filling = [u'│', (redornot, u'{}{}{}'.format(rank.ljust(2), spaces, suit)), u'│\n']
            if not self.on_pile or self.top_of_pile:
                filling += (
                    [u'│', (style, u' ' * (columns-2)), u'│\n'] * (rows-4) +
                    [u'│', (redornot, u'{}{}{}'.format(suit, spaces,rank.rjust(2))), u'│\n']
                )
         

        if self.on_pile and not self.bottom_of_pile: 
            top = u'├'+ '─' * (columns-2) +'┤\n'
        else: 
            top = u'╭'+ '─' * (columns-2) +'╮\n'

        text = [top] + filling
        if not self.on_pile or self.top_of_pile:
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
