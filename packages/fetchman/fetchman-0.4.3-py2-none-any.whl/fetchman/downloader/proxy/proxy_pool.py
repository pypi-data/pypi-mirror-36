#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from fetchman.settings.default_settings import PROXY_PATH_REQUEST

if sys.version_info < (3, 0):
    import Queue
    reload(sys)
    sys.setdefaultencoding('utf-8')
else:
    from queue import Queue


class ProxyPool(object):
    def __init__(self):
        self.queue = Queue.Queue()
        with open(PROXY_PATH_REQUEST, 'r') as f:
            lines = f.readlines()
            self.len = len(lines)
            for line in lines:
                info = line.strip().split(',')
                proxy = {}
                if len(info) == 2:
                    proxy = {"http": "http://%s:%s" % (info[0], info[1]),
                             "https": "http://%s:%s" % (info[0], info[1])}
                elif len(info) == 4:
                    proxy = {"http": "http://%s:%s@%s:%s/" % (info[2], info[3], info[0], info[1]),
                             "https": "http://%s:%s@%s:%s/" % (info[2], info[3], info[0], info[1])}
                self.queue.put(proxy)

    def __len__(self):
        return self.len

    def getProxy(self):
        proxy = self.queue.get()
        self.queue.put(proxy)
        return proxy
