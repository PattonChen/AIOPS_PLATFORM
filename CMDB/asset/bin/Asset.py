'''
    Asset.py
    Written By Kyle Chen
    Version 20190316v1
'''

## import buildin pkgs
import sys
import re
import os
import logging
from logging.handlers import RotatingFileHandler

## get workpath
workpath = ""
pathlst = re.split(r"\/", sys.path[0])
max_index = len(pathlst) - 1
i = 0

while i < max_index - 1:
    workpath += pathlst[i] + "/"
    i += 1

workpath += pathlst[i]

## append workpath to path
sys.path.append("%s/lib" % (workpath))

## import priviate pkgs
from Config import Config
from Lock import Lock

## Asset Class
class Asset(object):

    ## initial function
    def __init__(self):

        ## set priviate values
        self.config = Config(workpath)
        self.pid = os.getpid()
        self.pname = 'Asset.py'

        ## logger initial
        self.logger_init()

        ## lock initial
        self.lockObj = Lock(
            self.pname,
            self.pid,
            self.config.LOCK_DIR,
            self.config.LOCK_FILE,
            self.logger)

        ## debug output
        self.logger.debug('Asset Initial Start')
        self.logger.debug('[SYS_CIS][%s]' % (self.config.SYS_CIS))
        self.logger.debug('[LOCK_DIR][%s]' % (self.config.LOCK_DIR))
        self.logger.debug('[LOCK_FILE][%s]' % (self.config.LOCK_FILE))
        self.logger.debug('[LOG_DIR][%s]' % (self.config.LOG_DIR))
        self.logger.debug('[LOG_FILE][%s]' % (self.config.LOG_FILE))
        self.logger.debug('[LOG_LEVEL][%s]' % (self.config.LOG_LEVEL))
        self.logger.debug('[LOG_MAX_SIZE][%s]' % (self.config.LOG_MAX_SIZE))
        self.logger.debug(
            '[LOG_BACKUP_COUNT][%s]' %
            (self.config.LOG_BACKUP_COUNT))
        self.logger.debug('Asset Initial Done')

        ## auto import libs
        CIDict = locals()
        for l in self.config.SYS_CIS:
            print(l)
            CIDict[l] = import('%s.%s'.format(l, l))

        for c in CIDict:
            if c == 'self':
                continue

            CIDict[c].getData()

    ## initial logger
    def logger_init(self):

        self.logger = logging.getLogger("Asset")

        try:
            log_level = getattr(logging, self.config.LOG_LEVEL)
        except BaseException:
            log_level = logging.NOTSET

        self.logger.setLevel(log_level)

        fh = RotatingFileHandler(
            self.config.LOG_FILE,
            mode='a',
            maxBytes=self.config.LOG_MAX_SIZE,
            backupCount=self.config.LOG_BACKUP_COUNT)
        fh.setLevel(log_level)

        ch = logging.StreamHandler()
        ch.setLevel(log_level)

        formatter = logging.Formatter(
            '[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        return(True)

    ## run asset function
    def run(self):

        self.logger.debug('main run func')
        return(True)

    ## destructor function
    def __del__(self):

        ## lock release
        try:
            self.lockObj.lock_release(self.config.LOCK_FILE)

        except Exception as e:
            pass

        return(None)


## run it
assetObj = Asset()
assetObj.run()
