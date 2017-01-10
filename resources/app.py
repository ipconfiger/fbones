# coding=utf8

from flask import Flask


def create_app():
    app = Flask(__name__)
    regist_errorhandlers(app)
    regist_extensions(app)
    regist_hooks(app)
    regist_blueprints(app)
    return app


def regist_blueprints(app):
    pass


def regist_extensions(app):
    pass


def regist_errorhandlers(app):
    pass


def regist_hooks(app):
    pass
