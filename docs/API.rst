.. _API:

===
API
===

This chapter will describe every RESTful API call you can make. You will have to change `localhost:5000` to whatever is you configuration.

manageuser
==========

You can add and remove player with a POST request. The :ref:`Create User <Create>` page uses this.

Parameter _action
-----------------

* *add*: to add a user
* *del*: to delete a user

Parameter username
------------------

This parameter is used to add a user. User will be named like the value of this parameter.

Parameter delusername
---------------------

This parameter is used to delete a user. User with the name like the value of this parameter will be deleted.

Examples
--------

Add a user named Johnny:

.. code-block:: bash

        curl -X POST 'http://localhost:5000/game/manageuser' -d "_action=add&username=Johnny"

Delete a user named Johnny:

.. code-block:: bash

        curl -X POST 'http://localhost:5000/game/manageuser' -d "_action=del&delusername=Johnny"

throw
=====

You can add a throw with a GET request.
The URL will look like `http://localhost:5000/game/throw/hit/mod`.
The :ref:`game controller <Controller>` page uses this.

Parameter Hit
-------------

This parameter determines which number was hit. It is supposed to be between 0-20 or 25, where 0 will be a miss 1-20 will be the corresponding number on the board and 25 will be bulls eye.

Parameter Mod
-------------

This parameter determines which modifier was hit. It is supposed to be between 1-3, where 1 is a hit within the big number fields or single bulls eye, 2 is a double or double bulls eye and 3 is a triple

Examples
--------

Hitting a single 5:

.. code-block:: bash

        curl -X GET 'http://localhost:5000/game/throw/5/1'

Hitting triple 20:

.. code-block:: bash

        curl -X GET 'http://localhost:5000/game/throw/20/3'

Hitting double bulls eye

.. code-block:: bash

        curl -X GET 'http://localhost:5000/game/throw/25/2'

throw update
============

You can update a throw with a GET request.
The URL will look like `http://localhost:5000/game/throw/update/throwid/newhit/newmod`
The :ref:`game controller <Controller>` page uses this.

Parameter throwid
-----------------

This parameter determines which throw has to be updated. Throws are counted up. So the first throw of the first player will start with id number 1 and the second throw will be number 2 and so on.

Parameter newhit
----------------

This parameter determines to which number the throw should be corrected. It is supposed to be between 0-20 or 25, where 0 will be a miss 1-20 will be the corresponding number on the board and 25 will be bulls eye.

Parameter newmod
----------------

This parameter determines to which modifier the throw should be corrected. It is supposed to be between 1-3, where 1 is a hit within the big number fields or single bulls eye, 2 is a double or double bulls eye and 3 is a triple

Example
-------

Correct throw with id `1` to be triple 20 instead.

.. code-block:: bash

        curl -X GET 'http://localhost:5000/game/throw/update/1/20/3'

nextPlayer
==========

You can change to the next player with a GET request.
The URL will look like `http://localhost:5000/game/nextPlayer`
The :ref:`game controller <Controller>` page uses this. Also this is used by a javascript function when no recognition is used to automatically switch user after three throws were inserted.

Example
-------

.. code-block:: bash

        curl -X GET 'http://localhost:5000/game/nextPlayer'
        -

endGame
=======

You can end the game with a GET request.
The URL will look like `http://localhost:5000/game/endGame`
The :ref:`game controller <Controller>` page uses this.

Example
-------

.. code-block:: bash

        curl -X GET 'http://localhost:5000/game/endGame'
        Done

rematch
=======

You can trigger a rematch of a game with a GET request.
The URL will look like `http://localhost:5000/game/rematch`
The :ref:`game controller <Controller>` page uses this.

.. caution::
        The game is supposed to be active but won (e.g. player score is 0 and podium placement is shown in scoreboard). Will not work if 'endGame' was issued.

Example
-------

.. code-block:: bash

        curl -X GET 'http://localhost:5000/game/rematch'
        -
