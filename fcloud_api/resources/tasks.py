from . import c
from marathon.models import MarathonApp
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import request


class Tasks(Resource):

    def get(self):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/tasks')), True)


class TasksDelete(Resource):

    # Kill a list of running tasks.
    def post(self):
        c = HttpClient()
        data = request.json
        return c._result(c._post_json(c._url('/v2/tasks/delete'), data), True)