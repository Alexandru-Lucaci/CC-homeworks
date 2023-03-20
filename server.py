from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import urllib
import json
import subprocess
try:
    import regex as re
except:
    subprocess.run(["pip", "install", "regex"])
    import regex as re
try:
    from bs4 import BeautifulSoup
except:
    subprocess.run(["pip", "install", "bs4"])
    from bs4 import BeautifulSoup
try:
    import requests
except:
    subprocess.run(["pip", "install", "requests"])
    import requests
try:
    import tqdm
except:
    subprocess.run(["pip", "install", "tqdm"])
    import tqdm
import cgi

# HOST = "192.168.100.34"
HOST = "localhost"
PORT = 8000
HTML_FILE = "index.html"


def get_header():
    # get the header
    with open("index.html", "r") as file:
        soup = BeautifulSoup(file, "html.parser")
    header = soup.find("thead")
    header = [th.text for th in header.find_all("th")]
    header = header[1:]
    header = [th.lower().split(" ")[0] for th in header]
    return header


def checkAlreadyExists(dict_data_all: dict, dict_data: dict) -> bool:
    for key in dict_data_all.keys():
        if key != '#':
            print(key, dict_data_all[key].keys())
            for params in dict_data_all[key].keys():
                ok = True
                if dict_data_all[key][params] != dict_data[params]:
                    ok = False
                if ok == True:
                    return True
    return False


def get_data():
    """Get the data from the index.html file and return a dictionary with the data

    By data i'm refering to the table in the html file
    :return: dictionary with the data"""

    # get the header
    header = get_header()
    # header will contains the header of the table Name = The name of the film, Type = The type of the film, Film = FilmGenra

    with open("index.html", "r") as file:
        soup = BeautifulSoup(file, "html.parser")

    # get the data and make a dictionary with the data
    result = {}
    data = soup.find_all("tr")
    for row in data:
        th = row.find("th")
        aux = row.find_all("td")
        aux_dict = {}
        if (len(aux) == len(header)):
            for i in range(len(header)):
                aux_dict[header[i].lower()] = aux[i].text
        film = aux_dict
        result[th.text] = film

    return result


# print(get_data())
def maxId():
    data = get_data()
    id = 0
    for key in data.keys():
        if key != "#":
            id = int(key)
    return id+1


def check_id_exsits(id):
    print(f'the id is {id}')
    data = get_data()
    id = int(id)
    return len([i for i in data.keys() if i != '#' if int(i) == id > 0]) > 0


