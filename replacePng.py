#!/usr/bin/env python
# coding:utf8

import time
import os
import tarfile
import cPickle as p
import hashlib
import urllib2
from zlib import crc32
from subprocess import Popen, PIPE
import subprocess
import re
import requests
import base64
from shutil import copyfile

def remove(src_dir):
    for root, folders, files in os.walk(src_dir):
        for fname in files:
            print root
            if fname.endswith('.meta')| fname.endswith('.anim')|fname.endswith('.prefab')|fname.endswith('.fnt'):
                fullname = os.path.join(root, fname)
                print fullname
                os.remove(fullname)



def scan(src_dir, dst_dir):

    src_png_listname = []
    src_png_listpath = []
    for root, folders, files in os.walk(src_dir):
        # print root, folders, files
        for fname in files:
            if not fname.endswith('.png'):
                continue
            fullname = os.path.join(root, fname)
            src_png_listname.append(fname)
            src_png_listpath.append(fullname)

            # remove_dir_file = fullname[len(src_dir):]
            # dist_dir_file = dst_dir + remove_dir_file
            # print '-----------------------------'
            # print dist_dir_file,fullname
            # copyfile(fullname, dist_dir_file)
    # print src_png_listname
    # print src_png_listpath

    for aroot,folders,afiles in os.walk(dst_dir):
        for fname in afiles:
            if fname.endswith('.png'):
                for i in range(len(src_png_listname)):
                    if fname == src_png_listname[i]:
                        dirfullname = os.path.join(aroot,fname)
                        print src_png_listpath[i]
                        print dirfullname
                        print '--------------------------------'
                        copyfile(src_png_listpath[i],dirfullname)
if __name__ == '__main__':
    # remove('/Users/lz/Desktop/tank')
    # scan("/Users/lz/Desktop/h5game/sanguo/", "/Users/lz/Desktop/h5game/K8ClientBanHao2_kehuan_sanguo/Assets/Res/")
    scan('/Users/lz/Desktop/h5game/tan_ke_fight/tank_1/','/Users/lz/Desktop/h5game/tan_ke_fight/xiangmu/TankBanHao/assets/resources/')