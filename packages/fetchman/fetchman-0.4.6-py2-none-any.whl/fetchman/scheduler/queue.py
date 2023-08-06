#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import redis
from fetchman.scheduler.bloom_filter import BloomFilter
from fetchman.utils.reqser import request_to_dict, request_from_dict
from fetchman.settings import default_settings

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    import cPickle
else:
    import pickle as cPickle


class Base(object):
    """Per-spider base queue class"""

    def __init__(self, processor):
        self.task_id = processor.spider_id
        self.processor = processor
        self._filter = BloomFilter(key=self.task_id)
        self._server = redis.StrictRedis(host=default_settings.REDIS_HOST, port=default_settings.REDIS_PORT)

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, request):
        """Push a request"""
        raise NotImplementedError

    def pop(self):
        """Pop a request"""
        raise NotImplementedError

    def clear_queue(self):
        self._server.delete(self.task_id)

    def clear_filter(self):
        keys = self._server.keys(self.task_id + '*')
        for key in keys:
            if key != self.task_id:
                self._server.delete(key)

    def clear(self):
        keys = self._server.keys(self.task_id + '*')
        for key in keys:
            self._server.delete(key)


class PriorityQueue(Base):
    def get_pipe(self):
        return self._server.pipeline()

    def push_pipe(self, request, pipe):
        score = -request.priority
        d = request_to_dict(request, self.processor)
        data = cPickle.dumps(d, protocol=-1)
        del d['meta']
        filter_data = cPickle.dumps(d, protocol=-1)
        if not request.duplicate_remove:
            pipe.execute_command('ZADD', self.task_id, score, data)
        else:
            if not self._filter.is_contains(filter_data):
                pipe.execute_command('ZADD', self.task_id, score, data)
                self._filter.insert(filter_data)

    def push(self, request):
        score = -request.priority
        d = request_to_dict(request, self.processor)
        data = cPickle.dumps(d, protocol=-1)
        del d['meta']
        filter_data = cPickle.dumps(d, protocol=-1)
        if not request.duplicate_remove:
            self._server.execute_command('ZADD', self.task_id, score, data)
        else:
            if not self._filter.is_contains(filter_data):
                self._server.execute_command('ZADD', self.task_id, score, data)
                self._filter.insert(filter_data)

    def pop(self):
        pipe = self._server.pipeline()
        pipe.multi()
        pipe.zrange(self.task_id, 0, 0).zremrangebyrank(self.task_id, 0, 0)
        results, count = pipe.execute()
        if results:
            return request_from_dict(cPickle.loads(results[0]), self.processor)
        else:
            return None

    def __len__(self):
        return self._server.zcard(self.task_id)
