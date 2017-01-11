# coding=utf8

import default_Settings
import config

__all__ = ['settings']


def load_settings():
    for class_name in dir(config):
        if (not class_name.startswith('__')) and (not class_name.endswith("__")) and class_name != "Config":
            config_item = getattr(config, class_name)
            if issubclass(config_item, default_Settings.Config):
                return config_item
    raise ImportError

settings = load_settings()