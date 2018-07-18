from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from weixin import WXAPPAPI
from weixin.lib.wxcrypt import WXBizDataCrypt
from calc.oauth import Account
from calc.models import User
from calc.models import Category
from calc.models import Tag
from calc.models import Label
from calc.models import Service
from calc.models import Post
from calc.models import PostPicture
from calc.models import ServicePicture
from calc.models import Follow
from calc.models import Star
import datetime
import jwt
import json
from django.core import serializers
from datetime import datetime
import time

APP_ID = '1'
APP_SECRET = '2'

# api = WXAPPAPI(appid=APP_ID,
#                   app_secret=APP_SECRET)
# session_info = api.exchange_code_for_session_key(code=code)

# # 获取session_info 后

# session_key = session_info.get('session_key')
# crypt = WXBizDataCrypt(WXAPP_APPID, session_key)

# # encrypted_data 包括敏感数据在内的完整用户信息的加密数据
# # iv 加密算法的初始向量
# # 这两个参数需要js获取
# user_info = crypt.decrypt(encrypted_data, iv)
# # Create your views here.






def add(request):
	a = request.GET['a']
	b = request.GET['b']
	c = int(a)+int(b)
	return HttpResponse(str(c))

def add2(request,a,b):
	c = int(a)+int(b)
	type = request.META.get('HTTP_CONTENT_TYPE', 'unkown')
	
	return HttpResponse(str(c))

def index(request):
	return render(request, 'home.html')

def old_add2_redirect(request,a,b):
	return HttpResponseRedirect(
		reverse('add2', args=(a,b)))






def get_wxapp_userinfo(encrypted_data, iv, code):
    from weixin.lib.wxcrypt import WXBizDataCrypt
    from weixin import WXAPPAPI
    from weixin.oauth2 import OAuth2AuthExchangeError
    appid = 'wx73bdc6a0b793aa42'
    secret = 'd18f4ce06504cc4d7c2dbb0e06e03929'
    api = WXAPPAPI(appid=appid, app_secret=secret)
    try:
        # 使用 code  换取 session key    
        session_info = api.exchange_code_for_session_key(code=code)
    except OAuth2AuthExchangeError as e:
        raise Unauthorized(e.code, e.description)
    session_key = session_info.get('session_key')
    crypt = WXBizDataCrypt(appid, session_key)
    # 解密得到 用户信息
    user_info = crypt.decrypt(encrypted_data, iv)
    print(user_info)
    return user_info


def verify_wxapp(encrypted_data, iv, code):
	# print('-------------')
	# print(code)
    user_info = get_wxapp_userinfo(encrypted_data, iv, code)
    # 获取 openid
    openid = user_info.get('openId', None)
    nickname = user_info.get('nickName', None)
    avatar = user_info.get('avatarUrl', None)
    print(openid)
    if openid:
    	try:
    		auth = User.objects.get(id=openid)
    		if not auth:
        		raise Unauthorized('wxapp_not_registered')
    		return auth
    	except User.DoesNotExist:
    		acc = User()
    		acc.id = openid
    		acc.nickname = nickname
    		acc.avatar = avatar
    		acc.created_time = datetime.now()
    		acc.updated_time = datetime.now()
    		acc.save()
    	
    	raise Unauthorized('invalid_wxapp_code')
    
  
