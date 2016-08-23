import six
import json
import requests
import requests.exceptions
from fcloud_api import config
from functools import partial
import errors


class HttpClient(requests.Session):
    def __init__(self, base_url=config.MARATHON_URL,
                 timeout=config.DEFAULT_TIMEOUT_SECONDS):
        super(HttpClient, self).__init__()
        self.base_url = base_url
        self.timeout = timeout

    def _set_request_timeout(self, kwargs):
        """Prepare the kwargs for an HTTP request by inserting the timeout
        parameter, if not already present."""
        kwargs.setdefault('timeout', self.timeout)
        return kwargs

    def _post(self, url, **kwargs):
        return self.post(url, **self._set_request_timeout(kwargs))

    def _get(self, url, **kwargs):
        return self.get(url, **self._set_request_timeout(kwargs))

    def _put(self, url, **kwargs):
        return self.put(url, **self._set_request_timeout(kwargs))

    def _delete(self, url, **kwargs):
        return self.delete(url, **self._set_request_timeout(kwargs))

    def _url(self, pathfmt, *args, **kwargs):
        for arg in args:
            if not isinstance(arg, six.string_types):
                raise ValueError(
                    'Expected a string but found {0} ({1}) '
                    'instead'.format(arg, type(arg))
                )
        quote_f = partial(six.moves.urllib.parse.quote_plus, safe="/:")
        args = map(quote_f, args)
        return '{0}{1}'.format(self.base_url, pathfmt.format(*args))

    def _raise_for_status(self, response, explanation=None):
        """Raises stored :class:`APIError`, if one occurred."""
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise errors.NotFound(e, response, explanation=explanation)
            raise errors.APIError(e, response, explanation=explanation)

    def _result(self, response, json=False, binary=False):
        assert not (json and binary)
        #self._raise_for_status(response)
        token = response.headers.get('X-Subject-Token', '')
        headers = {'X-Subject-Token': token}
        if json:
            return response.json(), response.status_code, headers
        if binary:
            return response.content, response.status_code, headers
        return response.text, response.status_code, headers

    def _post_json(self, url, data, **kwargs):
        # Go <1.1 can't unserialize null to a string
        # so we do this disgusting thing here.
        data2 = {}
        if data is not None:
            for k, v in six.iteritems(data):
                if v is not None:
                    data2[k] = v

        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        kwargs['headers']['Content-Type'] = 'application/json'
        return self._post(url, data=json.dumps(data2), **kwargs)


if __name__ == "__main__":
    a = HttpClient()
    u = a._url('/v2/apps/{0}', 'myadd')
    r = a._result(a._get(u), True)
    print r