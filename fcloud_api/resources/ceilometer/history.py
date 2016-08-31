# coding:utf8
from flask_restful import Resource
from fcloud_api.models import History
from flask import request
from fcloud_api.common.utils import AlchemyEncoder
import json
from flask_restful_swagger import swagger


class HistoryLog(Resource):

    @swagger.operation(
      notes='获取历史操作记录',
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
        """ 获取操作日志 """
        filters = request.args
        if filters.has_key('limit'):
            limit = int(filters['limit'])
            result = History.query.order_by(-History.date).limit(limit).all()
        else:
            result = History.query.order_by(-History.date).all()
        return {"history": json.loads(json.dumps(result, cls=AlchemyEncoder))}