# Librewary

Librewary is an online equipment lending management system written in the Python django framework.

It currently only supports one _brewing club_ per deployment, but support multiple groups is a forthcoming feature.

Dual licensed under MIT and GPLv2.

# Installation (local development on Ubuntu)

* `sudo apt-get install python-pip`
* `sudo pip install virtualenvwrapper`
* `sudo pip install autoenv`
* Append this to `.bashrc`:

```
# virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$HOME/Devel
source /usr/local/bin/virtualenvwrapper.sh

# autoenv
source ~/packages/autoenv/activate.sh
```

* `mkvirtualenv librewary`
* `mkdir -p code`
* `cd code/`
* `git clone git@github.com:pztrick/librewary.git`
* `cd librewary/`
* `cp .env.copy .env`
* `cd .` _(respond `y`es to executing the autoenv script)_
* `pip install -r requirements.txt`
* `python manage.py syncdb`
* `python manage.py migrate`
* `echo '127.0.0.1 localhost.librewary.com' | sudo tee -a /etc/hosts` _(trick required for localhost Facebook login)_
* `python manage.py runserver 0.0.0.0:4000` _(if you use the `.env` file, this is aliased to `rs`)_
* Copy all the `.template` files to their originals

# Development workflow

This project uses a master branch which is hosted on the _www.librewary.com_ production server and a stable development branch which is located at _beta.librewary.com_. Feature branches are developed locally before being committed to the develop branch (e.g. in a `merge --squash` commit). You should develop locally using the `runserver` django management command.

# How to get involved

Drop a short line to Patrick Paul [<http://pztrick.com>](http://pztrick.com).