.. _Configuration:

=============
Configuration
=============

I decided to use a central config file on all the configurations a user is supposed to do.
The file is called *config.py* and can be found in the root directory of the project.

Configuration Parameters
========================

The following configuration parameters can be found in the configuration file.
The table gives an overview for what they are used:

+------------------------+----------------------------------------------+
| Parameter              |          Function                            |
+========================+==============================================+
| IPADDR                 | QRCode IP address for index page             |
+------------------------+----------------------------------------------+
| IFACE                  | Server Interface IP for the webserver        |
+------------------------+----------------------------------------------+
| PORT                   | Server Interface Port for the webserver      |
+------------------------+----------------------------------------------+
| SSL                    | Server Interface is https (SSL) or plain     |
+------------------------+----------------------------------------------+
| RECOGNITION            | Use recognition software or not.             |
|                        | GameController will look different depending |
|                        | on this flag                                 |
+------------------------+----------------------------------------------+
| SOUND                  | Control wether to play sound or not          |
+------------------------+----------------------------------------------+
| BABEL_DEFAULT_LOCALE   | Controls the language to be displayed.       |
|                        | For now either `de` or `en`.                 |
+------------------------+----------------------------------------------+
| BABEL_DEFAULT_TIMEZONE | Timezone to use. Isn't used yet within the   |
|                        | code, though.                                |
+------------------------+----------------------------------------------+
| DEBUG                  | Python Flask Debugging mode                  |
+------------------------+----------------------------------------------+
| TESTING                | Python Flask Testing mode                    |
+------------------------+----------------------------------------------+

The other parameters are not supposed to be changed.

Edit the configuration to your liking and proceed to :ref:`running <Running>` the scoreboard.


