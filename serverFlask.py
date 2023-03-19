import subprocess
import os
import sys
try:
    import requests
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
# pyenv exec python -m venv .venv
# print(os.path.dirname(sys.executable))
try:
    from flask import Flask
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask
    
    
app = Flask(__name__)

@app.route("/films")
def get_data():
    response = requests.get("http://localhost:8000/get_data/")
    data = response.json()
    print(data)
    return data
@app.route("/")
def getFirst():
    response = requests.get("http://localhost:8000/")
    data = response.json()
    print(data)
    return data
@app.route("/<id>")
def getFilmByID(id):
    response = requests.get(f"http://localhost:8000/{id}")
    data = response.json()
    print(data)
    return data
@app.route("/<id>/<name>")
def getFilterdID(id,name):
    response = requests.get(f"http://localhost:8000/{id}/{name}")
    data = response.json()
    print(data)
    return data
@app.route("/get/<key>=<value>")
def getType(key,value):
    print("our values are", key,value)
    response = requests.get(f"http://localhost:8000/get/?{key}={value}")
    
    print('the response is',response)
    data = response.content
    print(data)
    return data
# @app.route("/", methods=['POST'])
# def doPut():
    
if __name__ == "__main__":
    app.run(debug=True)