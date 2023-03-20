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
    from flask import Flask,request
    from flask_cors import CORS
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask-cors"])
    from flask import Flask
    from flask_cors import CORS
    
    
app = Flask(__name__)

@app.route("/films")
def get_data():
    response = requests.get("http://localhost:8000/get_data/")
    data = response.json()
    print(data)
    return data

def log(msg,ID,err = False):
    if err:
        print(f"[Error][{ID}]: {msg}")
    else:
        print(f"[{ID}]: {msg}")
@app.route("/put/", methods=["OPTIONS", "PUT"])
def PutWithParams():
    print("we are in putttttt")
    vars = request.args
    string= "/?"
 
    for i in vars:
        string += f"{i}={vars[i]}&"
    string = string[:-1]
    print(string)
    headers = {'Content-Type': 'application/json'}
    response = requests.put(f"http://localhost:8000{string}",headers=headers)
    print("Done")
    try:
        data = response.json()
    except Exception as e:
        data = response.content
    print(data)
    return data

@app.route("/",methods=[ "POST", "PUT","PATCH","DELETE","OPTIONS"])
def PostWithParams1():
    if request.method == 'POST':
        # print("request is", request.args)
        data = request.get_data()
        print("data getting from post is ")
        print(data)
        post_data = data.decode('utf-8')
        if post_data:
            if post_data.startswith('----------------------------'):
                post_data = post_data.split('name=')[1:]
                print(f'{post_data} is the post data')
                newData = {}
                for i in range(0, len(post_data)):
                    key = post_data[i].split('\r\n\r\n')[0]
                    key = key.replace('"', '').replace("'", '')
                    value = post_data[i].split('\r\n\r\n')[1]
                    value = value.split('\r\n')[0]
                    newData[key] = value
                post_data = newData
            else:
                post_data = post_data.replace(
                    ' ', '').replace('"', '').replace("'", '')
                post_data = post_data.split("&")
                post_data = [i.replace("+", " ") for i in post_data]
                post_data = {i.split("=")[0]: i.split("=")[1]
                                for i in post_data}

        print("Final data e ", post_data)
        myString = "?"
        for key, value in post_data.items():
            myString += f"{key}={value}&"
        myString = myString[:-1]
        print(f"the final string is localhost:8000{myString}")
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"http://localhost:8000{myString}", headers=headers)
        return response.json()
    elif request.method == 'PUT':
        vars = request.args
        # generate the string
        string= "/?"
        # iterate thru vars
        for i in vars:
            string += f"{i}={vars[i]}&"
        string = string[:-1]
        # log("PUT request received", "PUT")
        log("PUT request received", "PUT")
        log(f"Vars: {string}", "PUT")
        response = requests.put(f"http://localhost:8000{string}")
        try:
            return response.json()
        except:
            return response.content
    elif request.method == 'PATCH':
        vars = request.args
        # generate the string
        string= "/?"
        # iterate thru vars
        for i in vars:
            string += f"{i}={vars[i]}&"
        string = string[:-1]
        # log("PUT request received", "PUT")
        log("PUT request received", "PATCH")
        log(f"Vars: {string}", "PATCH")
        response = requests.put(f"http://localhost:8000{string}")
        try:
            return response.json()
        except:
            return response.content
    elif request.method == 'DELETE':
        data = request.get_data()
        print("data getting from post is ")
        print(data)
        post_data = data.decode('utf-8')
        if post_data:
            if post_data.startswith('----------------------------'):
                post_data = post_data.split('name=')[1:]
                print(f'{post_data} is the post data')
                newData = {}
                for i in range(0, len(post_data)):
                    key = post_data[i].split('\r\n\r\n')[0]
                    key = key.replace('"', '').replace("'", '')
                    value = post_data[i].split('\r\n\r\n')[1]
                    value = value.split('\r\n')[0]
                    newData[key] = value
                post_data = newData
            else:
                post_data = post_data.replace(
                    ' ', '').replace('"', '').replace("'", '')
                post_data = post_data.split("&")
                post_data = [i.replace("+", " ") for i in post_data]
                post_data = {i.split("=")[0]: i.split("=")[1]
                                for i in post_data}
        print("Final data is ", post_data)
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(f"http://localhost:8000", headers=headers, data=data)
        try:
            return response.json()
        except:
            return response.content
    elif request.method == 'OPTIONS':
        data = request.get_data()
        print("data getting from post is ")
        print(data)
        vars = request.args
        # generate the string
        string= "/?"
        # iterate thru vars
        for i in vars:
            string += f"{i}={vars[i]}&"
        string = string[:-1]
        log(f'OPTIONS request received {request.args}', 'OPTIONS')  
        post_data = data.decode('utf-8')
        if post_data:
            if post_data.startswith('----------------------------'):
                post_data = post_data.split('name=')[1:]
                print(f'{post_data} is the post data')
                newData = {}
                for i in range(0, len(post_data)):
                    key = post_data[i].split('\r\n\r\n')[0]
                    key = key.replace('"', '').replace("'", '')
                    value = post_data[i].split('\r\n\r\n')[1]
                    value = value.split('\r\n')[0]
                    newData[key] = value
                post_data = newData
            else:
                post_data = post_data.replace(
                    ' ', '').replace('"', '').replace("'", '')
                post_data = post_data.split("&")
                post_data = [i.replace("+", " ") for i in post_data]
                post_data = {i.split("=")[0]: i.split("=")[1]
                                for i in post_data}
        if post_data!='':
            print("Final data is ", post_data)
            headers = {'Content-Type': 'application/json'}
            response = requests.delete(f"http://localhost:8000", headers=headers, data=data)
        else:
            print("Final data is ", post_data)
            headers = {'Content-Type': 'application/json'}
            response = requests.delete(f"http://localhost:8000{string}")
        try:
            return response.json()
        except:
            return response.content
@app.route("/post/",methods=["POST"])
def PostWithParams():
    print("we are in post2")
    vars = request.args
    string= "/?"
 
    for i in vars:
        string += f"{i}={vars[i]}&"
    string = string[:-1]
    print(string)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"http://localhost:8000{string}",headers=headers)
    print("Done")
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
    # response.headers.add('Access-Control-Allow-Origin', '*')
    print('the response is',response)
    data = response.content
    print(data)
    return data

if __name__ == "__main__":
    CORS(app)
    app.run(debug=True)