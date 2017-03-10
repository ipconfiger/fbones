# coding=utf8
"""
用于生成flask项目的脚手架命令工具
"""
import os
import shutil
import click
import sys


def get_path(*path):
    paths = []
    paths.append(os.getcwd())
    for p in path:
        paths.append(p)
    return os.path.join(*paths)


def copy_to(src, dst, ext):
    files_to_copy = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f)) and f.endswith(ext)]
    for f_name in files_to_copy:
        shutil.copy(os.path.join(src, f_name), dst)


def clear_directory(path):
    for item_name in [f for f in os.listdir(path)]:
        item_path = os.path.join(path, item_name)
        if os.path.isfile(item_path):
            os.remove(item_path)
        else:
            shutil.rmtree(item_path)


def set_lock():
    with open(get_path('.project'), 'w') as f:
        f.write('')
        f.close()


def check_lock():
    return os.path.exists(get_path('.project'))


def edit_alembic_env():
    """
    修补alembic的env.py使之可以用config.py中定义的DB_URL

    :return:
    :rtype:
    """
    file_path = get_path('db_versions', 'env.py')
    lines = None
    with open(file_path, 'r') as f:
        lines = f.readlines()
        f.close()
    lines.insert(4, "from models import Base")
    lines.insert(4, "from configs import settings")
    lines.insert(1, "sys.path.append(os.path.join('./'))")
    lines.insert(1, "import os")
    lines.insert(1, "import sys")
    for idx, line in enumerate(lines):
        if line.startswith('target_metadata ='):
            lines[idx] = 'target_metadata = Base.metadata'

    for idx, line in enumerate(lines):
        if line.startswith('    url = config.get_main_option'):
            lines [idx] = '    url = settings.DB_URI'

    selected_idx = 0
    for idx, line in enumerate(lines):
        if line.startswith('        config.get_section(config.config_ini_section)'):
            selected_idx = idx - 1
            lines[idx] = '        section,'

    lines.insert(selected_idx, "    section['sqlalchemy.url'] = settings.DB_URI")
    lines.insert(selected_idx, "    section = config.get_section(config.config_ini_section)")

    with open(file_path, 'w') as f:
        f.write("\n".join(lines))


@click.group()
def cli():
    pass


@click.command()
def init():
    if check_lock():
        click.echo("There's a exists project in this directory, an empty directory needed")
        sys.exit(1)
    click.echo('init project...')
    click.echo('create directory...')
    static_js_path = get_path('static', 'js')
    static_img_path = get_path('static', 'img')
    static_css_path = get_path('static', 'css')
    templates_path = get_path('templates')
    configs_path = get_path('configs')
    os.makedirs(static_js_path)
    os.makedirs(static_img_path)
    os.makedirs(static_css_path)
    os.makedirs(templates_path)
    os.makedirs(configs_path)
    click.echo('|-static/')
    click.echo('|    |----js/')
    click.echo('|    |----css/')
    click.echo('|    |----img/')
    click.echo('|')
    click.echo('|-templates/')
    click.echo('|')
    click.echo('|-configs/')
    git_root = get_path('.tmp')
    os.mkdir(git_root)
    click.echo('Downloading...')
    os.system('git clone https://github.com/ipconfiger/fbones.git %s' % git_root)
    click.echo('Download complete')
    copy_to('%s/resources' % git_root, os.getcwd(), '.py')
    copy_to('%s/resources/configs' % git_root, get_path('configs'), '.py')
    shutil.rmtree(git_root)
    click.echo('start initialize alembic')
    os.system('alembic init db_versions')
    edit_alembic_env()
    click.echo('completed!')
    set_lock()


@click.command()
@click.argument('name')
def addbp(name):
    if not check_lock():
        click.echo('This command must run under project root directory')
        sys.exit(1)
    click.echo('add blueprint:%s' % name)
    dir_path = get_path(name)
    os.mkdir(dir_path)
    view_lines = []
    view_lines.append("# coding=utf8")
    view_lines.append("from flask import Blueprint, g, request, jsonify")
    view_lines.append("")
    view_lines.append("")
    view_lines.append("bp = Blueprint('%(name)s', __name__, template_folder='templates/%(name)s', url_prefix='/%(name)s')" % dict(name=name))
    view_lines.append("")
    view_lines.append("")
    view_lines.append("@bp.route(\"/test\")")
    view_lines.append("def test():")
    view_lines.append("    return \"it works\"")
    view_lines.append("")
    file_path = get_path(name, "views.py")
    file_data = "\n".join(view_lines)
    with open(file_path, 'w') as f:
        f.write(file_data)
        f.close()

    init_py_path = get_path(name, '__init__.py')
    with open(init_py_path, 'w') as f:
        f.write('# coding=utf8')
        f.close()

    p = dict(name=name)

    insert_line0 = u"    from %(name)s import views as %(name)s_views" % p
    insert_line1 = u"    app.register_blueprint(%s_views.bp)" % name

    app_file = get_path('app.py')
    app_lines = None
    with open(app_file, 'r') as fi:
        app_lines = [l.decode('utf8') for l in fi.read().split('\n')]
        fi.close()
    if_in_function = False
    if_get_pass = False
    insert_point = 0
    for idx, line in enumerate(app_lines):
        if line.startswith(u'def configure_blueprints(app):'):
            if_in_function = True
        if if_in_function and line.strip().startswith(u'pass'):
            if_get_pass = True
        if if_in_function and if_in_function:
            insert_point = (idx - 1)

    app_lines.insert(insert_point, insert_line1)
    app_lines.insert(insert_point, insert_line0)

    with open(app_file, 'w') as fo:
        fo.write((u"\n".join(app_lines)).encode('utf8'))
        fo.close()

    click.echo("Blueprint created")


@click.command()
def clear():
    if not check_lock():
        click.echo('This command must run under project root directory')
        sys.exit(1)
    clear_directory(os.getcwd())
    click.echo("done")


@click.command()
def db_patch():
    edit_alembic_env()
    click.echo("Done!")


cli.add_command(init)
cli.add_command(addbp)
cli.add_command(clear)
cli.add_command(db_patch)

def main():
    cli()

if __name__ == "__main__":
    main()

