import os
import secrets
from PIL import Image
from flask import url_for, current_app
# from flask_mail import Message
# from flaskblog import app, mail


def type_user(s):
    return "admin" if s == 1 else "normal"