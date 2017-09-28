from flask import Blueprint, render_template
from flask_login import login_required
from flask_restful import Api, Resource, url_for

bp = Blueprint('project', __name__)
api = Api(bp)

@bp.route('/')
@login_required
def test_for_vue():
    # import time
    # time.sleep(6)
    # return 'hello'
    return render_template('index.html')

class Project(Resource):
    def get(self, id):
        return {'task': 'done'}

    def post(self):
        pass

    def put(self):
        pass

api.add_resource(Project, '/project/<int:id>')