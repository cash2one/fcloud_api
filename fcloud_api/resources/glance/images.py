# coding:utf8
from flask_restful import Resource
from flask_restful import reqparse
from flask_restful import fields, marshal_with
from fcloud_api.common.client import HttpClient
from flask import request, Response
from fcloud_api.config import IMAGE_STORE
import os
import gevent
import gevent.monkey
import datetime
gevent.monkey.patch_all()
from shelljob import proc
from fcloud_api.config import logging
from fcloud_api.common.utils import add_history
from flask_restful_swagger import swagger

LOG = logging.getLogger(__name__)

class Images(Resource):

    @swagger.operation(
      notes='获取镜像列表',
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
        """ 获取镜像列表 """
        c = HttpClient(base_url=IMAGE_STORE)
        r, _, _ = c._result(c._get(c._url('/v1/search')), True)
        results = r['results']
        image_list = []
        for result in results:
            names = result['name'].split('/')[-1]
            _r, _, _ = c._result(c._get(c._url('/v1/repositories/%s/tags' % names)), True)
            for k, v in _r.items():
                my_images = '%s/%s' % (IMAGE_STORE, names)
                image_list.append({'name': my_images.replace('http://', ''), 'type': 'public', 'tag': k})
        return {'images': image_list}


class Image(Resource):

    @swagger.operation(
      notes='获取镜像明细',
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
          },

      ])
    def get(self, store, tag):
        """ 获取镜像明细 """
        c = HttpClient(base_url=IMAGE_STORE)
        image_id, _, _ = c._result(c._get(c._url('/v1/repositories/%s/tags/%s' % (store, tag))))
        image_id = image_id.replace('"', '')
        return c._result(c._get(c._url('/v1/images/%s/json' % image_id)), True)

    @swagger.operation(
      notes='删除镜像',
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
          },

      ])
    @add_history(u'删除', u'镜像')
    def delete(self, store, tag):
        """ 删除镜像 """
        c = HttpClient(base_url=IMAGE_STORE)
        return c._result(c._delete(c._url('/v1/repositories/%s/tags/%s' % (store, tag))), True)


class ImagesBuild(Resource):

    def get(self):
        args = request.args
        store = args['store']
        tag = args['tag']
        docker_dir = 'DockerDir/%s-%s' % (store, tag)
        docker_file_path = docker_dir + '/Dockerfile'
        if not os.path.exists(docker_dir):
            os.makedirs(docker_dir)
        if os.path.exists(docker_file_path):
            os.remove(docker_file_path)
        with open(docker_file_path, 'a+') as f:
            f.write('FROM ' + args['from'] + '\n')
            f.write('MAINTAINER ' + args['maintainer']+ '\n')
            f.write('ADD ' + args['src_link'] + ' /usr/local/' '\n')
            if args.has_key('run'):
                f.write('RUN ' + args['run'])
        g = proc.Group()
        image_name = store + ':' + tag
        DICT = {
            "image_name": image_name,
            "image_store": IMAGE_STORE.replace('http://', ''),
            "docker_dir": docker_dir
        }
        cmd = "docker build -t %(image_name)s %(docker_dir)s " \
              "&& docker tag %(image_name)s %(image_store)s/%(image_name)s " \
              "&& docker push %(image_store)s/%(image_name)s" \
              "&& docker rmi %(image_name)s" \
              "&& docker rmi %(image_store)s/%(image_name)s" % DICT
        p = g.run(["/bin/bash", "-c", cmd])
        #p = g.run(["bash", "-c", "for ((i=0;i<100;i=i+1)); do echo $i; sleep 1; done"])
        def read_process():
            try:
                while g.is_pending():
                    lines = g.readlines()
                    for proc, line in lines:
                        yield "retry:10000000\n"
                        yield "data:" + line + "\n\n"
                if g.get_exit_codes()[0][1] != 0:
                    yield "data:Error\n\n"
                yield "data:Finished\n\n"
            except Exception, e:
                LOG.exception('Error with build images, user: %s' % args['maintainer'])
                yield "data:Error\n\n"
                yield "data:%s\n\n" % e
        return Response( read_process(), mimetype='text/event-stream' )