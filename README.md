# Introduction
This project is a scoreboard for a darts game which will run on an automated steel darts machine. It's purpose is to track the score of the game.
An automated darts recognition will be needed to use this scoreboard.

# Recommended darts recognition
As this project is developed depending on the following recognition software, it is recommended to use it: [https://github.com/nluede/cvdarts](https://github.com/nluede/cvdarts).
You can use any other recoginition as well, as long as it is propagating it's throws and next player via a GET Request to the scoreboard engine in this format:

- TODO add GET URL for throw
- TODO add GET URL for nextPlayer

# Scoreboard
This scoreboard is written in python flask. It uses flaskIO for websockets.

# Setup
To setup the server you will need to install the requirements first.
It might be best to use an virtual environment like so:

```
python3 -m venv ./venv
. venv/bin/activate
```

This will activate an virtual environment.

No you can safely run `pip3 install -r requirements.txt` without screwing up your python3 locally.

Open up _config.py_ and edit *IPADDR* and *PORT* to match your network settings.

# Development run it
First activate the virtual environment like described above. Then run `python3 run.py`.
To leave the virtual environment you just stop the service with `ctrl+c` and then run `deactivate`.

Now you'll find the scoreboard at [http://127.0.0.1:5000/game/](http://127.0.0.1:5000/game/).

# Deploy it
TODO
