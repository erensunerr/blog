from flask import Flask
from flask_multistatic import MultiStaticFlask
# app = Flask(__name__, static_folder="build/static", template_folder="build")
app = MultiStaticFlask(__name__, static_folder=[
"build/admin_panel/static", "build/user_blog/static"
], template_folder="build"
)
from app import routes
