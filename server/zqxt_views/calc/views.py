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
from calc.models import Order
from calc.models import Comment
import datetime
import jwt
import json
from django.core import serializers
from datetime import datetime
import time
import uuid
import random

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
	client_access_token = request.GET['access_token']
	client_account_id = request.GET['account_id']
	user_all_labels = list(Label.objects.filter(user__id=request_user_id))
	print(user_all_labels)
	labels_all_dict = list()
	if(verify_token(client_access_token)):
		for labels in user_all_labels:
			# 获取该用户是否已收藏这些标签
			isStarted = 0
			try:
				tmpStar = Star.objects.get(user__id=client_account_id,label__labelName=labels.labelName)
				if tmpStar:
					isStarted = 1
			except Exception as e:
				isStarted = 0
			else:
				pass
			finally:
				pass
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
			eve_dict = dict(id=labels.labelNum,isStared=isStarted,name=labels.labelName,desc=labels.labelDes,service=serviceNames,post=postObjects)
			labels_all_dict.append(eve_dict)
	
	
	res_json = json.dumps(labels_all_dict)
	return HttpResponse(res_json)

def getLabelServices(request):
	userId = request.GET['userId']
	res_dict = list()
	user_all_labels = list(Label.objects.filter(user__id=userId))
	for labels in user_all_labels:
		label_all_service = list(Service.objects.filter(label__labelNum=labels.labelNum))
		label_serviceList = list()
		for services in label_all_service:
			imgList = list()
			service_all_pic = list(ServicePicture.objects.filter(service__serviceNum=services.serviceNum))
			for pics in service_all_pic:
				imgDict = dict(imageUrl=pics.url)
				imgList.append(imgDict)
			eve_service = dict(name=services.serviceName,price=services.price,description=services.serviceDes,imageList=imgList,serviceId=services.serviceNum)
			label_serviceList.append(eve_service)
		eve_dict = dict(label=labels.labelName,service=label_serviceList)
		res_dict.append(eve_dict)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def getServiceDetail(request):
	serviceId = request.GET['serviceId']
	res_dict = dict()
	the_service = Service.objects.get(serviceNum=serviceId)
	service_seller = the_service.label.user
	service_comments = list(Comment.objects.filter(order__service=the_service))
	commentNumbers = len(service_comments)
	service_all_pic = list(ServicePicture.objects.filter(service__serviceNum=the_service.serviceNum))
	imgList = list()
	for pics in service_all_pic:
		imgDict = dict(imageUrl=pics.url)
		imgList.append(imgDict)
	res_dict = dict(sellerAvatar=service_seller.avatar,sellerName=service_seller.nickname,serviceName=the_service.serviceName,servicePrice=the_service.price,serviceDesc=the_service.serviceDes,imgList=imgList,serviceDetail=the_service.serviceDetail,commentNum=commentNumbers)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def getComment(request):
	serviceId = request.GET['serviceId']
	res_dict = list()
	the_service = Service.objects.get(serviceNum=serviceId)
	service_seller = the_service.label.user
	service_comments = list(Comment.objects.filter(order__service=the_service))	
	for comment in service_comments:
		comment_user = comment.user
		eve_dict = dict(user=comment_user.nickname,userAvatar=comment_user.avatar,type=comment.commentType,time=comment.time.strftime("%Y-%m-%d %H:%M:%S"),desc=comment.desc)
		res_dict.append(eve_dict)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def submitTheOrder(request):
	client_access_token = request.POST['access_token']
	client_account_id = request.POST['account_id']
	serviceId = request.POST['serviceId']
	the_service = Service.objects.get(serviceNum=serviceId)
	if(verify_token(client_access_token)):
		the_user = User.objects.get(id=client_account_id)
		newOrder = Order()
		newOrder.service = the_service
		newOrder.user = the_user
		newOrder.status = 0
		newOrder.createTime = datetime.now()
		newOrder.serviceTime = datetime.now()
		newOrder.completeTime = datetime.now()
		newOrder.save()
	return HttpResponse('ok')

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
			label_user_id = stars.label.user.id
			label_user_avatar = stars.label.user.avatar
			label_name = stars.label.labelName
			label_des = stars.label.labelDes
			label_id = stars.label.labelNum
			eve_label = dict(labelType=label_types,name=label_user_name,imgUrl=label_user_avatar,label=label_name,description=label_des,labelId=label_id,userId=label_user_id)
			labelList.append(eve_label)
		for i in range(len(labelList)):
			label_type = labelList[i]['labelType']
			tagList = list()
			for j in range(i,len(labelList)):
				if(labelList[j]['labelType']==label_type):
					tagList.append(dict(name=labelList[j]['name'],imgUrl=labelList[j]['imgUrl'],labelId=labelList[j]['labelId'],label=labelList[j]['label'],description=labelList[j]['description'],userId=labelList[j]['userId']))
			eve_dict = dict(type=label_type,labelList=tagList)
			isRepeat = False
			if(len(res_dict)>0):
				for dicts in res_dict:
					if(eve_dict['type']==dicts['type']):
						isRepeat = True
						print(eve_dict)
			if(isRepeat==False):
				res_dict.append(eve_dict)

		print(res_dict)	
		
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

