# Quintana

This repository is a muli-container docker app that hosts a financial API. 

It's built with:
* Docker & docker-compose
* Nginx
* Gunicorn
* Flask
* LetsEncrypt
* Postgres

**Note: Tested on Ubuntu 18.04 hosted on digitalocean.**

## Docker

service | image
--- | ---
flask & gunicorn | `alpine:3.11.0`
nginx | `nginx:1.17.7-alpine`
postgres | postgres:12-alpine

## Requirements

dependency | commands
--- | ---
docker | [commands for Debian / Ubuntu](https://gist.github.com/smallwat3r/45f50f067f248aa3c89eec832277f072)
docker-compose | [commands for Debian / Ubuntu](https://gist.github.com/smallwat3r/bb4f986dae4cb2fac8f26c8557517dbd)
make | `sudo apt install make`
a domain or sub-domain | DNS A record needs to points to your server static IP

## Setting things up

#### 1) Clone this repo on your server

I recommend doing this in `/opt`  

```sh
cd /opt
sudo git clone https://github.com/brettelliot/quintana.git
```

Install docker, docker-compose and make (explained [above](#requirements)).  

#### 2) Add user to `docker` group  

```sh
sudo usermod -aG docker $USER
```
Log out from the server and log back in for changes to apply.  

#### 3) Open the firewall for letsencrypt
```sh
sudo ufw allow http
sudo ufw allow https
sudo ufw status
```
#### 4) Define applications details
Copy `.env.example` to `.env` and enter your application details.   
```sh
# .env.example

# Email to get alerts from Letsencrypt.
EMAIL=email@email.com

# Domain name or subdomain linked to your server's public IP.
DOMAIN=mydomain.com

# Folder where is located your flask app in the repo. In this example
# it's under ./core/
APP_FOLDER=core

# Application environment.
FLASK_ENV=development

# If can be the app's entrypoint (wsgi if using ./core/wsgi.py)
# or the application package (as in this case) as the app's
# configs are under ./core/flask_app/__init__.py
FLASK_APP=flask_app

# The flask app's api is secured with an api key stored in an environment 
# variable. Set it to something stronger in production:production
API_KEY=demo_key

# Postgres stuff. Replace with more meaningful values
POSTGRES_USER=pguser
POSTGRES_PASSWORD=pgpw
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=pgdb
```

## Turning it on

**Start application**
```sh
sudo make dc-start
```
<p style="text-align: center;">
 🎉 Your web-app should now be running online with HTTPS 🎉   
</p>

**Other commands**
```sh
sudo make dc-reboot      # Reboot application.
sudo make dc-stop        # Stop application.
sudo make dc-cleanup     # Delete and clear docker images.
sudo make dc-start-local # Start application w/o nginx (for running locally)
sudo make dc-ps          # Show what docker processes are running
sudo make dc-pg          # Only run the postgres db service
```

Auto checks are running weekly to update the certificates. 

## Testing it

Locally:
* http://0.0.0.0:5000/
* http://0.0.0.0:5000/api/v1/tests/secure-object?api_key=demo_key
* http://0.0.0.0:5000/api/v1/tests/secure-pg-object?api_key=demo_key

To test remotely, simply use https and the domain name of your server.

## Updating the host after a change
Let's say quintana has been updated. This is how you get the new changes on the host:

```sh
cd /opt/quintana

# Shutdown everything
sudo make dc-stop

# Get the changes
sudo git checkout master
sudo git pull origin master

# Update the .env file if needed
sudo cp .env.example .env
sudo vim .env

# run it
sudo make dc-start

# check its running
sudo make dc-ps
```

