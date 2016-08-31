# coding:utf8
from flask_restful import Resource
from fcloud_api.common.client import HttpClient
from flask import request
from fcloud_api.config import KEYSTONE
from fcloud_api.common.utils import user_login
from flask_restful_swagger import swagger


class Identity(Resource):

    @swagger.operation(
      notes='获取Token',
      nickname='get',
      # Parameters can be automatically extracted from URLs (e.g. <string:id>)
      # but you could also override them here, or add other parameters.
      parameters=[
          {
            "name": "body",
            "description": "json串",
            "required": True,
            "allowMultiple": False,
            "dataType": 'json',
            "paramType": "body"
          }
      ])
    @user_login
    def post(self):
        """获取有效Token
        <pre>{
            "auth": {
                "tenantName": "",
                "passwordCredentials": {
                    "username": "admin",
                    "password": "password"
                }
            }
        }</pre>
        """
        c = HttpClient(base_url=KEYSTONE["uri"])
        data = request.json
        return c._result(c._post_json(c._url('/v2.0/tokens'), data), True)