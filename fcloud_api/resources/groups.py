from . import c
from marathon.models import MarathonApp
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import request


class Groups(Resource):

    def get(self):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/groups')), True)

    def post(self):
        c = HttpClient()
        data = request.json
        return c._result(c._post_json(c._url('/v2/groups'), data), True)

    def put(self):
        c = HttpClient()
        data = request.json
        return c._result(c._put(c._url('/v2/groups'), data=data), True)

    def delete(self):
        c = HttpClient()
        return c._result(c._delete(c._url('/v2/groups')), True)


class GroupsVersions(Resource):

    def get(self):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/groups/versions')), True)


class Group(Resource):

    def get(self, group_id):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/groups/{0}', group_id)), True)

    def post(self, group_id):
        c = HttpClient()
        data = request.json
        return c._result(c._post_json(c._url('/v2/groups/{0}', group_id), data), True)

    def put(self, group_id):
        c = HttpClient()
        data = request.json
        return c._result(c._put(c._url('/v2/groups/{0}', group_id), data=data), True)

    def delete(self, group_id):
        c = HttpClient()
        return c._result(c._delete(c._url('/v2/groups/{0}', group_id)), True)


class GroupVersion(Resource):

    def get(self, group_id):
        c = HttpClient()
        return c._result(c._get(c._url('/v2/groups/{0}/versions', group_id)), True)