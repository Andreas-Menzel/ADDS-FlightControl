# Setup

## Install Flight Control and Dependencies

Clone the repository:

```bash
git clone https://github.com/Andreas-Menzel/ADDS-FlightControl.git
cd ADDS-FlightControl
```

Make sure you have **Python 3** installed. Flight Control was tested with
Python 3.7 and higher.

Install the python dependencies:

```bash
cd code/
pip install -r requirements.txt
```

In the future a docker container will be created so that the installation and
starting of Flight Control gets even easier.

## Modify Config

Modify the `cchainlink_url` variable in `/code/functions_collection.py` to the
URL of your C-Chain Link instance.

```
cchainlink_url = 'http://adds-demo.an-men.de:8080/'
```

## Initialize database

This will set up the sqlite database.

**Note: If the database already exists, it will be overwritten**.

```bash
cd code/
flask --app flaskr init-db
```

## Start Flight Control

To start Flight Control, simply run the following:

```bash
cd code/
flask --app flaskr/ --debug run
```
