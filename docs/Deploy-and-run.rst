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

    ./run.py

You will now have a rich output of what is happening whilst you play.
The development server will restart everytime you change code and save it.
It will directly crash and give you stack traces if you have an error.
This is very convenient for developing.

Navigate your browser to |localhost| to see if it is working.

.. |localhost| raw:: html

    <a href="http://localhost:5000/game/" target="_blank">http://localhost:5000/game/</a>

Deploying for production
========================

The following instructions are mainly taken off |serve|. Feel free to follow along those instructions instead or follow the steps below.

.. |serve| raw:: html

        <a href="https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04" target="_blank">this tutorial</a>

Gunicorn
--------

You can use gunicorn do deploy the app in a production environment. It is highly recommended to follow this steps.

Create virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have not already done this now is the time to. Navigate to the root folder and do the following:

.. code-block:: bash

        python -m venv ./.venv

Activate the virtual environment afterwards and install requirements.

.. code-block:: bash

        source .venv/bin/activate
        pip install -r requirements

Test gunicorn
^^^^^^^^^^^^^

Test if everything is working out.

.. code-block:: bash

        gunicorn --bind 0.0.0.0:5000 --worker-class eventlet -w 1 run:app --reload

The output should show something like:

.. code-block:: bash

        [2019-04-25 13:25:26 +0200] [1605] [INFO] Starting gunicorn 19.9.0
        [2019-04-25 13:25:26 +0200] [1605] [INFO] Listening at: http://0.0.0.0:5000 (1605)
        [2019-04-25 13:25:26 +0200] [1605] [INFO] Using worker: eventlet
        [2019-04-25 13:25:26 +0200] [1608] [INFO] Booting worker with pid: 1608

You can exit out pressing `CTRL+C` and deactivate the virtual environment by issueing the command `deactivate`.

Systemd service for autostart
-----------------------------

We will use a systemd service to automatically start the gunicorn server for us.

As root create a service file called **dom3000.service** under **/etc/systemd/system/**.
It's content should look like this. Remember to alter the paths to fit your path structure:

Systemd service file
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

        [Unit]
        Description=Gunicorn instance to serve Dart-O-Mat 3000
        After=network.target
        
        [Service]
        User=patrick
        WorkingDirectory=/home/patrick/dart-o-mat-3000
        Environment="PATH=/home/patrick/dart-o-mat-3000/.venv/bin"
        ExecStart=/home/patrick/dart-o-mat-3000/.venv/bin/gunicorn --workers 1 --worker-class eventlet --bind 0.0.0.0:5000 run:app --reload
        
        [Install]
        WantedBy=multi-user.target

Choosing 0.0.0.0:5000 as a bind address will bind the server to all interface IPs on port 5000.
Afterwards you can test if it starts. And if it does you can enable it to start automatically at boot time.

Enable service
^^^^^^^^^^^^^^

.. code-block:: bash

        sudo systemctl start dom3000.service
        sudo systemctl status dom3000.service
        sudo systemctl enable dom3000.service

Finally to test if the service is running fine just go and point your browser to |localhost| directly on the Dart-O-Mat 3000 machine or to it's corresponding interface IP like for example |ip|

.. |ip| raw:: html

        <a href="http://192.168.1.10:5000/game/" target="_blank">http://192.168.1.10:5000/game/</a>

Nginx configuration
-------------------

We will use nginx as a proxy to handle connections to our gunicorn service.
If you have not yet installed nginx |now| is the time to.

.. |now| raw:: html

        <a href="https://www.nginx.com/resources/wiki/start/topics/tutorials/install/" target="_blank">now</a>

Nginx config file
^^^^^^^^^^^^^^^^^

Next we will create a config file called **dom3000** under **/etc/nginx/sites-available/**

It will have this content

.. code-block:: bash

        server {
            listen 80;
            server_name localhost;

            location /socket.io/ {
		proxy_http_version 1.1;

		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection "upgrade";

		proxy_pass http://localhost:5000/socket.io/;
            }


            location / {
                include proxy_params;
                proxy_pass http://localhost:5000/;
            }
        }

Enable site
^^^^^^^^^^^

Now we enable the site by linking to this file

.. code-block:: bash

        sudo ln -s /etc/nginx/sites-available/dom3000 /etc/nginx/sites-enabled
        sudo systemctl restart nginx

Test if it is working
^^^^^^^^^^^^^^^^^^^^^

You now should be able to get your **Dart-O-Mat 3000** at either |localhost2| directly on the machine or at it's corresponding IP address like for example |ip2|


.. |localhost2| raw:: html

        <a href="http://localhost/game/" target="_blank">http://localhost/game/</a>

.. |ip2| raw:: html

        <a href="http://192.168.1.10/game/" target="_blank">http://192.168.1.10/game/</a>

Setup config.py for production
------------------------------

You should be sure to choose the correct configuration flags in config.py in the root directory of **Dart-O-Mat 3000**. Those are

.. code-block:: bash

        IPADDR = '192.168.1.10'  # QRCode IP
        DEBUG = False
        TESTING = False

As we are not testing or developing in this scenario be sure to choose False for both of this flags. Also you need to choose the right IP address so the QR code will be drawn accordingly.

Be sure to restart the **dom3000.service** afterwards issueing the command `sudo systemctl restart dom3000.service`

Autostart browser and index page
--------------------------------


