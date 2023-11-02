Python HTTP server for exposing Thorlabs Kensis API

adapted from https://github.com/rwalle/py_thorlabs_ctrl





# Install
1. clone project
```
git clone https://github.com/PychronLabsLLC/KinesisServer
```
2. change to KinesisServer folder
```
cd KinesisServer
```
3. create a python virtual environment
```
python -m venv .
```
4. Activate your python environment
```
source ./venv/bin/activate
```
5. install dependencies into the enviroment
```
pip install -r requirements.txt
```
6. launch the http server
```
gunicorn wsgi:app
```
