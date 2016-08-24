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
                my_images = '%s/%s' % (IMAGE_STORE, names)
                image_list.append({'name': my_images.replace('http://', ''), 'type': 'public', 'tag': k})
        return {'images': image_list}


class ImagesBuild(Resource):

    def get(self):
        now = datetime.datetime.now().strftime('DockerFile-%Y-%m-%d-%H-%M-%S')
        docker_dir = 'DockerDir/' + now
        docker_file_path = docker_dir + '/DockerFile'
        args = request.args
        # 'fcloud_api/resources/glance/DockerFile/' +
        os.makedirs(docker_dir)
        with open(docker_file_path, 'a+') as f:
            f.write('FROM ' + args['from'] + '\n')
            f.write('MAINTAINER ' + args['maintainer']+ '\n')
            f.write('ADD ' + args['src_link'] + ' /usr/local/' '\n')
            if args.has_key('run'):
                f.write('RUN ' + args['run'])
        store = args['store']
        tag = args['tag']
        g = proc.Group()
        p = g.run(["docker", "build", "-t", "%s:%s" % (store, tag), docker_dir])
        #p = g.run(["bash", "-c", "for ((i=0;i<100;i=i+1)); do echo $i; sleep 1; done"])
        def read_process():
            while g.is_pending():
                lines = g.readlines()
                for proc, line in lines:
                    yield "retry:10000000\n"
                    yield "data:" + line + "\n\n"
            yield "data:Finished\n\n"
        return Response( read_process(), mimetype='text/event-stream' )
