#! --*-- coding: utf-8 --*--

__author__ = 'kongliang'

# 解析data.pak文件

import sys
import struct


def read_file(filename, encoding):
    """

    :param filename:
    :param encoding:
    :return:
    """
    mode = 'rb' if encoding == 0 else 'rU'
    with open(filename, mode) as f:
        data = f.read()
    if encoding not in (0, 1):
        data = data.decode(encoding)
    return data


PACK_FILE_VERSION = 4
HEADER_LENGTH = 2 * 4 + 1   # Two uint32s. (file version, number of entries) and one uint8 (encoding of text resources)


def analysis_pak(filename):
    data = read_file(filename, 0)
    original_data = data

    # Read the header.
    version, num_entries, encoding = struct.unpack("<IIB", data[:HEADER_LENGTH])
    if version != PACK_FILE_VERSION:
        print "Wrong file version in ", filename, version, PACK_FILE_VERSION
        raise ""
    print version, num_entries, encoding
    resources = {}
    if num_entries == 0:
        return ""

    # Read the index and data.
    data = data[HEADER_LENGTH:]
    kIndexEntrySize = 2 + 4  # Each entry is a uint16 and a uint32.
    for _ in range(num_entries):
        id, offset = struct.unpack("<HI", data[:kIndexEntrySize])
        data = data[kIndexEntrySize:]
        next_id, next_offset = struct.unpack("<HI", data[:kIndexEntrySize])
        resources[id] = original_data[offset:next_offset]
        filetype = 'bin'
        fileheader = ''.join(original_data[offset:offset + 1])
        print ord(fileheader[0])
        if fileheader == '<':
            filetype = 'html'
        if fileheader == '\x89':
            filetype = 'png'
        elif fileheader == '/':
            filetype = 'js'
        of = open('{0}.{1}'.format(id, filetype), 'wb')
        of.write(original_data[offset:next_offset])
        of.close()


if __name__ == '__main__':
    print sys.argv
    if len(sys.argv) > 1:
        analysis_pak(sys.argv[1])
