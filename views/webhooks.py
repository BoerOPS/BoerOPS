from flask import Blueprint, render_template

bp = Blueprint('webhook', __name__)

@bp.route('/pushhook', methods=['GET', 'POST'])
def push_hook():
    return 'hook'