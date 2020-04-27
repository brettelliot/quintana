# Quintana

This repository is a muli-container docker app that hosts a financial API. It pulls data from IEX and stores it in a postgres database so you can access it as often as you need by only making one call to IEX for the data. This prevents unessecary message spend when (for example) pulling data into google spreadsheets. 

It has one endpoint (right now) that returns data from a company's latest financial statement.

## `financials` endpoint
This endpoint gets the latest financial statement data (10-K or 10-Q) including the balance sheet, income statement, and cash flow. In theory, it only pulls the data once per report per symbol and when new reports come out, will replace the existing one with the newest one. However, the trigger for this is the `nextEarningsDate` from the IEX key stats endpoint. This endpoint is only as up to date as that value.

**HTTP Request:** 
`GET /api/v1/stock/{symbol}/financials?api_key=demo_key`

**JSON Response:**
```json
{
  "accountsPayable": 10790437732, 
  "capitalExpenditures": -767105698, 
  "capitalSurplus": 66862789259, 
  "cashChange": 9308632926, 
  "cashFlow": 4130950224, 
  "cashFlowFinancing": 6193277103, 
  "changesInInventories": null, 
  "changesInReceivables": 557959624, 
  "commonStock": 2526814523, 
  "companyName": "Procter & Gamble Co.", 
  "costOfRevenue": 8552874444, 
  "currency": "USD", 
  "currentAssets": 28442605654, 
  "currentCash": 15604376329, 
  "currentLongTermDebt": null, 
  "depreciation": 828857515, 
  "dividendsPaid": -1994230129, 
  "ebit": 3569147262, 
  "exchangeRateEffect": -170178544, 
  "fiscalDate": "2020-03-30", 
  "goodwill": 40640827706, 
  "grossProfit": 8971868934, 
  "incomeTax": 541175596, 
  "intangibleAssets": 24927842380, 
  "interestIncome": null, 
  "inventory": 5390705642, 
  "investingActivityOther": null, 
  "investments": -3069555, 
  "longTermDebt": 24732160939, 
  "longTermInvestments": 51325788, 
  "minorityInterest": 40660792, 
  "netBorrowings": 8437678784, 
  "netIncome": 3023726812, 
  "netIncomeBasic": 2906536847, 
  "netTangibleAssets": -63754950974, 
  "nextEarningsDate": "2020-07-31", 
  "operatingExpense": 14035195961, 
  "operatingIncome": 3637145624, 
  "otherAssets": 6892014027, 
  "otherCurrentAssets": 1806620928, 
  "otherCurrentLiabilities": 9488015113, 
  "otherFinancingCashFlows": null, 
  "otherIncomeExpenseNet": -27084497, 
  "otherLiabilities": 9526158452, 
  "pretaxIncome": 3661736432, 
  "propertyPlantEquipment": 21871586341, 
  "receivables": 4846605388, 
  "reportDate": "2020-03-26", 
  "researchAndDevelopment": null, 
  "retainedEarnings": 103574264650, 
  "sellingGeneralAndAdmin": null, 
  "shareholderEquity": 46084334878, 
  "shortTermInvestments": null, 
  "symbol": "pg", 
  "totalAssets": 121613706054, 
  "totalCurrentLiabilities": 33623112618, 
  "totalInvestingCashFlows": -755713886, 
  "totalLiabilities": 74796943536, 
  "totalRevenue": 17265210878, 
  "treasuryStock": 108340359095
}
```
**Query params:**
`api_key`: This is a key you set on the server when you deploy the containers. It is NOT your IEX key, those are stored in environment variables on the server.

## Components

It's built with:
* Docker & docker-compose
* Nginx
* Gunicorn
* Flask
* LetsEncrypt
* Postgres
* iexfinance

**Note: Tested on Ubuntu 18.04 hosted on digitalocean.**

Docker service | image
--- | ---
flask & gunicorn | `alpine:3.11.0`
nginx | `nginx:1.17.7-alpine`
postgres | `postgres:12-alpine`

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
# variable. Set it to something stronger in production
API_KEY=demo_key

# Postgres stuff. Replace with more meaningful values
POSTGRES_USER=quintana_pguser
POSTGRES_PASSWORD=quintana_pgpw
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=quintana_pgdb

# This project gets data from IEX and requires a token and version
IEX_TOKEN=Tsk_xxx
IEX_API_VERSION=iexcloud-sandbox
#IEX_API_VERSION=iexcloud-v1
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
sudo make dc-psql        # Run psql (requires the postgres container to be running)
```

Auto checks are running weekly to update the certificates. 

## Testing it

Locally:
* http://0.0.0.0:5000/
* http://0.0.0.0:5000/api/v1/stock/{symbol}/financials?api_key=demo_key

Remotely, simply use https and the domain name of your server::
* https://mydomain.com/api/v1/stock/{symbol}/financials?api_key=demo_key


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

