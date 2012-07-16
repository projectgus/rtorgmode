rtm2orgmode is a very simple Python web app. It takes your
[Remember The Milk](http://www.rememberthemilk.com/) (aka RTM) task
lists and exports them in a format compatible with
[emacs org-mode](http://orgmode.org/).

This product uses the Remember The Milk API but is not endorsed or
certified by Remember The Milk.


# Using

You can use a
[hosted version of rtm2orgmode online](http://chainxor.org/rtm2orgmode),
but this README shows how to run it standalone on your computer.


# Prerequisites

* [milky](https://bitbucket.org/Surgo/milky/src), a Python RTM
  client. There's no pip/easy_install for this module, so I just copied
  the "milky" module directory straight into the rtm2orgmode
  directory.

* [Bottle](http://bottlepy.org) web framework (*pip install
  bottle* or *apt-get install python-bottle* or similar.)

* You'll need your own [RTM API Key](http://www.rememberthemilk.com/services/api/keys.rtm)

* Create a file in the rtm2orgmode directory called "api_key.py" with your RTM API key, like this:

	API_KEY = "myapikeyinquotes"
	API_SECRET = "myapikeysharedsecretinquotes"


# Running Locally

Running

    python rtm2orgmode.py

Will create a web server running on http://localhost:8000 that you can
connect to. The first time you connect it will redirect your browser
to RTM to authorise the app.

# Authorisation

The rtm2orgmode script expects to receive a callback redirect from RTM
of the form *localhost:8000/?frob=123456*, with the 123456 frob value
supplied by RTM to authorise access.

You can cheat on your local computer by looking at the *Application
successfully authorized* screen after you authorise your app in
RTM. Look at the URL bar and copy the frob, which is the part between
*frob=* and *&*. Then paste it into a new URL of the form
*http://localhost:8000/?frob=* and the exporter will run.

You have to do this every time you run an export, because rtm2orgmode
doesn't save the RTM authentication token.


# License

rtm2orgmode.py is licensed under the MIT license:

Copyright (c) 2012, Angus Gratton

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
