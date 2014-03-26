
import os
import urllib

def _requests_http_request(url, method, data):
    import requests
    if method.upper() == 'GET':
        return requests.get(url, data = data)
    elif method.upper() == 'POST':
        return requests.post(url, data = data)
    elif method.upper() == 'PUT':
        return requests.put(url, data = data)
    elif method.upper() == 'DELETE':
        return requests.delete(url, data = data)
    elif method.upper() == 'PATCH':
        return requests.patch(url, data = data)

    assert False

def _urlfetch_http_request(url, method, data):
    from google.appengine.api import urlfetch

    method = method.upper()
    qs = urllib.urlencode(data)
    if method == 'POST':
        payload = qs
    else:
        payload = None
        url += '?' + qs

    response = urlfetch.fetch(url,
        follow_redirects = True,
        method = method,
        payload = payload
    )

    return response

_is_appengine = None
def http_request(url, method, data = {}):
    global _is_appengine
    if _is_appengine is None:
        ss = os.environ.get('SERVER_SOFTWARE', None)
        _is_appengine = (ss and (ss.startswith('Development/') or ss.startswith('Google App Engine/')))

    if not _is_appengine:
        return _requests_http_request(url, method, data)
    else:
        return _urlfetch_http_request(url, method, data)

