# coding:utf8
from . import c
from flask_restful import Resource
from fcloud_api.common.client import HttpClient
from flask import request
from docker import Client
from flask_restful_swagger import swagger

class Task(Resource):
    """ 脱离 marathon 的 API"""

    @swagger.operation(
      notes='获取容器明细',
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
    def get(self, slave_ip, task_id):
        """ 获取容器明细 """
        app_id, uuid = task_id.split('.')
        container_id = 'docker.' + uuid
        c = Client('tcp://' + slave_ip + ':2375')
        r = c.inspect_container(container_id)
        return r

    @swagger.operation(
      notes='重启容器',
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
    def post(self, slave_ip, task_id):
        """ 重启容器 """
        app_id, uuid = task_id.split('.')
        container_id = 'docker.' + uuid
        c = Client('tcp://' + slave_ip + ':2375')
        r = c.restart(container_id)
        return r


class Tasks(Resource):

    def get(self):
        """ List all running tasks """
        c = HttpClient()
        return c._result(c._get(c._url('/v2/tasks')), True)


class TasksDelete(Resource):

    # Kill a list of running tasks.
    def post(self):
        c = HttpClient()
        data = request.json
        return c._result(c._post_json(c._url('/v2/tasks/delete'), data), True)