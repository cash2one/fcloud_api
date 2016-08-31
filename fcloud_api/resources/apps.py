# coding:utf8
from . import c
from marathon.models import MarathonApp
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import request
from fcloud_api.config import logging
from fcloud_api.common.utils import add_history
from flask_restful_swagger import swagger


class Apps(Resource):

    @swagger.operation(
      notes='获取应用列表',
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
        """ 获取应用列表 """
        c = HttpClient()
        return c._result(c._get(c._url('/v2/apps')), True)

    @swagger.operation(
      notes='新增应用',
      nickname='post',
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
          },
          {
            "name": "body",
            "description": "json串",
            "required": True,
            "allowMultiple": False,
            "dataType": 'json',
            "paramType": "body"
          }
      ])
    @add_history(u'新增', u'应用')
    def post(self):
        """ 新增应用
        <pre>{
              "id": "myadd",
              "cpus": 1,
              "mem": 128,
              "disk": 0,
              "instances": 2,
              "container": {
                "docker": {
                  "image": "nginx",
                  "parameters": [
                    {
                      "key": "net",
                      "value": "mac_net1"
                    }
                  ]
                },
                "type": "DOCKER"
              }
            }
        </pre>
        """
        c = HttpClient()
        data = request.json
        return c._result(c._post_json(c._url('/v2/apps'), data), True)


    @add_history(u'更新', u'应用')
    def put(self):
        c = HttpClient()
        data = request.json
        return c._result(c._put(c._url('/v2/apps'), data=data), True)


class App(Resource):

    def get(self, app_id):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/apps/{0}', app_id)), True)

    @swagger.operation(
      notes='扩容应用',
      nickname='put',
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
          },
          {
            "name": "body",
            "description": "json串",
            "required": True,
            "allowMultiple": False,
            "dataType": 'json',
            "paramType": "body"
          }
      ])
    @add_history(u'扩容', u'应用')
    def put(self, app_id):
        """扩容应用
        {"id": "/nginx", "instances": 3}
        """
        c = HttpClient()
        data = request.json
        #logging.info('DATA: %s' % data)
        return c._result(c._put_json(c._url('/v2/apps/{0}', app_id), data=data), True)

    @swagger.operation(
      notes='删除应用',
      nickname='delete',
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
    @add_history(u'删除', u'应用')
    def delete(self, app_id):
        """ 删除应用 """
        c = HttpClient()
        return c._result(c._delete(c._url('/v2/apps/{0}', app_id)), True)


class AppRestart(Resource):

    @swagger.operation(
      notes='重启应用',
      nickname='post',
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
    @add_history(u'重启', u'应用')
    def post(self, app_id):
        c = HttpClient()
        return c._result(c._post(c._url('/v2/apps/{0}', app_id)), True)


class AppTasks(Resource):

    @swagger.operation(
      notes='获取容器列表',
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
    def get(self, app_id):
        """ 获取容器列表 """
        c = HttpClient()
        return c._result(c._get(c._url('/v2/apps/{0}/tasks', app_id)), True)

    @swagger.operation(
      notes='删除APP下所有容器',
      nickname='delete',
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
    @add_history(u'删除', u'所有容器')
    def delete(self, app_id):
        """ 删除APP下所有容器 """
        c = HttpClient()
        return c._result(c._delete(c._url('/v2/apps/{0}/tasks', app_id)), True)


class KillTask(Resource):

    @add_history(u'删除', u'单个容器')
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