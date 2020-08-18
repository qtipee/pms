# PMS

To describe

## Setup

### Django

First, you need to add a file for your local settings in *src/pms/settings/local_settings.py*. This file is ignored by Git and allows you to overwrite some configurations for you development environment :

```
from pms.settings.common import *

SECRET_KEY = 'YOUR SECRET KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
```

Depending on your development database, you can also overwrite its configuration in this file.

After that, create a virtual environment :

```
python3 -m venv venv
source venv/bin/activate
```

Then, install the dependencies :

```
pip install -r requirements.txt
```

At last, apply the migrations and run the server :

```
cd src
python manage.py migrate
python manage.py runserver
```

### Nuxt

Go to the Nuxt project:

```
cd src/pms_nuxt
```

Once there, install the npm dependencies:

```
npm install
```

And then run the application

```
npm run dev
```
