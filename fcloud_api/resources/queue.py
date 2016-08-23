from . import c
from marathon.models import MarathonApp
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import request


class Queue(Resource):

    def get(self):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/queue')), True)


class DeleteQueue(Resource):

    def delete(self, app_id):
        c = HttpClient()
        return c._result(c._delete(c._url('/v2/queue/{0}/delay', app_id)), True)


class Ping(Resource):

    def get(self):
        c = HttpClient()
        return c._result(c._get(c._url('/ping')), True)


class Metrics(Resource):

    def get(self):
        c = HttpClient()
        return c._result(c._get(c._url('/metrics')), True)