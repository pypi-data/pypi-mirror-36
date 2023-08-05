# -*- coding： utf-8 -*-
# author：pengr

import json
import hashlib
from functools import reduce


class RequestManager(object):
    '''
    请求管理器
    统一管理所有的请求，包括待请求的与已请求的请求。
    '''

    def __init__(self, limit_level=3):
        '''
        请求管理器初始化函数

            @param :: limit_level : 爬取层数限制，默认限制3层
            @member :: level : 当前爬取层数
            @member :: new_requests : 未爬取请求集合，采用字典存储，key对应相应的层数，value相应层数未请求的请求集合
            @member :: old_requests : 已存储请求集合，采用元组存储，每个请求计算128位md5码进行存储
            @member :: limit_level : 爬取层数限制，默认限制3层

        '''
        self.__level = 1
        self.__new_requests = {}
        self.__old_requests = set()
        self.__limit_level = limit_level

    def add_new_requests(self, requests):
        '''
        添加请求集合

            @param :: requests : 待添加请求集合

            return : None

        '''
        if not requests or len(requests) == 0 or not type(requests) == list:
            return
        for request in requests:
            self.add_new_request(request)

    def add_new_request(self, request):
        '''
        添加请求

            @param :: requests : 待添加请求

            return : None

        '''
        if not request or not type(request) == dict:
            raise Exception('please construst right request dict')
        request_str = json.dumps(request)
        if not request_str in self.__old_requests:
            self.__add_new_request(request)
            self.__add_old_request(request_str)

    def has_new_request(self, level=None):
        '''
        判断是否还有待爬取的请求，当传入level后，判断相应的层数中是否还有待爬取的请求。默认判断所有层数

            @param :: level : 待添加请求集合

            return : Bool

        '''
        if level:
            return self.new_requests_size(level) > 0
        return self.new_requests_size() > 0

    def get_new_request(self, level=None):
        '''
        获取一个未被请求过的请求

            @param :: level : 从指定层数中提取，默认为None

            return : request

        '''
        if not self.has_new_request():
            return None
        if not level:
            level = self.__level
        if len(self.__new_requests[str(self.__level)]) <= 1:
            self.__add_level()
        return self.__get_new_request(level)

    def get_level(self,):
        '''
        获取当前层级

            return : int

        '''
        return self.__level

    def new_requests_size(self, level=None):
        '''
        待爬取的请求集合长度

            @param :: level : 获取指定层数的请求集合长度

            return : int

        '''
        if level:
            return self.__new_request_size(level)
        else:
            return sum(map(lambda x: self.__new_request_size(x), self.__new_requests))

    def old_requests_size(self):
        '''
        已请求的请求集合长度

            @param :: level : 获取指定层数的请求集合长度

            return : int

        '''
        return len(self.__old_requests)

    def __add_level(self,):
        '''
        (私有函数)增加当前爬取层数

            return : None

        '''
        self.__level += 1

    def __init_level(self, level):
        '''
        (私有函数)初始化level层的待爬取请求集合

            @param :: level : 指定要初始化的level层

            return : None

        '''
        if not str(level) in self.__new_requests:
            self.__new_requests[str(level)] = set()

    def __add_new_request(self, request):
        '''
        (私有函数)添加请求,向未爬取过的请求集合中添加请求

            @param :: requests : 待添加请求

            return : None

        '''
        if not 'level' in request:
            request['level'] = self.__level
        if not str(self.__level) in self.__new_requests:
            self.__init_level(self.__level)

        if request['level'] > self.__limit_level:
            return

        if not str(request['level']) in self.__new_requests:
            self.__init_level(request['level'])

        request_str = json.dumps(request)
        self.__new_requests[str(request['level'])].add(request_str)

    def __add_old_request(self, request_str):
        '''
        (私有函数)添加请求,向已爬取过的请求集合中添加请求。集合中添加请求文本的128位md5码

            @param :: request_str : 待添加请求文本

            return : None

        '''
        md5 = hashlib.md5()
        md5.update(request_str.encode('utf-8'))
        self.__old_requests.add(md5.hexdigest()[8:-8])

    def __get_new_request(self, level):
        '''
        (私有函数)获取一个未被请求过的请求

            @param :: level : 从指定层数中提取

        '''
        if str(level) in self.__new_requests and self.__new_requests[str(level)]:
            return json.loads(self.__new_requests[str(level)].pop())

    def __new_request_size(self, level):
        '''
        (私有函数)获取level层未爬取的请求集合长度

            @param :: level : 从指定层数中提取

            return : int

        '''
        if str(level) in self.__new_requests:
            return len(self.__new_requests[str(level)])
        return 0
