# coding=utf8

from flask import Blueprint, g, request, jsonify

bp = Blueprint('api', __name__, template_folder='templates', url_prefix='/api')


@bp.route('/test')
def test():
    return "it works"



