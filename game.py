# -*- coding: utf-8 -*-

import random


SUIT_SYMBOLS = {
    'spades': u'♠',
    'diamonds': u'♦',
    'clubs': u'♣',
    'hearts': u'♥',
}


class InvalidMove(Exception):
    """Raised to indicate an invalid move"""


class Card(object):
    def __init__(self, rank, suit, face_up=False):
        self.rank = rank
        self.suit = suit
        self.face_up = face_up

    def __repr__(self):
        return 'Card(rank={0.rank!r}, suit={0.suit!r}, face_up={0.face_up!r})'.format(self)

    @property
    def suit_symbol(self):
        return SUIT_SYMBOLS[self.suit]


class Deck(object):
    ranks = ['A'] + [str(n) for n in range(2, 11)] + list('JQK')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit)
                       for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __iter__(self):
        return iter(self._cards)

    def shuffle(self):
        random.shuffle(self._cards)


def suit_color(suit):
    return 'red' if suit in ('diamonds', 'hearts') else 'black'


class Game(object):
    def __init__(self):
        deck = Deck()
        deck.shuffle()
        cards = list(deck)
        for n in range(1, 8):
            self.tableau.append([cards.pop() for _ in range(n)])
        