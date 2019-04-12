# Introduction
This project is a scoreboard for a darts game which will run on an automated steel darts machine. It's purpose is to track the score of the game.
An automated darts recognition will be needed to use this scoreboard.

# Recommended darts recognition
As this project is developed depending on the following recognition software, it is recommended to use it: [https://github.com/nluede/cvdarts](https://github.com/nluede/cvdarts).
You can use any other recoginition as well, as long as it is propagating it's throws and next player via a GET Request to the scoreboard engine in this format:

- URL to insert a throw /game/throw/_number-of-throw_/_modifier-of-throw_
  - Example: Single 20 will be /game/throw/20/1
  - Example: Miss will be /game/throw/0/1
  - Example: Double 18 will be /game/throw/18/2
- URL to switch to next player /game/nextPlayer

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

# Configure it

Open up _config.py_ and edit:

```python
# Custom IP and Port Config, needed for example in QR Code generation
IPADDR = '192.168.1.160' #QRCode IP
IFACE = '0.0.0.0' #Server Interface IP
PORT = 5000
RECOGNITION = False #Use Recognition or not. If not you will have buttons to insert Score in gameController
SOUND = True #Sound output if you want
# Babel default settings
BABEL_DEFAULT_LOCALE = "de"
BABEL_DEFAULT_TIMEZONE = "UTC"
```
 to fit your needs. You are welcome to edit any other setting as well. But you do not really have to. Valid values for language are either `en` or `de`. As no time is used anywhere just ignore the timezone for now.

# Development run it
First activate the virtual environment like described above. Then run `python3 run.py`.
To leave the virtual environment you just stop the service with `ctrl+c` and then run `deactivate`.

Now you'll find the scoreboard at [http://127.0.0.1:5000/game/](http://127.0.0.1:5000/game/).

# Deploy it
TODO explain how to use gunicorn to deploy it.  
TODO Write systemd service to start it on boot  
TODO Write autostart script to startup a browser window in fullscreen displaying the intro page

# General TODOs
- Rematch Button(Button handling is okay, implement /rematch route to do something)
- Sound when next Player button is pressed
- Ask yes/no if you hit End Game Button
- Different Sounds to choose from
- Delete last Throws when first throw of new round
- Average of round sum not of all Throws
- Game Controller to only show last two throw round per user 
- Show Player score in game controller
- Show active player in game controller
- When Bust change throws to zero and don't delete them from database
- If more than 2 player do not end game after one player get's 0/wins cricket
- Cricket game mechanism
- Cricket scoreboard

# Changelog
## 2019-04-10 - v0.9: Alpha version
- Working condition: It might not work that stable. There will still be bugs. Therefore it is only Alpha.
- Ready features:
  - Game mechanism X01 is working with double/master in/out and sound
  - Game Controller X01 is working to either correct throws or to insert throws like any mobile app does

