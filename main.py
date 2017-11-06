# _*_ coding:utf-8 _*_
__author__ = 'daemonshao'
__date__ = '2017/10/7 15:36'

import os
import sys

from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","wanmei"])