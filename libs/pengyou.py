#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Python SDK for pengyou Open API
@author: dev.opensns@qq.com
@license: copyright © 2010, Tencent Corporation. All rights reserved.
@version: 1.0.0
@attention:本SDK依赖于json/simplejson，请先下载安装json/simplejson。
'''

import copy
import urllib,urllib2
from random import choice
import socket

try:
    import json
except ImportError:
    import simplejson as json

PYO_HTTP_TRANSLATE_ERROR = 2001


class pengyou(object):
    '''
    提供访问腾讯朋友社区（QQ校友） OpenAPI 的接口
    '''
    _appid = 0
    _appkey = ''
    _appname = ''
    _iplist = ['openapi.pengyou.qq.com',]

    def __init__(self,appid,appkey,appname,iplist=None):
        '''
        初始化一个朋友社区（QQ校友）应用
        @param appId:应用的ID
        @param appKey:应用的密钥
        @param appName:应用的英文名
        @param iplist:API服务器的IP地址列表或域名列表
        '''
        self._appid = appid
        self._appkey = appkey
        self._appname = appname
        if iplist is not None and len(iplist)>0:
            self._iplist = copy.deepcopy(iplist)

    def _api(self,url,params):
        '''
        执行API调用，返回结果JSON串
        '''
        req = urllib2.Request(url)
        en_params = urllib.urlencode(params)
        try:
            data = urllib2.urlopen(req,en_params).read()
        except:
            return {'ret':PYO_HTTP_TRANSLATE_ERROR,'msg':'urllib2 error'}
        else:
            return json.loads(data)

###############################################################################     
#                        以下是用户需要调用的函数接口
###############################################################################
        
    def getUserinfo(self,openid,openkey):
        '''
        返回当前登录用户信息
        @param openid:与APP通信的用户key，它和QQ号码一一对应                    
        @param openkey:访问OpenAPI时的session key           
        @return:用户信息
            - ret : 返回码 (0:正确返回, [1000,~]错误)
            - nickname : 昵称
            - gender : 性别
            - province : 省
            - city : 市
            - figureurl : 头像url
            - is_vip : 是否黄钻用户 (true|false)
            - is_year_vip : 是否年费黄钻(如果is_vip为false, 那is_year_vip一定是false)
            - vip_level : 黄钻等级(如果是黄钻用户才返回此字段)
        '''
        params = {
                'appid':self._appid,
                'appkey':self._appkey,
                'ref':self._appname,
                'openid':openid,
                'openkey':openkey,
                }
        url = 'http://%s/cgi-bin/xyoapp/xyoapp_get_userinfo.cgi' % (choice(self._iplist))
        return self._api(url,params)


    def isFriend(self,openid,openkey,fopenid):
        '''
        验证是否好友(验证 fopenid 是否是 openid 的好友)
        @param openid:与APP通信的用户key，它和QQ号码一一对应                   
        @param openkey:访问OpenAPI时的session key  
        @param fopenid:待验证用户的openid
        @return:验证结果
                - ret : 返回码 (0:正确返回, [1000,~]错误)
                - isFriend : 是否为好友(0:不是好友; 1:是好友; 2:是同班同学)
        '''
        params = {
                'appid':self._appid,
                'appkey':self._appkey,
                'ref':self._appname,
                'openid':openid,
                'openkey':openkey,
                'fopenid':fopenid,
                }
        url = 'http://%s/cgi-bin/xyoapp/xyoapp_get_isrelation.cgi' % (choice(self._iplist))
        return self._api(url,params)

    def getFriendList(self,openid,openkey,apped=1,infoed=0,page=0):
        '''
        获取好友列表
        @param openid:与APP通信的用户key，它和QQ号码一一对应                   
        @param openkey:访问OpenAPI时的session key  
        @param infoed:是否需要好友的详细信息(0:不需要;1:需要)
        @param apped:对此应用的安装情况(-1:没有安装;1:安装了的;0:所有好友)
        @param page:获取对应页码的好友列表，从1开始算起，每页是100个好友。(不传或者0：返回所有好友;>=1，返回对应页码的好友信息)
        @return:好友关系链的信息
                - ret : 返回码 (0:正确返回; (0,1000):部分数据获取错误,相当于容错的返回; [1000,~]错误)
                - items : 1-n个好友的用户信息
                - openid : 好友QQ号码转化得到的id
                - nickname : 昵称(infoed==1时返回)
                - gender : 性别(infoed==1时返回)
                - figureurl : 头像url(infoed==1时返回)
        '''
        params = {
                'appid':self._appid,
                'appkey':self._appkey,
                'ref':self._appname,
                'openid':openid,
                'openkey':openkey,
                'apped':apped,
                'infoed':infoed,
                'page':page,
                }
        url = 'http://%s/cgi-bin/xyoapp/xyoapp_get_relationinfo.cgi' % (choice(self._iplist))
        return self._api(url,params)

    def getMutilInfo(self,openid,openkey,fopenids):
        '''
        批量获取用户详细信息
        @param openid:与APP通信的用户key，它和QQ号码一一对应                   
        @param openkey:访问OpenAPI时的session key  
        @param fopenids:需要获取数据的openid列表
        @return:好友详细信息
                - ret : 返回码 (0:正确返回; (0,1000):部分数据获取错误,相当于容错的返回; [1000,~]错误)
                - items : 1-n个好友的详细信息
                        - openid : 好友的 OPENID
                        - nickname :昵称
                        - gender : 性别
                        - figureurl : 头像url
                        - is_vip : 是否黄钻 (true:黄钻; false:普通用户)
                        - is_year_vip : 是否年费黄钻 (is_vip为true才显示)
                        - vip_level : 黄钻等级 (is_vip为true才显示)
        '''
        params = {
                'appid':self._appid,
                'appkey':self._appkey,
                'ref':self._appname,
                'openid':openid,
                'openkey':openkey,
                'fopenids':'_'.join(fopenids),
                }
        url = 'http://%s/cgi-bin/xyoapp/xyoapp_multi_info.cgi' % (choice(self._iplist))
        return self._api(url,params)

    def isSetup(self,openid,openkey):
        '''
        验证登录用户是否安装了应用
        @param openid:与APP通信的用户key，它和QQ号码一一对应                   
        @param openkey:访问OpenAPI时的session key  
        @return:验证结果
                - ret : 返回码 (0:正确返回; (0,1000):部分数据获取错误,相当于容错的返回; [1000,~]错误)
                - setuped : 是否安装(0:没有安装;1:安装)
        '''
        params = {
                'appid':self._appid,
                'appkey':self._appkey,
                'ref':self._appname,
                'openid':openid,
                'openkey':openkey,
                }
        url = 'http://%s/cgi-bin/xyoapp/xyoapp_get_issetuped.cgi' % (choice(self._iplist))
        return self._api(url,params)

    def isVip(self,openid,openkey):
        '''
        判断用户是否为黄钻
        @param openid:与APP通信的用户key，它和QQ号码一一对应                   
        @param openkey:访问OpenAPI时的session key  
        @return:判断结果
                - ret: 返回码 (0:正确返回; (0,1000):部分数据获取错误,相当于容错的返回; [1000,~]错误)
                - is_vip:是否黄钻 (true:黄钻; false:普通用户)
        '''
        params = {
                'appid':self._appid,
                'appkey':self._appkey,
                'ref':self._appname,
                'openid':openid,
                'openkey':openkey,
                }
        url = 'http://%s/cgi-bin/xyoapp/xyoapp_pay_showvip.cgi' % (choice(self._iplist))
        return self._api(url,params)

    def getEmotion(self,openid,openkey,fopenids):
        '''
        批量获取好友的签名信息
        @param openid:与APP通信的用户key，它和QQ号码一一对应                   
        @param openkey:访问OpenAPI时的session key  
        @param fopenids:需要获取数据的openid列表(一次最多20个)
        @return:好友签名信息
                - ret : 返回码 (0:正确返回; (0,1000):部分数据获取错误,相当于容错的返回; [1000,~]错误)
                - items :1-n (n<=20)个好友的签名信息
                        - openid: 好友QQ号码转化得到的id
                        - content: 好友的校友心情内容
        '''
        params = {
                'appid':self._appid,
                'appkey':self._appkey,
                'ref':self._appname,
                'openid':openid,
                'openkey':openkey,
                'fopenids':'_'.join(fopenids),
                }
        url = 'http://%s/cgi-bin/xyoapp/xyoapp_get_emotion.cgi' % (choice(self._iplist))
        return self._api(url,params)


if __name__ == '__main__':
    socket.setdefaulttimeout(5)

    appid = 18157
    appkey = '3f1e158d8cf94a26a3131cda7ed92f99'
    appname = 'app18157'

    openid = '0000000000000000000000000FB01EE6'
    openkey = '5F29C898CF52F31E5CDA77D5FAAF9963C9F4298AED680FB6'

    api = pengyou(appid,appkey,appname,('openapi.pengyou.qq.com',))

    jsondata = api.getUserinfo(openid,openkey)
    data = json.dumps(jsondata,ensure_ascii=False)
    print data

    fopenid = ''
    jsondata = api.isFriend(openid,openkey,fopenid)
    data = json.dumps(jsondata,ensure_ascii=False)
    print data

    jsondata = api.isSetup(openid,openkey)
    data = json.dumps(jsondata,ensure_ascii=False)
    print data

    jsondata = api.isVip(openid,openkey)
    data = json.dumps(jsondata,ensure_ascii=False)
    print data

    jsondata = api.getFriendList(openid,openkey,1,1)
    data = json.dumps(jsondata,ensure_ascii=False)
    print data
    openidlist = []
    if jsondata['ret'] == 0:
        openidlist = [fid['openid'] for fid in jsondata['items']]

    jsondata = api.getMutilInfo(openid,openkey,openidlist[0:99])
    data = json.dumps(jsondata,ensure_ascii=False)
    print data

    jsondata = api.getEmotion(openid,openkey,openidlist[0:99])
    data = json.dumps(jsondata,ensure_ascii=False)
    print data
