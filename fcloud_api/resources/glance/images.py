from fcloud_api.resources import c
from marathon.models import MarathonApp
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import request, Response, render_template
from fcloud_api.config import IMAGE_STORE
import gevent
import gevent.monkey
gevent.monkey.patch_all()


def event_stream():
    count = 0
    while True:
        gevent.sleep(2)
        yield 'data: %s\n\n' % count
        count += 1


class Images(Resource):

    def get(self):
        c = HttpClient(base_url=IMAGE_STORE)
        r, _, _ = c._result(c._get(c._url('/v1/search')), True)
        results = r['results']
        image_list = []
        for result in results:
            names = result['name'].split('/')[-1]
            _r, _, _ = c._result(c._get(c._url('/v1/repositories/%s/tags' % names)), True)
            for k, v in _r.items():
                my_images = '%s/%s:%s' % (IMAGE_STORE, names, k)
                image_list.append({'name': my_images.replace('http://', ''), 'type': 'public'})
        return {'images': image_list}


class ImagesBuild(Resource):

    def get(self):
        resp = Response(event_stream(), mimetype='text/event-stream')
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp