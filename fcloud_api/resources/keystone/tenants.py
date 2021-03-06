# coding:utf8
from fcloud_api.resources import c
from marathon.models import MarathonApp
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import g
from fcloud_api.config import KEYSTONE
from flask_restful_swagger import swagger


class Tenants(Resource):

    @swagger.operation(
      notes='获取项目列表',
      nickname='get',
      # Parameters can be automatically extracted from URLs (e.g. <string:id>)
      # but you could also override them here, or add other parameters.
      parameters=[
          {
            "name": "X-Auth-Token",
            "description": "通过API获取的有效Token",
            "required": True,
            "allowMultiple": False,
            "dataType": 'string',
            "paramType": "header"
          }
      ])
    def get(self):
        """ 获取项目列表 """
        c = HttpClient(base_url=KEYSTONE["uri"])
        headers = {"X-Auth-Token": g.token}
        return c._result(c._get(c._url('/v2.0/tenants'), headers=headers), True)