from fcloud_api.resources import c
from marathon.models import MarathonApp
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import g
from fcloud_api.config import KEYSTONE


class Tenants(Resource):

    def get(self):
        c = HttpClient(base_url=KEYSTONE["uri"])
        headers = {"X-Auth-Token": g.token}
        return c._result(c._get(c._url('/v2.0/tenants'), headers=headers), True)