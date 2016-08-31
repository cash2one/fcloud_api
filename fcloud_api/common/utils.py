# coding:utf8
#################################################
#     　　　各种装饰器，你懂的 　　　　　　　　＃
#################################################
__author__ = 'liujiahua'
from flask_sqlalchemy import DeclarativeMeta
from fcloud_api.models import History
from fcloud_api import db
from fcloud_api.config import logging
from functools import wraps
from flask import g, request, jsonify
import datetime
import json

LOG = logging.getLogger(__name__)


SUCCESS_CODE = (200, 201, 202)


def get_object_id(kwargs):
    """ 给 add_history 用的方法 """
    if kwargs:
        object_id_list = []
        for k, v in kwargs.items():
            object_id_list.append(v)
        object_id = ':'.join(object_id_list)
    elif request.json is not None:
        object_id = request.json.get('id', None) or request.json.get('name', '')
    else:
        object_id = u'未知'
    return object_id


def add_history(action, action_object):
    """ 增加日志 """
    def exec_func(func):
        @wraps(func)
        def _exec_func(*args, **kwargs):
            LOG.info('Calling function: {}\n'.format(func.__name__))
            res = func(*args, **kwargs)
            result = u'成功' if res[1] in SUCCESS_CODE else u'失败'
            detail = str(res[0]) if result == u'失败' else u'成功'
            now = datetime.datetime.now()
            object_id = get_object_id(kwargs)
            history = History(user=g.username,
                              action=action,
                              action_object=action_object,
                              object_id=object_id,
                              result=result,
                              detail=detail,
                              date=now)
            db.session.add(history)
            db.session.commit()
            return res
        return _exec_func
    return exec_func


def user_login(func):
    """ 单独的用户登录日志 """
    @wraps(func)
    def _exec_func(*args, **kwargs):
        LOG.info('Calling function: {}\n'.format(func.__name__))
        res = func(*args, **kwargs)
        result = u'成功' if res[1] in SUCCESS_CODE else u'失败'
        detail = str(res[0]) if result == u'失败' else u'成功'
        now = datetime.datetime.now()
        object_id = request.json['auth']['passwordCredentials']['username']
        action = u'登录'
        action_object = u'keystone认证'
        history = History(user=object_id,
                              action=action,
                              action_object=action_object,
                              object_id=object_id,
                              result=result,
                              detail=detail,
                              date=now)
        db.session.add(history)
        db.session.commit()
        return res
    return _exec_func


class AlchemyEncoder(json.JSONEncoder):
    """ usage:
        c = YourAlchemyClass()
        print json.dumps(c, cls=AlchemyEncoder)
        query_set 转 json
    """
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)     # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:    # 添加了对datetime的处理
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.date):
                        fields[field] = data.isoformat()
                    elif isinstance(data, datetime.timedelta):
                        fields[field] = (datetime.datetime.min + data).time().isoformat()
                    else:
                        fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def admin_required(func):
    """ 定义只有管理员才能访问的API """
    @wraps(func)
    def is_admin(*args, **kwargs):
        if g.username == 'admin':
            ret = func(*args, **kwargs)
        else:
            ret = jsonify({"code": 403, "msg": "Only admin have access permissions"}), 403
        return ret
    return is_admin