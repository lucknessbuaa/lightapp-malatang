import logging
import json 
from urllib import urlencode

from social_auth.backends import BaseOAuth2, OAuthBackend
import requests


logger = logging.getLogger(__name__)


class BaiduBackend(OAuthBackend):
    name = 'baidu'
    EXTRA_DATA = [
        ('portrait', 'portrait'),
    ]

    def get_user_id(self, details, response):
        return response['userid']

    def get_user_details(self, response):
        return {
            'username': response.get('username', ''),
            'first_name': response.get('realname', '')
        }


class BaiduAuth(BaseOAuth2):
    AUTHORIZATION_URL = 'https://openapi.baidu.com/oauth/2.0/authorize'
    ACCESS_TOKEN_URL = 'https://openapi.baidu.com/oauth/2.0/token'
    AUTH_BACKEND = BaiduBackend
    SETTINGS_KEY_NAME = 'BAIDU_CLIENT_KEY'
    SETTINGS_SECRET_NAME = 'BAIDU_CLIENT_SECRET'
    REDIRECT_STATE = False

    def user_data(self, access_token, *args, **kwargs):
        url = 'https://openapi.baidu.com/rest/2.0/passport/users/getInfo'
        try:
            data = requests.get(url, params={
                'access_token': access_token
            }).json()
            logger.debug(data)
            return data
        except (ValueError, KeyError, IOError):
            logger.exception()
            return None


BACKENDS = {
    'baidu': BaiduAuth
}