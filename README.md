# Installation
.env example to test in local
```
DB_USER=marketease
DB_PASSWORD=marketease
DB_NAME=marketease
DB_URL=postgresql://${DB_USER}:${DB_PASSWORD}@172.16.25.2:5432/${DB_NAME}
API_URL=172.0.0.1:8000
```

## marketease utility
There's a script that let you lauch/test/develop the application. It is basically a shortcut to run docker-compose commands.

To use it you can run it with `python marketease.py --help`.

### For Development
```sh
python marketease.py up
```

### For Production
```sh
python marketease.py --production up 
```

## docker-compose

Make sure you have Docker and docker-compose installed

### For Development
```sh
docker-compose up -d
```

### For Production
```sh
docker-compose -f docker-compose-production.yml up -d
```

## web

This template should help get you started developing with Vue 3 in Vite.

### Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

### Project Setup

```sh
cd web
npm install
```
#### Launch Vue.js
##### Compile and Hot-Reload for Development

```sh
npm run dev
```

##### Compile and Minify for Production

```sh
npm run build
```

## api

### Project Setup

#### Create virtual environment (Optional)

By using an environment all the packages installed will be isolated to avoid version conflicts
```sh
cd api
python3.10 -m venv ./venv
## Activate the venv
source ./venv/bin/activate  ## MacOS/Linux
env\Scripts\activate.bat    ## Windows
```

#### Install the dependencies

```sh
pip install -r requirements.txt
```

### Launch FastAPI

#### Hot-reload for Development

```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Deploy in Production

```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```
More info for the solutions to deploy FastAPI [here](https://fastapi.tiangolo.com/deployment/)

# Development
## api
### Add new depedencies
```sh
source ./venv/bin/activate
pip install [package]
pip freeze > requirements.txt
marketease build api
marketease up api
```

