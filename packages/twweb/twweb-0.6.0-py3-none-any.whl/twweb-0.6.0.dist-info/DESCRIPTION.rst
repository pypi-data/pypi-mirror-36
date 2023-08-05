TWWeb is `Taskwarrior's <https://taskwarrior.org>`__ web interface.

It's aimed to be run on a internet-facing web server by a single user (it
currently supports only a single registered user and a single taskrc).

Quick test
==========

You can quickly check if TWWeb suits your needs by running a development server
locally on your computer.

::

    $ tox -e dev

After running this command TWWeb will be accessible on ``localhost:5000``. You
can change the port on which development server listens this way:

::

    $ tox -e dev -- --port=3333

Installation with Docker
========================

TWWeb provides a Docker image. You can quickly build a container and run an
image like that:

::

    # docker build . -t twweb
    # docker run -p 5456:5456 twweb

After that you should be able to open TWWeb in your browser on address
``localhost:5456``. Image preserves all data and configuration inside ``/data``
directory, so it's preferable to mount it as a volume:

::

    # docker run -v data:/data -p 5456:5456 twweb

Docker image will pre-populate ``/data`` with TWWeb's settings as long as
configuration file is not found.  Other settings (uwsgi configuration and
taskrc) won't be pre-populated when ``/data`` is mounted as a host directory.

You can change settings before the first run with the following environment
variables (listed together with their default values):

- ``TWWEB_SETTINGS`` [/data/twweb.cfg]: path to TWWeb's configuration file.
- ``TWW_CFG_SECRET`` [empty]: TWWeb's secret key used for encryption. If this is
  empty, image will generate a random secret on first run. Leave it empty in
  most cases.
- ``TWW_CFG_PIN`` [twweb]: PIN used for registration of the first user. You
  probably should change it
- ``TWW_CFG_DB_ENGINE`` [sqlite]
- ``TWW_CFG_DB_HOST`` [/data/twweb.db]
- ``TWW_CFG_TW_TASKRC`` [/data/taskrc]

Example:

::

    # docker run -v data:/data -p 5456:5456 \
                -e TWW_CFG_SECRET=extraSecret1122 \
                -e TWW_CFG_PIN=supersecret \
                twweb

You can also build and run the image via a docker-compose.

Manual Installation
===================

To install TWWeb you'll need a web server able to run Python applications.
You'll also need a database, but sqlite should be fine as TWWeb doesn't store a
lot. Obviously you'll also need a working Taskwarrior.

We'll install all required components inside a virtualenv. Before you start, you
should select and create a directory in which TWWeb will be placed. For now
we'll assume ``/var/www/example.com/twweb``, where "example.com" part is
typically replaced with a name of your domain.

::

    $ sudo mkdir -p /var/www/example.com/twweb
    $ sudo chown $USER:www-data /var/www/example.com/twweb
    $ chmod 775 /var/www/example.com/twweb
    $ cd /var/www/example.com/twweb

Above commands create and set appropriate permissions for TWWeb's directory.
When following this installation method, TWWeb itself will need write
permissions in this directory so that's why we change the group permission to
``rwx``.

Taskwarrior configuration
-------------------------

For Taskwarrior, choose the most appropriate installation method for your
server. Keep in mind that you'll need a ``task`` executable which will be
available in ``$PATH`` of a user which will run TWWeb (typically ``www-data``).

For example, for Debian-based distributions the following command should do the
trick:

::

    $ sudo apt install task

Now create a separate taskrc and task directory in which Taskwarrior will store
its data:

::

    $ mkdir -m 775 task && chown $USER:www-data task
    $ echo "data.location=`pwd`/task" > taskrc

If you want to use synchronization with Task Server, you can place your
certificates in this directory and configure it inside a newly created
``taskrc`` file.

Installation with uWSGI
-----------------------

Now we'll install TWWeb and uWSGI inside a new virtualenv:

::

    $ virtualenv -p python3 venv
    $ venv/bin/pip install twweb uwsgi
    $ inst=`find venv -name twweb -type d`

The last command saves the path to the directory in which TWWeb package is
located. It's not strictly required, but will become handy later.  Typically it
will be found in a directory like ``venv/lib/python3.5/site-packages/twweb``.

Inside ``utils`` directory in Git repository there are various example
configuration files. One of them is ``twweb-uwsgi.ini`` which is a configuration
for uwsgi. You can edit it to your likings, but the original one should work
fine as well. Copy it to your current directory.

Now we'll create TWWeb's configuration file, named ``twweb.cfg``. We'll add a
custom ``SECRET_KEY`` and ``PIN`` to it (*VERY IMPORTANT*). We'll also point
sqlite database to our directory and taskrc to the previously created one:

::

    SECRET_KEY = 'this should be secret and complex'
    PIN = 'additional password used for first register'

    DB_ENGINE = 'sqlite'
    DB_HOST = '/var/www/example.com/twweb/twweb.db'

    TW_TASKRC = '/var/www/example.com/twweb/taskrc'

You have to point to it via ``TWWEB_SETTINGS`` environment variable, for example
this way:

::

    $ export TWWEB_SETTINGS=`pwd`/twweb.cfg

And that's it! You can run TWWeb with ``venv/bin/uwsgi --ini twweb-uwsgi.ini``.
Logs are stored inside ``/var/log/uwsgi/twweb.log``.

Now you'll have to configure your web server (e.g. Apache or Nginx) to forward
all requests to your uwsgi app. For example for Nginx you can add something like
that:

::

    location /update {
      include uwsgi_params;
      uwsgi_pass unix:/run/uwsgi/twweb.socket
    }