class NeuralHttp(BaseHTTPRequestHandler):
    def writeResponse(self, codeResponse, message, contentType):
        self.send_response(codeResponse)
        self.send_header('Content-type', contentType)
        self.end_headers()
        self.wfile.write(bytes(message, 'utf-8'))

    def writeResponse2(self, codeResponse, message, contentType):
        self.send_response(codeResponse)
        self.send_header('Content-type', contentType)
        self.end_headers()
        self.wfile.write(bytes(str(message), 'utf-8'))

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html" or self.path == "/server.py":
            self.path = f"/{HTML_FILE}"
            try:
                file_to_open = open(self.path[1:]).read()
                self.writeResponse(200, file_to_open, 'text/html')
            except:
                # create a response json
                response = {
                    "status": 404,
                    "message": "File not found",
                    "date": time.ctime(time.time())
                }
                self.writeResponse(404, json.dumps(response), 'application/json')

        elif self.path == "/get_data" or self.path == "/get_data/" or self.path == "/films":

            data = get_data()

            self.writeResponse(200, json.dumps(data), 'application/json')
        elif re.match(r"/\d+/\w+", self.path):
            print('path starts ', self.path)
            id = self.path.split('/')[1]
            if (check_id_exsits(id)):
                data = get_data()
                path = self.path[1:].split('/')
                path = path[1].split('&')
                key_to_print = []
                print('Key to print: ', data[id].keys())
                for i in range(0, len(path)):
                    if path[i] in data[id].keys():
                        # data = data[id][path[i]]
                        print('a match')
                        key_to_print.append(path[i])

                if len(key_to_print) == 0:
                    response = {
                        "status": 400,
                        "message": "Params didn't match",
                        "date": time.ctime(time.time())
                    }
                    self.writeResponse(400, response, 'application/json')
                else:
                    data = {key: data[id][key] for key in key_to_print}
                    self.writeResponse(200, json.dumps(
                        data), 'application/json')

            else:
                response = {
                    "status": 400,
                    "message": "id does not exist",
                    "date": time.ctime(time.time())
                }
                self.writeResponse(400, response, 'application/json')
        elif re.match(r"/\d+", self.path):
            print('matched')
            print('path starts ', self.path)
            id = self.path.split('/')[1]
            if (check_id_exsits(id)):
                print('id exists')
                data = get_data()
                print(data[id])
                info = data[id]
                print(info)
                self.writeResponse(200,json.dumps(info), 'application/json') 
                    
            else:
                response = {
                    "status": 400,
                    "message": "id does not exist",
                    "date": time.ctime(time.time())
                }
                self.writeResponse(400, json.dump(response), 'application/json')

        elif self.path == "/favicon.ico":
            pass
        else:
            if (self.path.startswith('/get/')):

                print("Path is ", self.path)
                params = self.path.split("?")[1].split("&")
                params = [i.replace("%20", " ") for i in params]
                params = {param.split("=")[0]: param.split("=")[
                    1] for param in params}
                print(params)
                header = [i.lower() for i in get_header()]
                data = get_data()
                finded = False
                for param in tqdm.tqdm(params.keys()):
                    if (param.lower() in header):
                        print("Param is ", param)
                        print(data)
                        result = []
                        print(params[param])
                        for film in data.keys():
                            item = [j for j in data[film].items()
                                    if param.lower() in j]
                            # print(type(item))
                            for tupla in item:
                                if tupla[1] == params[param]:
                                    finded = True
                                    result.append(data[film])
                                    # self.writeResponse(200, json.dumps(
                                    #     data[film]), 'application/json')
                                    # self.wfile.write(
                                    #     bytes(f"{data[film]}", 'utf-8'))
                        self.writeResponse(200, json.dumps(
                            result), 'application/json')
                    else:
                        print('could not find param')
                if (not finded):
                    response = {
                    "status": 400,
                    "message": "Could not find the film",
                    "date": time.ctime(time.time())
                    }
                    self.writeResponse(400, json.dumps(response), 'application/json')
                    # self.wfile.write(bytes("Could not find the film", 'utf-8'))
                # else:
                #     time.sleep(5)
                #     self.path = "/"
                #     print(self.path)
                #     self.do_GET()
            else:
                # false - there is a tag that i don't know
                self.end_headers()
                self.wfile.write(
                    bytes("Page not found, i will go to index.html in 5 seconds", 'utf-8'))
                for i in tqdm.tqdm(range(5)):
                    time.sleep(1)
                self.wfile.write(bytes("Going to index.html", 'utf-8'))
                time.sleep(1)

                self.path = f"/"
                self.do_GET()
                # delete the first write
                # self.send_response(200)
                # try:
                #     file_to_open = open(self.path[1:]).read()
                #     self.wfile.write(bytes(file_to_open, 'utf-8'))
                # except:
                #     self.wfile.write(bytes("File not found", 'utf-8'))

    def do_POST(self):
        # self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself

        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')

        print('Print the post data ', post_data)
        print(self.path)
        if post_data == '':
            post_data = self.path.split('?')[1]

        print('final post data ', post_data)
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

            print("Final datae ", post_data)

            headers = get_header()

            print(headers)
            data = get_data()
    # "name": "The Godfather", "type": "Crime", "film": "Drama"
            existed = False
            # check if the checkbox is checked
            if post_data.get('checked') is not None:
                # check if the film already exists
                if (checkAlreadyExists(data, post_data) and post_data["checked"]):

                    message = {"message": "Film already exists",
                               "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                    # self.wfile.write(bytes(str(message), 'utf-8'))
                    self.writeResponse(409, json.dumps(message), 'application/json')
                    # self.do_GET()
                    existed = True
            if not existed:
                soup = BeautifulSoup(open("index.html"), "html.parser")
                table = soup.find("tbody")
                # add to the end the new entry
                table.append('<tr>')
                table.append(
                    f"""
                    <th scope="row">{maxId()}</th>
                    <td>{post_data["name"]}</td>
                    <td>{post_data["type"]}</td>
                    <td>{post_data["film"]}</td>
                    </tr>""")

                # print(soup.prettify())
                with open("index.html", "w") as file:
                    file.write(str(soup).replace(
                        "&lt;", "<").replace("&gt;", ">"))
                message = {"message": "Film added",
                           "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                # self.wfile.write(bytes(str(message), 'utf-8'))
                self.writeResponse(201, json.dumps(
                    message), 'application/json')
                # self.do_GET()
        else:
            print(' i am here')

    def do_PUT(self):
        # "name='alex'"
        # id='1'

        # self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself

        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')

        print(post_data)
        if post_data == '':
            post_data = self.path.split('?')[1]
        post_data = post_data.replace(
            ' ', '').replace('"', '').replace("'", '')
        post_data = post_data.split("&")
        post_data = [i.replace("+", " ") for i in post_data]
        post_data = {i.split("=")[0]: i.split("=")[1] for i in post_data}

        print(post_data)

        headers = get_header()
        print(headers)
        data = get_data()

        # check if the first parameter is id
        if post_data.get('id') is not None:
            print('search by id')

            print('data from id', data[post_data['id']])

            if data[post_data['id']] is not None:
                print('found')
                # update the film
                print(data)
                # check if the newname is not empty
                changed = {}
                if post_data.get('newname') is not None and post_data['newname'] != '':

                    changed['name'] = post_data['newname']
                else:
                    changed['name'] = data[post_data['id']]['name']
                # check if the newtype is not empty
                if post_data.get('newtype') is not None and post_data['newtype'] != '':
                    changed['type'] = post_data['newtype']
                else:
                    changed['type'] = data[post_data['id']]['type']

                # check if the newfilm is not empty
                if post_data.get('newfilm') is not None and post_data['newfilm'] != '':
                    changed['film'] = post_data['newfilm']
                else:
                    changed['film'] = data[post_data['id']]['film']

                # update the html file
                soup = BeautifulSoup(open("index.html"), "html.parser")
                table = soup.find("tbody")
                # add to the end the new entry
                print(changed)
                # iterate through the table
                for i in table.find_all('tr'):
                    # check if the id is the same
                    if i.find('th').text == post_data['id']:

                        # create a tag with the new values
                        new_tag = soup.new_tag("td")
                        new_tag.string = changed['name']
                        # replace the old tag with the new one
                        i.find_all('td')[0].replaceWith(new_tag)
                        new_tag = soup.new_tag("td")
                        new_tag.string = changed['type']
                        i.find_all('td')[1].replaceWith(new_tag)
                        # i.find_all('td')[1].text.replaceWith(changed['type'])
                        new_tag = soup.new_tag("td")
                        new_tag.string = changed['film']
                        i.find_all('td')[2].replaceWith(new_tag)

                        # i.find_all('td')[2].text.replaceWith(changed['film'])
                        break

                with open("index.html", "w") as file:
                    file.write(str(soup).replace(
                        "&lt;", "<").replace("&gt;", ">"))
                message = {"message": "Film updated",
                           "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                # self.wfile.write(bytes(str(message), 'utf-8'))
                self.writeResponse(200, json.dumps(
                    message), 'application/json')
                # print(soup.prettify())
                self.path = '/index.html'
                # self.do_GET()
            else:
                print('not found')
                message = {"message": "Film not found",
                           "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                # self.wfile.write(bytes(str(message), 'utf-8'))
                self.writeResponse(404, json.dumps(
                    message), 'application/json')
                # self.do_GET()
        elif post_data.get('name') is not None:
            print('search by name')
            # search by name
            found = False
            print(data)
            for i in data:
                i = data[i]
                print(i)
                if (i != {}):
                    if i['name'] == post_data['name']:
                        print('found')
                        found = True
                        # update the film
                        print(data)
                        # check if the newname is not empty
                        changed = {}
                        if post_data.get('newname') is not None and post_data['newname'] != '':

                            changed['name'] = post_data['newname']
                        else:
                            changed['name'] = i['name']
                        # check if the newtype is not empty
                        if post_data.get('newtype') is not None and post_data['newtype'] != '':
                            changed['type'] = post_data['newtype']
                        else:
                            changed['type'] = i['type']

                        # check if the newfilm is not empty
                        if post_data.get('newfilm') is not None and post_data['newfilm'] != '':
                            changed['film'] = post_data['newfilm']
                        else:
                            changed['film'] = i['film']

                        # update the html file
                        soup = BeautifulSoup(open("index.html"), "html.parser")
                        table = soup.find("tbody")
                        # add to the end the new entry
                        print(changed)
                        # iterate through the table
                        oneFound = False
                        for j in table.find_all('tr'):
                            if oneFound == False:
                                # check if the id is the same
                                if j.find('td').text == str(i['name']):
                                    oneFound = True
                                    print('found --- i m here ')
                                    # create a tag with the new values
                                    new_tag = soup.new_tag("td")
                                    new_tag.string = changed['name']
                                    # replace the old tag with the new one
                                    j.find_all('td')[0].replaceWith(new_tag)
                                    new_tag = soup.new_tag("td")
                                    new_tag.string = changed['type']
                                    j.find_all('td')[1].replaceWith(new_tag)
                                    # i.find_all('td')[1].text.replaceWith(changed['type'])
                                    new_tag = soup.new_tag("td")
                                    new_tag.string = changed['film']
                                    j.find_all('td')[2].replaceWith(new_tag)

                                    # i.find_all('td')[2].text.replaceWith(changed['film'])
                                    break

                        with open("index.html", "w") as file:
                            file.write(str(soup).replace(
                                "&lt;", "<").replace("&gt;", ">"))
                        message = {"message": "Film updated",
                                   "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                        # self.wfile.write(bytes(str(message), 'utf-8'))
                        self.writeResponse(200, json.dumps(
                            message), 'application/json')
                        self.path = '/index.html'
                        # self.do_GET()
                if not found:
                    print('not found')
                    message = {"message": "Film not found",
                               "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                    # self.wfile.write(bytes(str(message), 'utf-8'))
                    # self.do_GET()
                    self.writeResponse(404, json.dumps(
                        message), 'application/json')

    def do_PATCH(self):
        # "name='alex'"
        # id='1'

        # self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself

        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')

        print(post_data)
        if post_data == '':
            post_data = self.path.split('?')[1]
        post_data = post_data.replace(
            ' ', '').replace('"', '').replace("'", '')
        post_data = post_data.split("&")
        post_data = [i.replace("+", " ") for i in post_data]
        post_data = {i.split("=")[0]: i.split("=")[1] for i in post_data}

        print(post_data)

        headers = get_header()
        print(headers)
        data = get_data()

        # check if the first parameter is id
        if post_data.get('id') is not None:
            print('search by id')

            print('data from id', data[post_data['id']])

            if data[post_data['id']] is not None:
                print('found')
                # update the film
                print(data)
                # check if the newname is not empty
                changed = {}
                if post_data.get('newname') is not None and post_data['newname'] != '':

                    changed['name'] = post_data['newname']
                else:
                    changed['name'] = data[post_data['id']]['name']
                # check if the newtype is not empty
                if post_data.get('newtype') is not None and post_data['newtype'] != '':
                    changed['type'] = post_data['newtype']
                else:
                    changed['type'] = data[post_data['id']]['type']

                # check if the newfilm is not empty
                if post_data.get('newfilm') is not None and post_data['newfilm'] != '':
                    changed['film'] = post_data['newfilm']
                else:
                    changed['film'] = data[post_data['id']]['film']

                # update the html file
                soup = BeautifulSoup(open("index.html"), "html.parser")
                table = soup.find("tbody")
                # add to the end the new entry
                print(changed)
                # iterate through the table
                for i in table.find_all('tr'):
                    # check if the id is the same
                    if i.find('th').text == post_data['id']:

                        # create a tag with the new values
                        new_tag = soup.new_tag("td")
                        new_tag.string = changed['name']
                        # replace the old tag with the new one
                        i.find_all('td')[0].replaceWith(new_tag)
                        new_tag = soup.new_tag("td")
                        new_tag.string = changed['type']
                        i.find_all('td')[1].replaceWith(new_tag)
                        # i.find_all('td')[1].text.replaceWith(changed['type'])
                        new_tag = soup.new_tag("td")
                        new_tag.string = changed['film']
                        i.find_all('td')[2].replaceWith(new_tag)

                        # i.find_all('td')[2].text.replaceWith(changed['film'])
                        break

                with open("index.html", "w") as file:
                    file.write(str(soup).replace(
                        "&lt;", "<").replace("&gt;", ">"))
                message = {"message": "Film updated",
                           "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                # self.wfile.write(bytes(str(message), 'utf-8'))
                self.writeResponse(200, json.dumps(
                    message), 'application/json')
                print(soup.prettify())
                self.path = '/index.html'
                # self.do_GET()
            else:
                print('not found')
                message = {"message": "Film not found",
                           "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                # self.wfile.write(bytes(str(message), 'utf-8'))
                self.writeResponse(404, json.dumps(
                    message), 'application/json')
                # self.do_GET()
        elif post_data.get('name') is not None:
            print('search by name')
            # search by name
            found = False
            print(data)
            for i in data:
                i = data[i]
                print(i)
                if (i != {}):
                    if i['name'] == post_data['name']:
                        print('found')
                        found = True
                        # update the film
                        print(data)
                        # check if the newname is not empty
                        changed = {}
                        if post_data.get('newname') is not None and post_data['newname'] != '':

                            changed['name'] = post_data['newname']
                        else:
                            changed['name'] = i['name']
                        # check if the newtype is not empty
                        if post_data.get('newtype') is not None and post_data['newtype'] != '':
                            changed['type'] = post_data['newtype']
                        else:
                            changed['type'] = i['type']

                        # check if the newfilm is not empty
                        if post_data.get('newfilm') is not None and post_data['newfilm'] != '':
                            changed['film'] = post_data['newfilm']
                        else:
                            changed['film'] = i['film']

                        # update the html file
                        soup = BeautifulSoup(open("index.html"), "html.parser")
                        table = soup.find("tbody")
                        # add to the end the new entry
                        print(changed)
                        # iterate through the table
                        oneFound = False
                        for j in table.find_all('tr'):
                            if oneFound == False:
                                # check if the id is the same
                                if j.find('td').text == str(i['name']):
                                    oneFound = True
                                    print('found --- i m here ')
                                    # create a tag with the new values
                                    new_tag = soup.new_tag("td")
                                    new_tag.string = changed['name']
                                    # replace the old tag with the new one
                                    j.find_all('td')[0].replaceWith(new_tag)
                                    new_tag = soup.new_tag("td")
                                    new_tag.string = changed['type']
                                    j.find_all('td')[1].replaceWith(new_tag)
                                    # i.find_all('td')[1].text.replaceWith(changed['type'])
                                    new_tag = soup.new_tag("td")
                                    new_tag.string = changed['film']
                                    j.find_all('td')[2].replaceWith(new_tag)

                                    # i.find_all('td')[2].text.replaceWith(changed['film'])
                                    break

                        with open("index.html", "w") as file:
                            file.write(str(soup).replace(
                                "&lt;", "<").replace("&gt;", ">"))
                        message = {"message": "Film updated",
                                   "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                        # self.wfile.write(bytes(str(message), 'utf-8'))
                        self.writeResponse(200, json.dumps(
                            message), 'application/json')
                        self.path = '/index.html'
                        # self.do_GET()
                if not found:
                    print('not found')
                    message = {"message": "Film not found",
                               "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                    # self.wfile.write(bytes(str(message), 'utf-8'))
                    # self.do_GET()
                    self.writeResponse(404, json.dumps(
                        message), 'application/json')

    def do_PUT(self):
        # "name='alex'"
        # id='1'

        # self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()
        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself

        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')

        print(post_data)
        if post_data == '':
            post_data = self.path.split('?')[1]
        post_data = post_data.replace(
            ' ', '').replace('"', '').replace("'", '')
        post_data = post_data.split("&")
        post_data = [i.replace("+", " ") for i in post_data]
        post_data = {i.split("=")[0]: i.split("=")[1] for i in post_data}

        print(post_data)

        headers = get_header()
        print(headers)
        data = get_data()

        # check if the first parameter is id
        if post_data.get('id') is not None:
            print('search by id')
            try:
                print('data from id', data[post_data['id']])
            except KeyError as e :
                print('not found')
                message = {"message": "Film not found",
                           "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                # self.wfile.write(bytes(str(message), 'utf-8'))
                self.writeResponse(404, json.dumps(
                    message), 'application/json')
                
            if data[post_data['id']] is not None:
                print('found')
                # update the film
                print(data)
                # check if the newname is not empty
                changed = {}
                if post_data.get('newname') is not None and post_data['newname'] != '':

                    changed['name'] = post_data['newname']
                else:
                    changed['name'] = data[post_data['id']]['name']
                # check if the newtype is not empty
                if post_data.get('newtype') is not None and post_data['newtype'] != '':
                    changed['type'] = post_data['newtype']
                else:
                    changed['type'] = data[post_data['id']]['type']

                # check if the newfilm is not empty
                if post_data.get('newfilm') is not None and post_data['newfilm'] != '':
                    changed['film'] = post_data['newfilm']
                else:
                    changed['film'] = data[post_data['id']]['film']

                # update the html file
                soup = BeautifulSoup(open("index.html"), "html.parser")
                table = soup.find("tbody")
                # add to the end the new entry
                print(changed)
                # iterate through the table
                for i in table.find_all('tr'):
                    # check if the id is the same
                    if i.find('th').text == post_data['id']:

                        # create a tag with the new values
                        new_tag = soup.new_tag("td")
                        new_tag.string = changed['name']
                        # replace the old tag with the new one
                        i.find_all('td')[0].replaceWith(new_tag)
                        new_tag = soup.new_tag("td")
                        new_tag.string = changed['type']
                        i.find_all('td')[1].replaceWith(new_tag)
                        # i.find_all('td')[1].text.replaceWith(changed['type'])
                        new_tag = soup.new_tag("td")
                        new_tag.string = changed['film']
                        i.find_all('td')[2].replaceWith(new_tag)

                        # i.find_all('td')[2].text.replaceWith(changed['film'])
                        break

                with open("index.html", "w") as file:
                    file.write(str(soup).replace(
                        "&lt;", "<").replace("&gt;", ">"))
                message = {"message": "Film updated",
                           "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                # self.wfile.write(bytes(str(message), 'utf-8'))
                self.writeResponse(200, json.dumps(
                    message), 'application/json')
                print(soup.prettify())
                self.path = '/index.html'
                # self.do_GET()
            else:
                print('not found')
                message = {"message": "Film not found",
                           "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                # self.wfile.write(bytes(str(message), 'utf-8'))
                self.writeResponse(404, json.dumps(
                    message), 'application/json')
                # self.do_GET()
        elif post_data.get('name') is not None:
            print('search by name')
            # search by name
            found = False
            print(data)
            for i in data:
                i = data[i]
                print(i)
                if (i != {}):
                    if i['name'] == post_data['name']:
                        print('found')
                        found = True
                        # update the film
                        print(data)
                        # check if the newname is not empty
                        changed = {}
                        if post_data.get('newname') is not None and post_data['newname'] != '':

                            changed['name'] = post_data['newname']
                        else:
                            changed['name'] = i['name']
                        # check if the newtype is not empty
                        if post_data.get('newtype') is not None and post_data['newtype'] != '':
                            changed['type'] = post_data['newtype']
                        else:
                            changed['type'] = i['type']

                        # check if the newfilm is not empty
                        if post_data.get('newfilm') is not None and post_data['newfilm'] != '':
                            changed['film'] = post_data['newfilm']
                        else:
                            changed['film'] = i['film']

                        # update the html file
                        soup = BeautifulSoup(open("index.html"), "html.parser")
                        table = soup.find("tbody")
                        # add to the end the new entry
                        print(changed)
                        # iterate through the table
                        oneFound = False
                        for j in table.find_all('tr'):
                            if oneFound == False:
                                # check if the id is the same
                                if j.find('td').text == str(i['name']):
                                    oneFound = True
                                    print('found --- i m here ')
                                    # create a tag with the new values
                                    new_tag = soup.new_tag("td")
                                    new_tag.string = changed['name']
                                    # replace the old tag with the new one
                                    j.find_all('td')[0].replaceWith(new_tag)
                                    new_tag = soup.new_tag("td")
                                    new_tag.string = changed['type']
                                    j.find_all('td')[1].replaceWith(new_tag)
                                    # i.find_all('td')[1].text.replaceWith(changed['type'])
                                    new_tag = soup.new_tag("td")
                                    new_tag.string = changed['film']
                                    j.find_all('td')[2].replaceWith(new_tag)

                                    # i.find_all('td')[2].text.replaceWith(changed['film'])
                                    break

                        with open("index.html", "w") as file:
                            file.write(str(soup).replace(
                                "&lt;", "<").replace("&gt;", ">"))
                        message = {"message": "Film updated",
                                   "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                        # self.wfile.write(bytes(str(message), 'utf-8'))
                        self.writeResponse(200, json.dumps(
                            message), 'application/json')
                        self.path = '/index.html'
                        # self.do_GET()
                if not found:
                    print('not found')
                    message = {"message": "Film not found",
                               "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                    # self.wfile.write(bytes(str(message), 'utf-8'))
                    # self.do_GET()
                    self.writeResponse(404, json.dumps(
                        message), 'application/json')

    def do_DELETE(self):
        # self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()

        # <--- Gets the size of data
        content_length = int(self.headers['Content-Length'])
        # <--- Gets the data itself

        post_data = self.rfile.read(content_length)
        post_data = post_data.decode('utf-8')

        print('the post_data is:')
        print(post_data)
        if post_data == '':
            post_data = self.path.split('?')[1]

        print('final post data ', post_data)
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

        print('the post_data is:')
        print(post_data)
        headers = get_header()
        print(headers)
        data = get_data()
        print(data)
        if post_data.get('id') is not None:
            try:
                if data[post_data['id']] is not None:
                    soup = BeautifulSoup(open("index.html"), "html.parser")
                    table = soup.find("tbody")
                    # iterate through the table
                    for i in table.find_all('tr'):
                        # check if the id is the same
                        if i.find('th').text == post_data['id']:
                            i.decompose()
                            break

                    with open("index.html", "w") as file:
                        file.write(str(soup).replace(
                            "&lt;", "<").replace("&gt;", ">"))
                        message = {"message": "Film deleted",
                                "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                        # self.wfile.write(bytes(str(message), 'utf-8'))
                        self.path = '/index.html'
                        self.writeResponse(200, json.dumps(message), 'application/json')
                        # self.do_GET()
                else:
                    print('not found')
                    message = {"message": "Film not found",
                            "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                    # self.wfile.write(bytes(str(message), 'utf-8'))
                    self.writeResponse(404, json.dumps(message), 'application/json')
                    # self.do_GET()
            except KeyError:
                print('not found')
                message = {"message": "Film not found",
                        "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                # self.wfile.write(bytes(str(message), 'utf-8'))
                self.writeResponse(404, json.dumps(message), 'application/json')
        elif post_data.get('name') is not None:
            for i in data:
                i = data[i]
                print(i)
                if (i != {}):
                    if i['name'] == post_data['name']:
                        print('found')
                        found = True

                        # update the html file
                        soup = BeautifulSoup(open("index.html"), "html.parser")
                        table = soup.find("tbody")
                        # iterate through the table
                        oneFound = False
                        for j in table.find_all('tr'):
                            if oneFound == False:
                                # check if the id is the same
                                if j.find('td').text == str(i['name']):
                                    oneFound = True
                                    j.decompose()
                                    break

                        with open("index.html", "w") as file:
                            file.write(str(soup).replace(
                                "&lt;", "<").replace("&gt;", ">"))
                        message = {"message": "Film deleted",
                                   "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
                        # self.wfile.write(bytes(str(message), 'utf-8'))
                        self.writeResponse2(200, json.dumps(message), 'application/json')
                        self.path = '/index.html'
                        # self.do_GET()
        else:
            message = {"message": "Param not found",
                       "data": f"{time.strftime('%Y-%m-%d %H: %M: %S', time.localtime(time.time()))}"}
            # self.wfile.write(bytes(str(message), 'utf-8'))
            self.writeResponse(404, message, 'application/json')
            # self.do_GET()


server = HTTPServer((HOST, PORT), NeuralHttp)
print("Server started at http://%s:%s" % (HOST, PORT))
server.serve_forever()
server.server_close()
