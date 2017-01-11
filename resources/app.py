# coding=utf8
from flask import Flask
from configs import config

__all__ = ['create_app']


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    configure_extensions(app)
    configure_template_filters(app)
    configure_hooks(app)
    configure_blueprints(app)
    return app


def configure_extensions(app):
    """
    配置Flask扩展
    :param app:
    :type app:
    :return:
    :rtype:
    """
    pass


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
    import xxx
    app.register_blueprint(xxx.views.bp)
    pass
