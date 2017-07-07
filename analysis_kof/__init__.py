#! --*-- coding: utf-8 --*--

__author__ = 'kongliang'

# 解析腾讯拳皇98终极之战

import os
import sqlite3
import struct
import shutil


def analysis_reslib():
    path = "/Users/kongliang/Downloads/KingOfFight-iOS"
    s = sqlite3.connect('%s/reslib' % path)

    tables = s.execute("select name from SQLITE_MASTER where type='table'").fetchall()
    table = tables[0][0]
    sql = 'select * from %s' % table

    for name, real_path, size, md5, release_path, _ in s.execute(sql).fetchall():
        release_tr_path = os.path.dirname('%s/release_tr/%s' % (path, real_path))
        if not os.path.exists(release_tr_path):
            os.makedirs(release_tr_path)

        _, suffix = os.path.splitext(real_path)
        basename = os.path.basename(real_path)

        if ".png" == suffix:
            f = open('%s/release/%s' % (path, release_path), 'r')
            data = f.read()
            data1, data2, head = data[0:16], data[16:32], []
            for i in xrange(16):
                k = struct.unpack('!B', data1[i])[0] ^ struct.unpack('!B', data2[i])[0]
                head.append(k)
            h = struct.pack('!16B', *head)
            d = h + data[32:]
            ff = open('%s/%s' % (release_tr_path, basename), 'w')
            ff.write(d)
            ff.close()
            f.close()
        else:
            shutil.copy('%s/release/%s' % (path, release_path),
                        '%s/release_tr/%s' % (path, real_path))


if __name__ == '__main__':
    analysis_reslib()
