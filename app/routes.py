from app import app
import json, os, threading, hashlib, time
from flask import send_from_directory, render_template, request
import hashlib

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
    print(username, password)
    print(USERNAME, PASSWORD)
    username = hashlib.md5(username.encode('utf-8')).hexdigest()
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    print(username, password)
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
    username = hashlib.md5(username.encode('utf-8')).hexdigest()
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
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
    username = hashlib.md5(username.encode('utf-8')).hexdigest()
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
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
            {
                "title": title,
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


@app.route('/api/<username>/<password>/del_post/<title>')
def del_entry(username, password, title):
    global USERNAME, PASSWORD
    username = hashlib.md5(username.encode('utf-8')).hexdigest()
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    if username == USERNAME and password == PASSWORD:
        global BLOG_FILE_LOCATION, USER_FILE_LOCATION
        read_file = open(BLOG_FILE_LOCATION, 'r')
        prev_data = read_file.read()
        read_file.close()
        print(prev_data)
        prev_data_json = json.loads(prev_data.replace("\n", " ").replace("\t", " "))
        print(prev_data_json['posts'])
        posts = prev_data_json['posts']
        for n in range(len(posts) - 1):
            print(posts[n])
            if posts[n]['title'] == title:
                posts = posts[:n] + posts[n+1:]
                print(posts)
        prev_data_json['posts'] = posts
        write_file = open(BLOG_FILE_LOCATION, 'w+')
        write_file.write(json.dumps(prev_data_json))
        write_file.close()
        response = app.response_class(
            status=200
        )
    else:
        response = app.response_class(
            status=400
            )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/<username>/<password>/set_essentials/<title>/<author>')
def set_essentials(username, password, title, author):
    global USERNAME, PASSWORD
    username = hashlib.md5(username.encode('utf-8')).hexdigest()
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    if username == USERNAME and password == PASSWORD:
        global BLOG_FILE_LOCATION
        read_file = open(BLOG_FILE_LOCATION, 'r')
        prev_data = read_file.read()
        read_file.close()
        prev_data_json = json.loads(prev_data.replace("\n", " ").replace("\t", " "))
        prev_data_json['title'] = title
        prev_data_json['author'] = author
        write_file = open(BLOG_FILE_LOCATION, 'w+')
        write_file.write(json.dumps(prev_data_json))
        write_file.close()
        response = app.response_class(
            status=200
        )

    else:
        response = app.response_class(
            status=400
        )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/<username>/<password>/set_user_pass/<user>/<passw>')
def set_user_pass(username, password, user, passw):
    global USERNAME, PASSWORD
    username = hashlib.md5(username.encode('utf-8')).hexdigest()
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    if username == USERNAME and password == PASSWORD:
        global USER_FILE_LOCATION
        user = hashlib.md5(user.encode('utf-8')).hexdigest()
        passw = hashlib.md5(passw.encode('utf-8')).hexdigest()
        write_file = open(USER_FILE_LOCATION, 'w+')
        write_file.write(f"{user}\n{passw}\n")
        write_file.close()
        response = app.response_class(
            status=200
        )
        update_blog()

    else:
        response = app.response_class(
            status=400
        )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



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
