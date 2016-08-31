# coding:utf8
from flask_restful import Resource
from fcloud_api.models import History
from flask import request
from fcloud_api.common.utils import AlchemyEncoder
from fcloud_api.common.utils import add_history
from fcloud_api.models import Flavor
from fcloud_api import db
from flask_restful_swagger import swagger
import json


class Flavors(Resource):

    @swagger.operation(
      notes='获取容器类型列表',
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
        """ 列出所有容器类型 """
        result = Flavor.query.order_by(Flavor.date).all()
        return {"flavors": json.loads(json.dumps(result, cls=AlchemyEncoder))}

    @add_history(u'新增', '容器类型')
    def post(self):
        """ Add A Flavors """
        data = request.json
        flavor = Flavor(**data)
        db.session.add(flavor)
        db.session.commit()
        return {"flavor": json.loads(json.dumps(flavor, cls=AlchemyEncoder))}, 200

    @add_history(u'删除', '容器类型')
    def delete(self):
        """ Delete Flavors """
        ids = request.args.get('ids')
        for i in ids.split(','):
            if i:
                f = Flavor.query.filter_by(id=i).first()
                db.session.delete(f)
        db.session.commit()
        return {"message": "delete success"}, 200