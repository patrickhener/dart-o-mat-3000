.. _Installation:

============
Installation
============

As the first requirements you will need `Python3` and `Python3-Pip`.
You might wanna refer to the official documentation on how to install `python <https://docs.python.org/3/>`_ and `pip <https://pip.pypa.io/en/stable/installing/>`_
for your specific operating system.

Virtual Environment
===================

It is recommended to use a virtual environment to keep your pip clean. If you do not want to use one just continue with the next section.

To install and activate the virtual environment do the following:

.. code-block:: bash

    pip install --user virtualenv
    python -m venv ./venv
    . venv/bin/activate

Install python package requirements
===================================

To install the requirements you can use *pip* again like shown in the code block below. Keep in mind that you can do this either
within a virtual environment or not.

.. code-block:: bash

    pip install --user -r requirements.txt

You should no have everything in place to :ref:`configure <Configuration>` and :ref:`run <Running>` the scoreboard.