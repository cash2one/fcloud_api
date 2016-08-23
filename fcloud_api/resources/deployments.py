from . import c
from marathon.models import MarathonApp
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import request


class Deployments(Resource):

    def get(self):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/deployments')), True)


class DeleteDeployments(Resource):

    def delete(self, deployment_id):
        c = HttpClient()
        return c._result(c._delete(c._url('/v2/deployments/{0}', deployment_id)), True)