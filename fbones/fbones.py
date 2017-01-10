# coding=utf8
"""
用于生成flask项目的脚手架命令工具
"""
import os
import shutil
import click

def get_path(*path):
    paths = []
    paths.append(os.getcwd())
    for p in path:
        paths.append(p)
    return os.path.join(*paths)


@click.group()
def cli():
    pass


@click.command()
def init():
    click.echo('init project...')
    click.echo('create directory...')
    static_js_path = get_path('static', 'js')
    static_img_path = get_path('static', 'img')
    static_css_path = get_path('static', 'css')
    templates_path = get_path('templates')
    os.makedirs(static_js_path)
    os.makedirs(static_img_path)
    os.makedirs(static_css_path)
    os.makedirs(templates_path)
    click.echo('|-static/')
    click.echo('|    |----js/')
    click.echo('|    |----css/')
    click.echo('|    |----img/')
    click.echo('|')
    click.echo('|-templates/')




@click.command()
@click.argument('name')
def addbp(name):
    click.echo('add blueprint:%s' % name)


cli.add_command(init)
cli.add_command(addbp)


cli()

