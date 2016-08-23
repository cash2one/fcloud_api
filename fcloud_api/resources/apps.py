from . import c
from marathon.models import MarathonApp
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import request



class Apps(Resource):

    def get(self):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/apps')), True)

    def post(self):
        c = HttpClient()
        data = request.json
        return c._result(c._post_json(c._url('/v2/apps'), data), True)

    def put(self):
        c = HttpClient()
        data = request.json
        return c._result(c._put(c._url('/v2/apps'), data=data), True)


class App(Resource):

    def get(self, app_id):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/apps/{0}', app_id)), True)

    def put(self, app_id):
        c = HttpClient()
        data = request.json
        return c._result(c._put(c._url('/v2/apps/{0}', app_id), data=data), True)

    def delete(self, app_id):
        c = HttpClient()
        return c._result(c._delete(c._url('/v2/apps/{0}', app_id)), True)


class AppRestart(Resource):

    def post(self, app_id):
        c = HttpClient()
        return c._result(c._post(c._url('/v2/apps/{0}', app_id)), True)


class AppTasks(Resource):

    def get(self, app_id):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/apps/{0}/tasks', app_id)), True)

    def delete(self, app_id):
        c = HttpClient()
        return c._result(c._delete(c._url('/v2/apps/{0}/tasks', app_id)), True)


class KillTask(Resource):

    def delete(self, app_id, task_id):
        c = HttpClient()
        return c._result(c._delete(c._url('/v2/apps/{0}/tasks/{1}',
                                          app_id, task_id)), True)


class Versions(Resource):

    def get(self, app_id):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/apps/{0}/versions', app_id)), True)


class VersionsVersion(Resource):

    def get(self, app_id, version):
        return c._result(c._get(c._url('/v2/apps/{0}/versions/{1}',
                                          app_id, version)), True)