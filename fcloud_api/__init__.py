# -*- coding: utf-8 -*-
__author__ = 'liujiahua'
# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import json
import re

from flask import Flask, Blueprint
from flask import abort
from flask import g
from flask import jsonify
from flask import request
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_restful_swagger import swagger
from config import KEYSTONE, DATABASE, logging
from fcloud_api.common.client import HttpClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api_bp = Blueprint('api', __name__)
#api = Api(api_bp)
api = swagger.docs(Api(api_bp), apiVersion='0.1',
                   basePath='http://127.0.0.1:8181',
                   resourcePath='/',
                   produces=["application/json", "text/html"],
                   api_spec_url='/api/spec',
                   description='fcloud_api 文档')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
#app.config['SQLALCHEMY_BINDS'] = {
#    'cmdb': DATABASE_CMDB,
#    'cloud': DATABASE_CLOUD
#}
db = SQLAlchemy(app)

logger = logging.getLogger(__name__)

@app.errorhandler(401)
def page_not_found(error):
    return jsonify({ "message": "Unauthorized, Token Required." }), 401


@app.before_request
def before_request():
    token = request.headers.get("X-Auth-Token")
    g.admin_token = KEYSTONE['admin_token']  # v3 keystone需要每次生成，这是V2 直接用 admin token
    g.uri = KEYSTONE['uri']
    g.admin_proj = KEYSTONE['admin_proj']
    # 静态文件和监控数据不用验证，直接通过
    if re.match('/fcloud_api/v1/images', request.path):
        g.token = g.admin_token
    elif re.match('/fcloud_api/v1/api/spec', request.path):
        pass
    elif re.match('/static', request.path):
        pass
    elif re.match('/fcloud_api/v1/tokens', request.path):
        pass
    elif not token:
        abort(401)
    else:
        if validatedToken(token):
            g.token = token  # 不带 tenant_id 的 token
            pass
        else:
            return jsonify({"error": "invalid token"}), 400


def validatedToken(token):
    try:
        if token == g.admin_token:
            return True
        headers = {"X-Auth-Token": "%s" % g.admin_token}
        c = HttpClient(base_url=KEYSTONE["uri"])
        c, s, h = c._result(c._get(c._url('/v2.0/tokens/%s' % token), headers=headers), True)
        if c.has_key('access'):
            g.username = c['access']['user']['username']
            return True
        else:
            return False
    except:
        return False


# v2 不需要这个方法了
def get_admin_token():
    try:
        c = HttpClient(base_url=KEYSTONE["uri"])
        data = """
                {
                    "auth": {
                        "identity": {
                            "methods": [
                                "password"
                            ],
                            "password": {
                                "user": {
                                    "domain": {
                                        "name": "default"
                                    },
                                    "name": "%s",
                                    "password": "%s"
                                }
                            }
                        },
                        "scope": {
                            "project": {
                                "domain": {
                                    "name": "default"
                                },
                                "name": "admin"
                            }
                        }
                    }
                }
            """ % (KEYSTONE['ks_user'], KEYSTONE['ks_pass'])
        c, s, headers = c._result(c._post_json(c._url('/v3/auth/tokens'), data=json.loads(data)), True)
        apitoken = headers['X-Subject-Token']
        return apitoken
    except:
        logger.exception('Error with get admin token')
        return None


#from mana_api import models
#api = Api(app)
#
#class HelloWorld(Resource):
#
#    def get(self):
#        return {'hello': 'world'}
#
#api.add_resource(HelloWorld, '/')
#from unify.api.identity import identity_bp

#app.register_blueprint(identity_bp, url_prefix='/identity')
from fcloud_api.resources.keystone.identity import Identity
from resources.apps import Apps
from resources.apps import App
from resources.apps import AppRestart
from resources.apps import AppTasks
from resources.apps import KillTask
from resources.apps import Versions
from resources.apps import VersionsVersion
from resources.deployments import Deployments
from resources.deployments import DeleteDeployments
from resources.groups import Groups
from resources.groups import GroupsVersions
from resources.groups import Group
from resources.groups import GroupVersion
from resources.tasks import Task
from resources.tasks import Tasks
from resources.tasks import TasksDelete
from resources.queue import Queue
from resources.queue import DeleteQueue
from resources.queue import Ping
from resources.queue import Metrics
from fcloud_api.resources.keystone.tenants import Tenants
from fcloud_api.resources.glance.images import Images, Image, ImagesBuild
from fcloud_api.resources.ceilometer.history import HistoryLog
from fcloud_api.resources.glance.flavors import Flavors

api.add_resource(Identity, '/tokens')
api.add_resource(Apps, '/apps')
api.add_resource(App, '/apps/<string:app_id>')
api.add_resource(AppRestart, '/apps/<string:app_id>/restart')
api.add_resource(AppTasks, '/apps/<string:app_id>/tasks')
api.add_resource(KillTask, '/apps/<string:app_id>/tasks/<string:task_id>')
api.add_resource(Versions, '/apps/<string:app_id>/versions')
api.add_resource(VersionsVersion, '/apps/<string:app_id>/versions/<string:version>')
api.add_resource(Deployments, '/deployments')
api.add_resource(DeleteDeployments, '/deployments/<string:deployment_id>')
api.add_resource(Groups, '/groups')
api.add_resource(GroupsVersions, '/groups/versions')
api.add_resource(Group, '/groups/<string:group_id>')
api.add_resource(GroupVersion, '/groups/<string:group_id>/versions')
api.add_resource(Task, '/tasks/<string:slave_ip>/<string:task_id>')
api.add_resource(Tasks, '/tasks')
api.add_resource(TasksDelete, '/tasks/delete')
api.add_resource(Queue, '/queue')
api.add_resource(DeleteQueue, '/queue/<string:app_id>/delay')
api.add_resource(Ping, '/ping')
api.add_resource(Metrics, '/Metrics')
api.add_resource(Tenants, '/tenants')
api.add_resource(Images, '/images')
api.add_resource(Image, '/image/<string:store>/<string:tag>')
api.add_resource(ImagesBuild, '/images_build')
api.add_resource(HistoryLog, '/history')
api.add_resource(Flavors, '/flavors')

app.register_blueprint(api_bp, url_prefix='/fcloud_api/v1')