def create_token(request):
    # verify basic token
    approach = request.POST['auth_approach']
    username = request.POST['username']
    password = request.POST['password']
    print(approach)
    print(username)
    print(password)
    print(request.GET.get('code'))
    account = verify_wxapp(username, password, request.GET.get('code'))
    if not account:
        return False, {}
    payload = {
        "sub": account.id,
        "nickname": account.nickname,
        "scopes": ['open']
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    print('----------------------------')
    print(token)
    print(account.id)
    token = str(token, encoding="utf-8")
    resp = {'access_token': token, 'account_id': account.id}
    return HttpResponse(json.dumps(resp), content_type="application/json")

def verify_token(token):
	try:
		payload = jwt.decode(token, 'secret', algorithm='HS256')
	except Exception as e:
		return False
	else:
		pass
	finally:
		pass
	
	if payload:
		return True, token
	return False, token


def get_category(request):

	# resp = serializers.serialize("json", Category.objects.values('categoryId','categoryName'))
	all_categories = list(Category.objects.all())
	all_dicts = list()
	for categories in all_categories:
		eve_tags = list(Tag.objects.filter(category__categoryId=categories.categoryId))
		tagNames = list()
		for tags in eve_tags:
			tagNames.append(tags.tagName)
		eve_dict = dict(id=categories.categoryId,name=categories.categoryName,labels=tagNames)
		all_dicts.append(eve_dict)

	print(all_dicts)
	res_json = json.dumps(all_dicts)
	# print(all_categories)

	return HttpResponse(res_json)

def get_index_recommand(request):
	all_labels = list(Label.objects.all())
	all_dicts = list()
	for labels in all_labels:
		even_dict = dict(id=labels.labelNum,name=labels.user.nickname,imgUrl=labels.user.avatar,userId=labels.user.id,tag=labels.labelName,description=labels.labelDes)
		all_dicts.append(even_dict)
	res_json = json.dumps(all_dicts)
	return HttpResponse(res_json)

def get_person(request):
	request_user_id = request.GET['userId']
	# print(request_user_id)
	user_all_labels = list(Label.objects.filter(user__id=request_user_id))
	print(user_all_labels)
	labels_all_dict = list()
	for labels in user_all_labels:
		# 获取service
		eve_label_services = list(Service.objects.filter(label__labelNum=labels.labelNum))
		serviceNames = list()
		for services in eve_label_services:
			serviceNames_dict = dict(name=services.serviceName)
			serviceNames.append(serviceNames_dict)
		# 获取post
		eve_label_posts = list(Post.objects.filter(label__labelNum=labels.labelNum))
		postObjects = list()
		for posts in eve_label_posts:
			pictures = list(PostPicture.objects.filter(post__postNum=posts.postNum))
			imgUrls = list()
			for pic in pictures:
				picUrls_dict = dict(imageUrl=pic.url)
				imgUrls.append(picUrls_dict)
			str_date = posts.date.strftime("%Y-%m-%d")
			postObjects_dict = dict(postID=posts.postNum,time=str_date,desc=posts.postDes,imgList=imgUrls)
			postObjects.append(postObjects_dict)
		eve_dict = dict(id=labels.labelNum,name=labels.labelName,desc=labels.labelDes,service=serviceNames,post=postObjects)
		labels_all_dict.append(eve_dict)
	res_json = json.dumps(labels_all_dict)
	return HttpResponse(res_json)

def login(request):
	client_access_token = request.GET['access_token']
	client_account_id = request.GET['account_id']
	print(client_access_token)
	print(client_account_id)
	res_dict = dict()
	if(verify_token(client_access_token)):
		the_user = User.objects.get(id=client_account_id)
		print(the_user)
		res_dict = dict(nickName=the_user.nickname,avatarUrl=the_user.avatar,userDesc=the_user.user_des)
	else:
		print('false')
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def changeDesc(request):
	client_access_token = request.POST['access_token']
	client_account_id = request.POST['account_id']
	changedDesc = request.POST['changedDesc']
	res_dict = dict()
	if(verify_token(client_access_token)):
		the_user = User.objects.get(id=client_account_id)
		the_user.user_des = changedDesc
		the_user.save()
		res_dict = dict(userDesc=changedDesc)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def get_follow(request):
	client_access_token = request.GET['access_token']
	client_account_id = request.GET['account_id']
	res_dict = list()
	if(verify_token(client_access_token)):
		# the_user = User.objects.get(id=client_account_id)
		user_all_follows = list(Follow.objects.filter(user__id=client_account_id))
		for follows in user_all_follows:
			res_dict.append(follows.followTagName.tagName)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def get_star(request):
	client_access_token = request.GET['access_token']
	client_account_id = request.GET['account_id']
	res_dict = list()
	if(verify_token(client_access_token)):
		# the_user = User.objects.get(id=client_account_id)
		user_all_stars = list(Star.objects.filter(user__id=client_account_id))
		labelList = list()
		for stars in user_all_stars:
			label_types = stars.label.tag.category.categoryName
			label_user_name = stars.label.user.nickname
			label_user_avatar = stars.label.user.avatar
			label_name = stars.label.labelName
			label_des = stars.label.labelDes
			eve_label = dict(labelType=label_types,name=label_user_name,imgUrl=label_user_avatar,label=label_name,description=label_des)
			labelList.append(eve_label)
		for i in range(len(labelList)):
			label_type = labelList[i]['labelType']
			tagList = list()
			for j in range(i,len(labelList)):
				if(labelList[j]['labelType']==label_type):
					tagList.append(dict(name=labelList[j]['name'],imgUrl=labelList[j]['imgUrl'],label=labelList[j]['label'],description=labelList[j]['description']))
			eve_dict = dict(type=label_type,tagList=tagList)
			res_dict.append(eve_dict)
		
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def getFollowStatus(request):
	client_access_token = request.GET['access_token']
	client_account_id = request.GET['account_id']
	tagName = request.GET['tagName']
	isFollowed = 0
	if(verify_token(client_access_token)):
		try:
			tmpFollow = Follow.objects.get(user__id=client_account_id,followTagName__tagName=tagName)
			print(tmpFollow)
			if tmpFollow:
				isFollowed = 1
		except Exception as e:
			isFollowed = 0
		else:
			pass
		finally:
			pass
	res_dict = dict(isFollow=isFollowed)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def changeFollowStatus(request):
	client_access_token = request.GET['access_token']
	client_account_id = request.GET['account_id']
	tagName = request.GET['tagName']
	isFollowed = 1
	if(verify_token(client_access_token)):
		try:
			tmpFollow = Follow.objects.get(user__id=client_account_id,followTagName__tagName=tagName)
			print(tmpFollow)
			if tmpFollow:
				print('will delete')
				tmpFollow.delete()
				isFollowed = 0
			if not tmpFollow:
				print('will add')
				the_user = User.objects.get(id=client_account_id)
				the_tag = Tag.objects.get(tagName=tagName)
				newFollow = Follow.objects.create(user=the_user,followTagName=the_tag)
				print(newFollow)
				newFollow.save()
		except Exception as e:
			isFollowed = 1
			the_user = User.objects.get(id=client_account_id)
			the_tag = Tag.objects.get(tagName=tagName)
			newFollow = Follow.objects.create(user=the_user,followTagName=the_tag)
			print(newFollow)
			newFollow.save()
		else:
			pass
		finally:
			pass

	res_dict = dict(isFollow=isFollowed)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)