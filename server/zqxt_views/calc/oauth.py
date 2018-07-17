from django.db import models

class Account(models.Model):

    '''
    帐号
    :param _id: account ID
    :param username: 用户ID
    :param created_time: 创建时间
    :param password: 密码
    :param authentications: 认证信息 {'wxapp': 'openid', 'mobile': 'mobile_num'}
    :param status: 状态(active|发布|forbidden)
    '''

    meta = {
        'collection': 'account',
        'indexes': [
            '$username',  # text index
        ]
    }

    id = models.TextField(primary_key=True)
    nickname = models.TextField()
    avatar = models.TextField()
    username = models.TextField()
    password = models.TextField()
    authentications = models.TextField()
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()

    # @classmethod
    # def get_by_wxapp(cls,openid):
    #     account = cls.objects.get(id=openid)
    #     return account