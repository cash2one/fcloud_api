from . import c
from marathon.models import MarathonApp
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import request
from fcloud_api.config import KEYSTONE



class Identity(Resource):

    def post(self):
        c = HttpClient(base_url=KEYSTONE["uri"])
        data = request.json
        return c._result(c._post_json(c._url('/v3/auth/tokens'), data), True)