def changeStarStatus(request):
	client_access_token = request.GET['access_token']
	client_account_id = request.GET['account_id']
	labelId = request.GET['labelId']
	isStared = 1
	if(verify_token(client_access_token)):
		try:
			tmpStar = Star.objects.get(user__id=client_account_id,label__labelNum=labelId)
			print(tmpStar)
			if tmpStar:
				print('will delete')
				tmpStar.delete()
				isStared = 0
			if not tmpStar:
				print('will add')
				the_user = User.objects.get(id=client_account_id)
				the_label = Label.objects.get(labelNum=labelId)
				newLabel = Label.objects.create(user=the_user,label=the_label)
				print(newLabel)
				newLabel.save()
		except Exception as e:
			isStared = 1
			the_user = User.objects.get(id=client_account_id)
			the_label = Label.objects.get(labelNum=labelId)
			newStar = Star.objects.create(user=the_user,label=the_label)
			print(newStar)
			newStar.save()
		else:
			pass
		finally:
			pass

	return HttpResponse('ok')

def deleteStar(request):
	client_access_token = request.GET['access_token']
	client_account_id = request.GET['account_id']
	deleteList = list()
	selectList = request.GET['selectList']
	selectList = selectList[1:-1]
	selectList = selectList.replace('"', '')
	deleteList = selectList.split(',')
	print(selectList)
	print(deleteList)
	if(verify_token(client_access_token)):
		for labelId in deleteList:
			tmpStar = Star.objects.get(user__id=client_account_id,label__labelNum=labelId)
			tmpStar.delete()
	return HttpResponse('ok')


def getLabelOfTag(request):
	res_dict = list()
	tagName = request.GET['tagName']
	tag_all_labels = list(Label.objects.filter(tag__tagName=tagName))
	for labels in tag_all_labels:
		label_all_posts = list(Post.objects.filter(label__labelNum=labels.labelNum))
		imageList = list()
		for posts in label_all_posts:
			post_pictures = list(PostPicture.objects.filter(post__postNum=posts.postNum))
			for pics in post_pictures:
				imgDict = dict(imageUrl=pics.url)
				if(len(imageList)<=3):
					imageList.append(imgDict)
		eve_dict = dict(name=labels.user.nickname,tag=labels.labelName,imgUrl=labels.user.avatar,userdesc=labels.user.user_des,desc=labels.labelDes,imageList=imageList,userId=labels.user.id)
		res_dict.append(eve_dict)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def getOrders(request):
	client_access_token = request.GET['access_token']
	client_account_id = request.GET['account_id']
	res_dict = list()
	if(verify_token(client_access_token)):
		user_all_orders = list(Order.objects.filter(user__id=client_account_id))
		for orders in user_all_orders:
			seller = orders.service.label.user
			servicePics = list(ServicePicture.objects.filter(service__serviceNum=orders.service.serviceNum))
			servicePic = servicePics[0].url
			eve_dict = dict(user=seller.nickname,userAvatar=seller.avatar,orderId=str(orders.orderId),status=orders.status,serviceName=orders.service.serviceName,servicePrice=orders.service.price,servicePic=servicePic)
			res_dict.append(eve_dict)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def getOrderDetail(request):
	client_access_token = request.GET['access_token']
	client_account_id = request.GET['account_id']
	orderIdstr = request.GET['orderId']
	orderId = uuid.UUID(orderIdstr)
	res_dict = dict()
	
	if(verify_token(client_access_token)):
		the_order = Order.objects.get(orderId=orderId)
		seller = the_order.service.label.user
		servicePics = list(ServicePicture.objects.filter(service__serviceNum=the_order.service.serviceNum))
		servicePic = servicePics[0].url
		order_dict = dict(orderStatus=the_order.status,sellerAvatar=seller.avatar,sellerName=seller.nickname,serviceName=the_order.service.serviceName,servicePrice=the_order.service.price,servicePic=servicePic,createTime=the_order.createTime.strftime("%Y-%m-%d %H:%M:%S"),serviceTime=the_order.serviceTime.strftime("%Y-%m-%d %H:%M:%S"),completeTime=the_order.completeTime.strftime("%Y-%m-%d %H:%M:%S"))
		comment_dict = dict()
		try:
			the_comment = Comment.objects.get(order__orderId=the_order.orderId)
			comment_dict = dict(time=the_comment.time.strftime("%Y-%m-%d %H:%M:%S"),desc=the_comment.desc,commentType=the_comment.commentType)
		except Exception as e:
			pass
		else:
			pass
		finally:
			pass

		res_dict = dict(order=order_dict,comment=comment_dict)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def changeOrderStatus(request):
	client_access_token = request.POST['access_token']
	client_account_id = request.POST['account_id']
	orderIdstr = request.POST['orderId']
	orderId = uuid.UUID(orderIdstr)
	orderStatus = request.POST['orderStatus']
	if(verify_token(client_access_token)):
		the_order = Order.objects.get(orderId=orderId)
		the_order.status = orderStatus
		the_order.save()
	return HttpResponse('ok')

