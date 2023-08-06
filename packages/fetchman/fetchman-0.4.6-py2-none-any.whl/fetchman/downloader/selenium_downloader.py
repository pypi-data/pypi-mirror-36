#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from fetchman.settings import default_settings
from fetchman.downloader.base_downloder import BaseDownLoader
from fetchman.downloader.http.selenium_response import SeleniumResponse
from fetchman.downloader.web_driver_pool import get_web_driver_pool
from fetchman.utils import FetchManLogger
from multiprocessing.pool import ThreadPool as Pool

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class SeleniumDownLoader(BaseDownLoader):
    def __init__(self, driver_pool_size=None):
        self.driver_pool_size = driver_pool_size
        FetchManLogger.logger.info("init web driver pool...")
        if driver_pool_size:
            self.web_driver_pool = get_web_driver_pool(driver_pool_size)
        else:
            self.web_driver_pool = get_web_driver_pool(default_settings.DRIVER_POOL_SIZE)
        FetchManLogger.logger.info("init web driver pool success")

    def download_one(self, request):
        web = self.web_driver_pool.get()  # type:WebDriver
        web.get(request.url)
        m_response = m_object()
        m_response.content = web.execute_script("return document.documentElement.outerHTML")
        response = SeleniumResponse(m_response=m_response, request=request)
        self.web_driver_pool.put(web)
        return response

    def download(self, batch):
        if self.driver_pool_size:
            pool = Pool(processes=self.driver_pool_size)
        else:
            pool = Pool(processes=default_settings.DRIVER_POOL_SIZE)

        results = []

        for request in batch:
            results.append(pool.apply_async(self.download_one, (request,)))
        pool.close()
        pool.join()

        true_responses = []
        for result in results:
            true_response = result.get()
            true_responses.append(true_response)
            FetchManLogger.logger.info(true_response)

        return true_responses


class m_object(object):
    pass
