import uuid
import logging
import json 
import requests
import re
from urllib import urlencode
from urllib2 import Request


from social_auth.backends import BaseOAuth2, OAuthBackend
from social_auth.utils import dsa_urlopen
import requests


logger = logging.getLogger(__name__)


class QQBackend(OAuthBackend):
    name = 'qq'
    EXTRA_DATA = [
        ('figureurl_2', 'figureurl_2'),
    ]

    def get_user_id(self, details, response):
        return response['openid']

    def get_user_details(self, response):
        logger.debug('response: ' + str(response))
        return {
            'username': response.get('nickname', '') + str(uuid.uuid4()),
            'first_name': response.get('nickname', '')
        }


class QQAuth(BaseOAuth2):
    AUTHORIZATION_URL = 'https://graph.qq.com/oauth2.0/authorize'
    ACCESS_TOKEN_URL = 'https://graph.qq.com/oauth2.0/token'
    AUTH_BACKEND = QQBackend
    SETTINGS_KEY_NAME = 'QQ_CLIENT_KEY'
    SETTINGS_SECRET_NAME = 'QQ_CLIENT_SECRET'
    REDIRECT_STATE = False

    def getOpenid(self, access_token):
        r = requests.get('https://graph.qq.com/oauth2.0/me', params={
            'access_token': access_token
        })

        try:
            ret = json.loads(re.search('\{.*\}',r.content).group())
        except Exception, e:
            ret = {x.split('=')[0]:str(x.split('=')[1]) for x in r.content.split("&")}

        if 'openid' not in ret:
            return None

        return ret['openid']

    def user_data(self, access_token, *args, **kwargs):
        openid = self.getOpenid(access_token)

        if not openid:
            return None

        url = 'https://graph.qq.com/user/get_user_info'

        try:
            data = requests.get(url, params={
                'access_token': access_token,
                'oauth_consumer_key': self.get_key_and_secret()[0],
                'openid': openid
            }).json()
            data['openid'] = openid
            return data
        except (ValueError, KeyError, IOError):
            logger.exception()
            return None

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        self.process_error(self.data)
        params = self.auth_complete_params(self.validate_state())
        request = Request(self.ACCESS_TOKEN_URL, data=urlencode(params),
                          headers=self.auth_headers())

        try:
            result = dsa_urlopen(request).read()
            import urlparse
            response = urlparse.parse_qs(result)
            logger.debug(str(response))
        except HTTPError, e:
            if e.code == 400:
                raise AuthCanceled(self)
            else:
                raise
        except (ValueError, KeyError):
            raise AuthUnknownError(self)

        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)


BACKENDS = {
    'qq': QQAuth
}