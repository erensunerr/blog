from app import app
import json, os, threading, hashlib, time
from flask import send_from_directory, render_template, request


BLOG_FILE_LOCATION = "blog.txt"
USER_FILE_LOCATION = "user_info.txt"

def update_blog():
    global BLOG_FILE_LOCATION, USER_FILE_LOCATION, USERNAME, PASSWORD, POSTS
    data = open(BLOG_FILE_LOCATION, 'r').read()
    POSTS = json.loads(data.replace("\n", " ").replace("\t", " "))
    USERNAME, PASSWORD = open(USER_FILE_LOCATION, 'r').read().split('\n')[:-1]
    print(USERNAME, PASSWORD)


update_blog()

# Serve React App
@app.route('/')
def serve():
    global POSTS
    return render_template("user_blog/index.html", tab_title=POSTS['title'])

@app.route('/admin_panel')
def administrate():
    return render_template("admin_panel/index.html")
# SECURE API METHODS START
@app.route('/api/<username>/<password>/authenticate')
def authenticate(username, password):
    global USERNAME, PASSWORD
    username = username.upper()
    password = password.upper()
    if username == USERNAME and password == PASSWORD:
        response = app.response_class(
            status=200
        )
    else:
        response = app.response_class(
            status=400
        )

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/<username>/<password>/update_blog')
def use_blog_updater(username, password):
    global USERNAME, PASSWORD
    username = username.upper()
    password = password.upper()
    if username == USERNAME and password == PASSWORD:
        update_blog()
        response = app.response_class(
            status=200
        )
    else:
        response = app.response_class(
            status=400
        )

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

@app.route('/api/<username>/<password>/add_entry/<title>', methods=["GET", "POST", "OPTIONS"])
def add_entry(username, password, title):
    if request.method == "OPTIONS":
        response = app.response_class(
            status=200
        )
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'content-type, *')
        return response
    global USERNAME, PASSWORD
    username = username.upper()
    password = password.upper()
    print("inside add_entry")
    if username == USERNAME and password == PASSWORD:
        elements = request.get_json()
        global BLOG_FILE_LOCATION
        file_read = open(BLOG_FILE_LOCATION, 'r')
        prev_data = file_read.read()
        file_read.close()
        print(json.dumps(elements))
        prev_data_json = json.loads(prev_data.replace("\n", " ").replace("\t", " "))
        print(prev_data_json)
        print(prev_data_json['posts'])
        print(prev_data_json)
        posts = prev_data_json['posts']
        posts += [
        {"title": title,
        'sections': elements}
        ]
        prev_data_json['posts'] = posts
        print(prev_data_json)
        file_write = open(BLOG_FILE_LOCATION, 'w')
        file_write.write(json.dumps(prev_data_json))
        file_write.close()
        response = app.response_class(
            status=200
        )

    else:
        response = app.response_class(
            status=400
        )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/api/<username>/<password>/del_entry/<title>')
def del_entry(username, password, title):
    global USERNAME, PASSWORD
    username = username.upper()
    password = password.upper()
    if username == USERNAME and password == PASSWORD:
        global BLOG_FILE_LOCATION, USER_FILE_LOCATION
        file = open(BLOG_FILE_LOCATION, 'r+')
        prev_data = file.read()
        prev_data_json = json.loads(prev_data.replace("\n", " ").replace("\t", " "))
        prev_data_json = ['posts'].remove(prev_data_json['posts'][title])
        file.write(json.dumps(prev_data_json))
        file.close()



# GENERAL API METHODS START

@app.route('/api/get_post_list')
def get_post_list():
    global POSTS
    P = POSTS
    q = []
    for post in P['posts']:
        q += [post['title']]

    response = app.response_class(
        response=json.dumps(q),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/get_post/<title>')
def get_post(title):
    global POSTS
    P = POSTS
    for post in P['posts']:
        if post['title'] == title:
            data = post
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/get_info')
def get_info():
    global POSTS
    P = POSTS
    q = {}
    q['title'] = P['title']
    q['author'] = P['author']

    response = app.response_class(
        response=json.dumps(q),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/<username>/<password>')
def f():
    pass
