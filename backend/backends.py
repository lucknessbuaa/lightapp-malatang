import logging
import requests

from backend.models import Account
from django.contrib.auth.models import User
import json

logger = logging.getLogger(__name__)

class BaiduBackend(object):
    def authenticate(self, token=None):
        r = requests.get('https://openapi.baidu.com/rest/2.0/passport/users/getLoggedInUser', params={
            'access_token': token
        })
        ret = json.loads(r.content)

        if r.status_code != 200 or 'error_code' in ret:
            logger.warn('not authenticated')
            return None

        logger.warn(ret)

        authID = str(ret['uid'])
        authType = 'BAIDU'
        name = 'baidu_' + authID
        try:
            account = Account.objects.get(authType=authType, authID=authID)
        except Exception, e:
            user = User.objects.create(username=name)
            account = Account.objects.create(authType=authType, authID=authID, user=user)
                    
        logger.debug(account.user)
        logger.debug(account.user.is_authenticated())

        return account.user

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)


class WeiboBackend(object):
    def authenticate(self, token=None):
        r = requests.get('https://api.weibo.com/2/account/get_uid.json', params={
            'access_token': token
        })
        ret = json.loads(r.content)

        if r.status_code != 200 or 'error_code' in ret:
            logger.warn('not authenticated')
            return None

        logger.warn(ret)

        authID = str(ret['uid'])
        authType = 'WEIBO'
        name = 'weibo_' + authID
        try:
            account = Account.objects.get(authType=authType, authID=authID)
        except Exception, e:
            user = User.objects.create(username=name)
            account = Account.objects.create(authType=authType, authID=authID, user=user)
                    
        logger.debug(account.user)
        logger.debug(account.user.is_authenticated())

        return account.user

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)


class QQBackend(object):
    def authenticate(self, token=None):
        r = requests.get('https://openapi.baidu.com/rest/2.0/passport/users/getLoggedInUser', params={
            'access_token': token
        })
        ret = json.loads(r.content)

        if r.status_code != 200 or 'error_code' in ret:
            logger.warn('not authenticated')
            return None

        logger.warn(ret)

        name = ret['uname']
        authID = ret['uid']
        authType = 'BAIDU'
        try:
            account = Account.objects.get(authType=authType, authID=authID)
        except Exception, e:
            user = User.objects.create(username=name)
            account = Account.objects.create(authType=authType, authID=authID, user=user)
                    
        logger.debug(account.user)
        logger.debug(account.user.is_authenticated())

        return account.user

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)