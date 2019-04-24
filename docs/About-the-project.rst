=================
About the project
=================

As I started playing Darts I always used to play on electronic Dart boards.
I started to wonder how it will be to play steel dart, so I bought a steel dart board and some steel darts and played.
Soon I began to realise that scoring on paper or with an mobile app might work but is not as **sexy** as I hoped for.

That was the moment this project was born. There aren't much projects like this online ready to use.
Either they are closed source or they do not work like I wanted them to do.

So with this motivation I started coding this project.

The idea
========

I was thinking of a scoreboard which has to handle score mechanisms on different games.
It has to work with multiple players and has to look some way of **sexy**.

The structure
=============

The scoreboard is supposed to be shown on a display in front of the player. At the best the display is standing right on
top of the dart board compartment or maybe a little to the left or right of the dart board.
You will use any smartphone or tablet as a game controller to control the game setup.

Recognition anyone?
===================

As there were already a few projects online using webcams and openCV to recognise Darts beeing thrown to a dart board
and to get the number and modifier hit I was curious if this will be working with my scoreboard project maybe.
So I designed the scoreboard to have a RESTful API which the recognition software can use to insert throws automatically.
This way the scoreboard will work fully automatically giving the players the feeling they are playing with a electronic
dart board, BUT with a regular steel dart board.

No recognition, no problem!
===========================

If you do not want to use a "complicated" recognition setup I didn't want to let players down.
So I designed the scoreboard to handle this case as well. In this case buttons will be displayed within the gameController
module. With this buttons you can use the scoreboard like any other mobile app you can find for dart scoring.

A few words on the coding language
==================================

As I am using python a lot at work it came naturally to me to use python here as well.
Also I think it will address a broad community if someone wants to contribute.
For the webservice I am using python flask with sqlalchemy to store game data.
For the live updates with the scoreboard python socketio is used.
Together it will build a nice and smooth experience while playing.

Ready to start?
===============

So you feel like you want to test it out yourself? Then go ahead and check out how information on :ref:`recognition software <Recognition>` and how to :ref:`install <Installation>` everything.