# coding=utf8
"""
用于生成flask项目的脚手架命令工具
"""
import os
import shutil
import click
import sys


def command(func):
    cli.add_command(func)
    return func


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

@command
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


@command
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


@command
@click.command()
def clear():
    if not check_lock():
        click.echo('This command must run under project root directory')
        sys.exit(1)
    clear_directory(os.getcwd())
    click.echo("done")


@command
@click.command()
def db_patch():
    edit_alembic_env()
    click.echo("Done!")

@command
@click.command()
@click.argument('name')
@click.argument('port')
@click.argument('core')
def deploy_supervisor(name, port, core):
    params = dict(
        name=name,
        port=port,
        core=core,
        path=get_path()
    )
    template = """[program:%(name)s]
command=/usr/local/bin/gunicorn -w %(core)s -b 127.0.0.1:%(port)s --timeout 180 --worker-class="egg:meinheld#gunicorn_worker" wsgi:app
directory=%(path)s
umask=022
startsecs=0
stopwaitsecs=0
redirect_stderr=true
stdout_logfile=/var/log/%(name)s.log
stderr_logfile=/var/log/%(name)s-error.log
autorestart=true
autostart=true
""" % params
    click.echo(template)

@click.command()
@click.argument('name')
@click.argument('port')
@click.argument('domain')
def deploy_nginx(name, port, domain):
    params = dict(
        name=name,
        port=port,
        domain=domain,
        path=get_path()
    )
    txt = """upstream %(name)s {
  server 127.0.0.1:%(port)s;
}

server {
  listen 80;
  server_name %(domain)s;
  access_log /var/log/nginx/%(name)s.log main;
  error_log /var/log/nginx/%(name)s error.log;

  location /static {
    root %(path)s;
  }

  location / {
    expires           -1;
    proxy_pass_header Server;
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Scheme $scheme;
    proxy_redirect off;
    proxy_pass http://%(name)s;
    proxy_next_upstream error;
    proxy_connect_timeout 60;
    proxy_send_timeout 60;
    proxy_read_timeout 60;
  }
}
""" % params
    click.echo(txt)

@command
@click.command()
@click.argument('model_class')
def gen_serv(model_class):
    """
    生成基础服务代码
    :param model_class:
    :type model_class:
    :return:
    :rtype:
    """
    sys.path.append('.')
    try:
        model_name, class_name = model_class.split(':')
    except Exception as e:
        click.echo(u"argument must as module:class")
        sys.exit(1)
    mod = __import__(model_name)
    cls = getattr(mod, class_name)
    serviceName = "%sService" % class_name
    tb_name = cls.__tablename__
    rows = ["class %s(object):" % serviceName]
    rows.append("    def __init__(self):")
    rows.append("        self.%s_id = None" % tb_name)
    rows.append("        self.%s = None" % tb_name)
    rows.append("")
    rows.append("    @classmethod")
    rows.append("    def fromId(cls, id):")
    rows.append("        ins = cls()")
    rows.append("        ins.%s_id = id" % tb_name)
    rows.append("        ins.%s = %s.byId(id)" % (tb_name, class_name))
    rows.append("        return ins")
    rows.append("")
    rows.append("    @classmethod")
    rows.append("    def fromObject(cls, obj):")
    rows.append("        ins = cls()")
    rows.append("        ins.%s_id = obj.id" % tb_name)
    rows.append("        ins.%s = obj" % tb_name)
    rows.append("        return ins")
    rows.append("")
    rows.append("    def remove(self):")
    rows.append("        db.delete(self.%s)" % tb_name)
    rows.append("")
    rows.append("")
    txt = "\n".join(rows)
    click.echo(txt)
    sys.exit(0)


def main():
    cli()

if __name__ == "__main__":
    main()

