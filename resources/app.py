# coding=utf8
from flask import Flask
from configs import config
from constants import FLASK_DOC_EXTENTION_KEY

__all__ = ['create_app']


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    extensions = configure_extensions(app)
    configure_template_filters(app)
    configure_hooks(app)
    configure_blueprints(app)
    extensions[FLASK_DOC_EXTENTION_KEY].prepare()
    return app


def configure_extensions(app):
    """
    配置Flask扩展
    :param app:
    :type app:
    :return:
    :rtype:
    """
    from flask_doc.generator import Generator
    results = {}
    results.update({FLASK_DOC_EXTENTION_KEY: Generator(app)})
    return results


def configure_template_filters(app):
    """
    配置模板的自定义过滤器
    :param app:
    :type app:
    :return:
    :rtype:
    """
    import filters
    for name in dir(filters):
        item = getattr(filters, name)
        if type(item) == type(configure_template_filters):
            app.jinja_env.filters.update({name: item})


def configure_hooks(app):
    """
    配置before和after操作的钩子
    :param app:
    :type app:
    :return:
    :rtype:
    """
    pass


def configure_blueprints(app):
    """
    配置blueprints
    :param app:
    :type app:
    :return:
    :rtype:
    """
    pass
