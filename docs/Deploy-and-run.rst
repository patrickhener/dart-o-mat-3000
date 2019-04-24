.. _Running:

==============
Run and Deploy
==============

There are two ways to run the scoreboard. Running it for development or running it in a productive environment.
The follwing sections will describe both as well as how to deploy it to run automatically at the systems start up.

For Development
===============

For development you can simply run it like the following code block shows.
Remember to activate the virtual environment first, if you happen to use one: `. venv/bin/activate`

.. code-block:: bash

    python ./run.py

You will now have a rich output of what is happening whilst you play.
The development server will restart everytime you change code and save it.
It will directly crash and give you stack traces if you have an error.
This is very convenient for developing.

Navigate your browser to |localhost| to see if it is working.

.. |localhost| raw:: html

    <a href="http://localhost:5000/game/" target="_blank">http://localhost:5000/game/</a>

Deploying for production
========================

If you want things to happen automagically you can follow this section.

* TODO explain how to use gunicorn to deploy it.
* TODO Write systemd service to start it on boot
* TODO Write autostart script to startup a browser window in fullscreen displaying the intro page
