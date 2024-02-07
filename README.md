## Setup

Create virtual environment:
``` shell
python -m venv .venv
```

On new development terminal:

``` shell
source .venv/bin/activate
```


Install from `requirements.txt`:


``` shell
pip install -r requirements.txt
```

Set up the development database (note: this assumes you can connect as an admin
to your local postgres, and that `postgres` is a database that already exists;
if you connect in some other way, figure out how to run the three SQL commands
in tha file):

``` shell
psql postgres < init.sql

```


Run the app:

``` shell
flask run
```
