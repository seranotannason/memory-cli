# Design Document for the Two-Players Memory Game

## Instructions
To optimize the playing experience, please enable the required Unicode support in the terminal:
```
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```
Then run:
```
python memory-cli/app.py
```
That's all, enjoy!

## Design Choices: **DRY** (Don't Repeat Yourself)
Object-oriented programming (OOP) is the backbone of this app. The OOP design of my project was inspired by the design so beautifully written in the following repository, which I have rightfully credited in my LICENSE file: https://github.com/eliasdorneles/usolitaire. </br>

The app is modularized into three main scripts: app, game, ui. 


Because I am using Urwid as my main console-based programming library, it is only natural to implement all widgets in the UI file.


The game script details the card, deck, and game classes that make up a game instance.


Finally, the app script contains the main logic that powers the game. This is the main script that we run!

## Data Structures and Algorithms: **KISS** (Keep It Simple, Stupid)
I used Python's list and Urwid's native widget collections as my data structures. No fancy algorithm was used in the process; I kept it simple. :-)

## Tools
I use Python, the language I am most fluent in, because I did not have much experience making console-based games (it's 2018; who does, really?) and I wished to prototype ideas quickly.


I use Urwid as my main library because a quick research confirms that it's been tried, tested, and used to build many great projects (e.g. Zulip's terminal interface).
