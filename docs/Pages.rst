=====
Pages
=====

This chapter will describe every single page involved in the scoreboard and it's function.
For notation I will choose to just give you the subpath without the complete `http://hostip:port`.


Index
=====

.. _Index:

The index page can be found at path `/game/`.

.. image:: images/index.png

The user is supposed to scan the generated QR code to redirect his smartphone to the :ref:`Admin <Admin>` page.

Admin
=====

.. _Admin:

The admin page can be found at path `/game/admin`.

The admin page will give you all the possibilities to setup a game.

.. image:: images/admin.png

You first select all player you want to create a game with. If you have not already created player the link on the bottom of the page (`linktext: one!`) will redirect you to page :ref:`Create User <Create>`. Then you can choose which game to play and the game specific settings.
After pressing `Start Game` the admin page will be redirected to the :ref:`game controller <Controller>` and the :ref:`index page <Index>` will be redirected to the corresponding :ref:`scoreboard <Scoreboards>`.

Go :ref:`here <Games>` if you want to get a good overview of the games available and the rules.


GameController
==============

.. _Controller:

The game controller page can be found at path `/game/gameController`.

Within this page the user is able to influence several things within a running game. In general the controller page will look slightly different depending on which game you play. Also it will not show certain areas when playing with an active darts recognition software in comparison to playing without one.

.. image:: images/controller.png

As an example you see two players playing 301. The page consists of different sections.

Game Controls
-------------

With the game controls you can either switch to the next player by pressing the button `Next Player` or you can end the game by pressing the button `End Game`.
Also when a game is over the next player button will turn into a Rematch button which will start over the game with the exact same setup, when pressing the button.

Insert Throws
-------------

.. _Insert:

This section will only be shown when no recognition software is used (i.e. if the RECOGNITION flag in the :ref:`configuration <Configuration>` is set to False).
Here you can insert throws just like in any mobile app for counting darts. If you wanna enter a double or a triple value be sure to hit double or triple first.

.. caution::
   When hitting double or triple there is no way of `unhitting` it for now.

.. tip::
   When three throws were inserted the controller is changing to the next player automatically.

The throw will then be inserted to the current players throws and will be handled by the game.

Update Throws
-------------

This section will give you the possibilities to update throws which were inserted wrong either by hand or by the recognition software.

.. danger::
   Only throws within the last round of the player can be changed. So be sure to change wrong throws right away!

To change a throw just hit the throw which is wrong and a menu will appear. It looks exactly like the :ref:`Insert Throws <Insert>` interface and works alike.

Scoreboards
===========

.. _Scoreboards:

Scoreboards will always highlight the active player with a white frame.

X01
---

This Scoreboard will show the progress of a X01 game.
The X01 Scoreboard page can be found at path `/game/scoreboardX01`.

.. image:: images/x01.png

1. This area will show:

   * The current active player name
   * How many rounds the player has already played
   * The throw average of the rounds
   * The throwcount of the player

2. This area will show:

   * The game which is player
   * Game specific variants chosen

3. Individual player name
4. Player Score
5. Last three player throws
6. Sum of last three palyer throws
7. Message area used for checkout possibilities or other messages (Winner, Remove Darts, ...)

Cricket
-------

This scoreboard will show the progress of a Cricket game.
The Cricket Scoreboard page can be found at path `/game/scoreboardCricket`.

.. image:: images/cricket.png

1. This area will show:

   * The current active player name
   * How many rounds the player has already played
   * The throwcount of the player

2. This area will show:

   * The game which is player
   * Game specific variants chosen

3. Individual player name
4. Player Score
5. Message area used for messages (Winner, Remove Darts, ...)
6. Last three player throws
7. Cricket table (Numbers will vanish when closed)

   * / means got hit once
   * X means got hit twice
   * .. raw:: html

        &#10683;

        means got hit three times and is opened

Around the clock
----------------

This scoreboard will show the progress of a Around the clock game.
The Around the clock Scoreboard page can be found at path `/game/scoreboardATC`.

.. image:: images/atc.png

1. This area will show:

   * The current active player name
   * How many rounds the player has already played
   * The throwcount of the player

2. This area will show:

   * The game which is player
   * Game specific variants chosen

3. Individual player name
4. The next number supposed to be hit
5. Message area used for messages (Winner, Remove Darts, ...)

Split-Score
-----------

This scoreboard will show the progress of a Split-Score game.
The Split-Score Scoreboard page can be found at path `/game/scoreboardSplit`.

.. image:: images/splitscore.png

1. This area will show:

   * The current active player name
   * How many rounds the player has already played
   * The throwcount of the player

2. This area will show:

   * The game which is player
   * Game specific variants chosen

3. Individual player name
4. Player Score
5. Last three player throws
6. The next number / area supposed to be hit
7. Message area used for messages (Winner, Remove Darts, ...)

Create User
===========

.. _Create:

The index page can be found at path `/game/manageuser`.

On this page you can manage available users.

.. image:: images/create.png

Either you enter a name and hit `Create User` to create one or you choose a user in the list and hit `Delete Selected User` to delete the user.

You can go back to the :ref:`admin <Admin>` page by hitting the link text `back`.
