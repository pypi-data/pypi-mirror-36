paybybot
========

Simple bot that sends you an email when you didn’t pay your parking on
https://www.paybyphone.fr/

Installation on a Raspberry PI
------------------------------

Get pip
~~~~~~~

::

   apt-get install python3-pip

Install paybybot
~~~~~~~~~~~~~~~~

::

   pip3 install paybybot

Configure your credentials
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   # ~/.paybybot
   {Your phone number}:{PayByPhone password}

   # ~/.email-creds
   {Your email address}:{Email password}

For your email account, I advise you to use an app password. See
`here <https://support.google.com/accounts/answer/185833?hl=en>`__ for
Gmail.

Geckodriver
~~~~~~~~~~~

Inspired by https://askubuntu.com/a/871077

1. Go to the `geckodriver releases
   page <https://github.com/mozilla/geckodriver/releases>`__. Find the
   latest version of the driver for the ARM platform and download it.
   For example:

   ::

       wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz

2. Extract the file with:

   ::

       tar -xvzf geckodriver*

3. Make it executable:

   ::

       chmod +x geckodriver

4. Add the driver to your PATH so other tools can find it:

   ::

       echo "export PATH=\$PATH:$PWD/geckodriver" >> .bashrc
