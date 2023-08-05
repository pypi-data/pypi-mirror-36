"""
A thin client for the Megaphone service.
"""

import requests.auth


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __eq__(self, rhs):
        return self.token == rhs.token

    def __call__(self, r):
        r.headers['Authorization'] = "Bearer {}".format(self.token)
        return r


class Megaphone(object):
    def __init__(self, url, api_key):
        self.url = url.rstrip('/')
        self.auth = BearerAuth(api_key)

    def send_version(self, broadcaster_id, channel_id, version):
        url = '{}/v1/broadcasts/{}/{}'.format(self.url, broadcaster_id, channel_id)
        resp = requests.put(url, auth=self.auth, data=version)
        resp.raise_for_status()