def deleteTheOrder(request):
	client_access_token = request.POST['access_token']
	client_account_id = request.POST['account_id']
	orderIdstr = request.POST['orderId']
	orderId = uuid.UUID(orderIdstr)
	if(verify_token(client_access_token)):
		the_order = Order.objects.get(orderId=orderId)
		the_order.delete()

	return HttpResponse('ok')

def submitComment(request):
	client_access_token = request.POST['access_token']
	client_account_id = request.POST['account_id']
	orderIdstr = request.POST['orderId']
	orderId = uuid.UUID(orderIdstr)
	commentDes = request.POST['commentDes']
	orderStatus = request.POST['orderStatus']
	commentTypeInt = request.POST['commentType']
	res_dict = dict()
	print(commentTypeInt)
	print(type(commentTypeInt))
	commentType = False
	if(commentTypeInt=='1'):
		commentType = True
	print(commentType)
	if(verify_token(client_access_token)):
		the_order = Order.objects.get(orderId=orderId)
		the_order.status = orderStatus
		the_order.save()
		the_user = User.objects.get(id=client_account_id)
		new_comment = Comment.objects.create(order=the_order,user=the_user,commentType=commentType,time=datetime.now(),desc=commentDes)
		res_dict = dict(commentTime=new_comment.time.strftime("%Y-%m-%d %H:%M:%S"))
		new_comment.save()
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def getSearchResult(request):
	searchValue = request.GET['searchValue']
	searchType = request.GET['searchType']
	res_dict = list()
	match_labels = list(Label.objects.filter(labelName__icontains=searchValue))
	match_services = list(Service.objects.filter(serviceName__icontains=searchValue))
	for services in match_services:
		match_labels.append(services.label)
	print(match_labels)
	for labels in match_labels:
		labels.tag.tagSearchNum = labels.tag.tagSearchNum + 1
		labels.tag.save()
		label_all_posts = list(Post.objects.filter(label__labelNum=labels.labelNum))
		imageList = list()
		for posts in label_all_posts:
			post_pictures = list(PostPicture.objects.filter(post__postNum=posts.postNum))
			for pics in post_pictures:
				imgDict = dict(imageUrl=pics.url)
				if(len(imageList)<=3):
					imageList.append(imgDict)
		eve_dict = dict(name=labels.user.nickname,tag=labels.labelName,imgUrl=labels.user.avatar,userdesc=labels.user.user_des,desc=labels.labelDes,imageList=imageList,userId=labels.user.id,labelId=labels.labelName)
		res_dict.append(eve_dict)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)

def getHotSearch(request):
	res_dict = list()
	sortedTags = list(Tag.objects.order_by("tagSearchNum"))
	hotTags = sortedTags[:20]
	returnTags = random.sample(hotTags, 7)
	for tags in returnTags:
		eve_dict = dict(tagId=tags.tagNum,tagName=tags.tagName)
		res_dict.append(eve_dict)
	res_json = json.dumps(res_dict)
	return HttpResponse(res_json)
