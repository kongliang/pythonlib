#! --*-- coding: utf-8 --*--

__author__ = 'kongliang'

import struct
import numpy
from PIL import Image

from swf.consts import BitmapType


class TagEnd(object):
    TYPE = 0

    def __init__(self, sam, tag):
        self.sam = sam
        self.init(tag)

    @classmethod
    def force_str(cls, message):
        if isinstance(message, unicode):
            return message.encode('utf-8')
        return message

    @property
    def type(self):
        return self.TYPE

    @property
    def tag_len(self):
        return numpy.uint32(0)

    def init(self, tag):
        pass

    def pack(self):
        fmt = 'II'
        buf = struct.pack(fmt, self.type, self.tag_len)
        return buf


class TagHandle(object):
    TYPE = 6

    def __init__(self, sam, tag):
        self.sam = sam
        self.frame_width = numpy.uint32(0)
        self.frame_height = numpy.uint32(0)
        self.frame_rate = numpy.float32(0)
        self.frame_count = numpy.uint32(0)
        self.init(tag)

    @classmethod
    def force_str(cls, message):
        if isinstance(message, unicode):
            return message.encode('utf-8')
        return message

    @property
    def type(self):
        return self.TYPE

    @property
    def tag_len(self):
        return numpy.uint32(self.frame_width.nbytes + self.frame_height.nbytes +
                            self.frame_rate.nbytes + self.frame_count.nbytes)

    def init(self, tag):
        self.frame_width = numpy.uint32((tag.frame_size.xmax - tag.frame_size.xmin)/20.0)
        self.frame_height = numpy.uint32((tag.frame_size.ymax - tag.frame_size.ymin)/20.0)
        self.frame_rate = numpy.float32(tag.frame_rate)
        self.frame_count = numpy.uint32(tag.frame_count)

    def pack(self):
        fmt = '4IfI'
        buf = struct.pack(fmt, self.type, self.tag_len,
                          self.frame_width, self.frame_height, self.frame_rate, self.frame_count)
        return buf


class TagLable(object):
    TYPE = 2

    def __init__(self, sam, tag):
        self.sam = sam
        self.name = ''
        self.init(tag)

    @classmethod
    def force_str(cls, message):
        if isinstance(message, unicode):
            return message.encode('utf-8')
        return message

    @property
    def type(self):
        return self.TYPE

    @property
    def tag_len(self):
        return numpy.uint32(len(self.name) + 1)

    def init(self, tag):
        self.name = self.force_str(tag.frameName)

    def pack(self):
        fmt = '2I%ss' % self.tag_len
        buf = struct.pack(fmt, self.type, self.tag_len, self.name)
        return buf


class TagShow(object):
    TYPE = 5

    def __init__(self, sam, tag):
        self.sam = sam
        self.init(tag)

    @classmethod
    def force_str(cls, message):
        if isinstance(message, unicode):
            return message.encode('utf-8')
        return message

    @property
    def type(self):
        return self.TYPE

    @property
    def tag_len(self):
        return numpy.uint32(0)

    def init(self, tag):
        pass

    def pack(self):
        fmt = '2I'
        buf = struct.pack(fmt, self.type, self.tag_len)
        return buf


class TagImage(object):
    TYPE = 1

    def __init__(self, sam, tag, framename=True):
        self.sam = sam
        self.cid = numpy.uint32(0)
        self.name = ''
        self.init(tag, framename)

    @classmethod
    def force_str(cls, message):
        if isinstance(message, unicode):
            return message.encode('utf-8')
        return message

    @property
    def type(self):
        return self.TYPE

    @property
    def tag_len(self):
        return numpy.uint32(self.cid.nbytes + len(self.name) + 1)

    def init(self, tag, framename):
        self.cid = numpy.uint32(tag.characterId)
        if framename:
            self.name = '%s%s.png' % (self.sam.swf.file_name, self.cid)
            self.sam.framename = self.name
        else:
            self.name = self.sam.framename

    def pack(self):
        fmt = '3I%ss' % (len(self.name) + 1)
        buf = struct.pack(fmt, self.type, self.tag_len, self.cid, self.name)
        return buf


class TagRemove(object):
    TYPE = 4

    def __init__(self, sam, tag):
        self.sam = sam
        self.depth = numpy.uint32(0)
        self.init(tag)

    @classmethod
    def force_str(cls, message):
        if isinstance(message, unicode):
            return message.encode('utf-8')
        return message

    @property
    def type(self):
        return self.TYPE

    @property
    def tag_len(self):
        return numpy.uint32(self.depth.nbytes)

    def init(self, tag):
        self.depth = numpy.uint32(tag.depth)

    def pack(self):
        fmt = '3I'
        buf = struct.pack(fmt, self.type, self.tag_len, self.depth)
        return buf


class TagPlace(object):
    TYPE = 3

    def __init__(self, sam, tag):
        self.sam = sam
        self.cid = numpy.uint32(0)
        self.depth = numpy.uint32(0)
        self.realdepth = numpy.uint32(0)
        self.has_color_transform = numpy.uint32(0)
        self.has_matrix = numpy.uint32(0)
        self.color_transform = {
            'hasAddTerms': numpy.int32(0),
            'hasMultTerms': numpy.int32(0),
            'redMultTerm': numpy.int32(0),
            'greenMultTerm': numpy.int32(0),
            'blueMultTerm': numpy.int32(0),
            'alphaMultTerm': numpy.int32(0),
            'redAddTerm': numpy.int32(0),
            'greenAddTerm': numpy.int32(0),
            'blueAddTerm': numpy.int32(0),
            'alphaAddTerm': numpy.int32(0),
        }
        self.matrix = (
            ('scaleX', numpy.float32(0)),
            ('scaleY', numpy.float32(0)),
            ('rotateSkew0', numpy.float32(0)),
            ('rotateSkew1', numpy.float32(0)),
            ('positionX', numpy.float32(0)),
            ('positionY', numpy.float32(0)),
        )
        self.init(tag)

    @classmethod
    def force_str(cls, message):
        if isinstance(message, unicode):
            return message.encode('utf-8')
        return message

    @property
    def type(self):
        return self.TYPE

    @property
    def tag_len(self):
        base_len = self.cid.nbytes + self.depth.nbytes + self.realdepth.nbytes + \
                   self.has_color_transform.nbytes + self.has_matrix.nbytes
        if self.has_color_transform:
            base_len += sum([value.nbytes for value in self.color_transform.itervalues()])
        if self.has_matrix:
            base_len += sum([value.nbytes for name, value in self.matrix])
        return numpy.uint32(base_len)

    def init(self, tag):
        self.cid = numpy.uint32(tag.characterId)
        self.depth = numpy.uint32(tag.depth)
        self.realdepth = numpy.uint32(tag.depth)
        self.has_color_transform = numpy.uint32(tag.hasColorTransform)
        self.has_matrix = numpy.uint32(tag.hasMatrix)
        if self.has_color_transform:
            self.color_transform = {
                'hasAddTerms': numpy.int32(tag.colorTransform.hasAddTerms),
                'hasMultTerms': numpy.int32(tag.colorTransform.hasMultTerms),
                'redMultTerm': numpy.int32(tag.colorTransform.rMult),
                'greenMultTerm': numpy.int32(tag.colorTransform.gMult),
                'blueMultTerm': numpy.int32(tag.colorTransform.bMult),
                'alphaMultTerm': numpy.int32(tag.colorTransform.aMult),
                'redAddTerm': numpy.int32(tag.colorTransform.rAdd),
                'greenAddTerm': numpy.int32(tag.colorTransform.gAdd),
                'blueAddTerm': numpy.int32(tag.colorTransform.bAdd),
                'alphaAddTerm': numpy.int32(tag.colorTransform.aAdd),
            }
        if self.has_matrix:
            self.matrix = (
                ('scaleX', numpy.float32(tag.matrix.scaleX)),
                ('scaleY', numpy.float32(tag.matrix.scaleY)),
                ('rotateSkew0', numpy.float32(-tag.matrix.rotateSkew0)),
                ('rotateSkew1', numpy.float32(-tag.matrix.rotateSkew1)),
                ('positionX', numpy.float32(tag.matrix.translateX/20.0)),
                ('positionY', numpy.float32(tag.matrix.translateY/20.0)),
            )

    def pack(self):
        fmt = '7I'
        buf = struct.pack(fmt, self.type, self.tag_len, self.cid, self.depth, self.realdepth,
                          self.has_color_transform, self.has_matrix)
        if self.has_matrix:
            buf += struct.pack('6f', *[value for name, value in self.matrix])
        if self.has_color_transform:
            buf += struct.pack('2I', self.color_transform['hasAddTerms'], self.color_transform['hasMultTerms'])
            if self.color_transform['hasMultTerms']:
                buf += struct.pack('4I', self.color_transform['redMultTerm'], self.color_transform['greenMultTerm'],
                                   self.color_transform['blueMultTerm'], self.color_transform['alphaMultTerm'])
            if self.color_transform['hasAddTerms']:
                buf += struct.pack('4I', self.color_transform['redAddTerm'], self.color_transform['greenAddTerm'],
                                   self.color_transform['blueAddTerm'], self.color_transform['alphaAddTerm'])
        return buf


class Display(object):

    def __init__(self):
        self.display_list = []

    def add_display(self, tag):
        if not isinstance(tag, TagPlace):
            tag = TagPlace(self, tag)
        self.display_list.append(tag)
        self.display_list = sorted(self.display_list, key=lambda x: x.depth)

    def remove_display(self, tag):
        index = None
        for k, v in enumerate(self.display_list):
            if v.depth == tag.depth:
                index = k
                break

        if index is not None:
            self.display_list.pop(index)

    def modify_display(self, tag):
        if not isinstance(tag, TagPlace):
            tag = TagPlace(self, tag)
        index = None
        for k, v in enumerate(self.display_list):
            if v.depth == tag.depth:
                index = k
                break

        if index is not None:
            dis_tag = self.display_list[index]
            if tag.has_color_transform:
                dis_tag.color_transform = tag.color_transform
                dis_tag.has_color_transform = tag.has_color_transform
            if tag.has_matrix:
                dis_tag.matrix = tag.matrix
                dis_tag.has_matrix = tag.has_matrix

    def change_display(self, tag):
        if not isinstance(tag, TagPlace):
            tag = TagPlace(self, tag)
        index = None
        for k, v in enumerate(self.display_list):
            if v.depth == tag.depth:
                index = k
                break

        if index is not None:
            dis_tag = self.display_list.pop(index)
            if dis_tag.has_color_transform and not tag.has_color_transform:
                tag.color_transform = dis_tag.color_transform
                tag.has_color_transform = dis_tag.has_color_transform
            if dis_tag.has_matrix and not tag.has_matrix:
                tag.matrix = dis_tag.matrix
                tag.has_matrix = dis_tag.has_matrix
            self.add_display(tag)


class Sam(object):

    def __init__(self, swf):
        self.swf = swf
        self.buf = ''
        self.framename = ''
        self.display = Display()

    @classmethod
    def force_str(cls, message):
        if isinstance(message, unicode):
            return message.encode('utf-8')
        return message

    def write(self):
        f = open('%s.sam' % self.swf.file_path, 'wb')
        f.write(self.buf)
        f.close()

    def analysis(self):
        tag_handle = TagHandle(self, self.swf.header)
        buf = tag_handle.pack()
        self.buf += buf

        for tag in self.swf.tags:
            if tag.type in [69, 9, 86]:
                continue
            if tag.type == 43:
                self.tag_lable(tag)
            elif tag.type == 1:
                self.tag_show(tag)
            elif tag.type == 35:
                self.tag_image_35(tag)
            elif tag.type == 36:
                self.tag_image_36(tag)
            elif tag.type == 2:
                self.tag_image_2(tag)
            elif tag.type == 28:
                self.tag_remove(tag)
            elif tag.type == 26:
                self.tag_place(tag)
            elif tag.type == 0:
                self.tag_end(tag)
                break
            else:
                print 'error tag: ', tag
                break

        self.write()

    def tag_lable(self, tag):
        tag_lable = TagLable(self, tag)
        buf = tag_lable.pack()
        self.buf += buf

        for i in self.display.display_list:
            buf = i.pack()
            self.buf += buf

    def tag_show(self, tag):
        tag_show = TagShow(self, tag)
        buf = tag_show.pack()
        self.buf += buf

    def tag_image_35(self, tag):
        tag_image = TagImage(self, tag)
        buf = tag_image.pack()
        self.buf += buf

        image = Image.open(tag.bitmapData)
        image = image.convert('RGBA')
        tag.bitmapData.seek(0)

        if tag.bitmapType == BitmapType.JPEG:
            width, height = image.size
            tag.bitmapAlphaData.seek(0)
            for h in xrange(height):
                for w in xrange(width):
                    alpha = struct.unpack('b', tag.bitmapAlphaData.read(1))[0]
                    pixel_4 = list(image.getpixel((w, h)))
                    pixel_4[-1] &= alpha
                    image.putpixel((w, h), tuple(pixel_4))
            tag.bitmapAlphaData.seek(0)
            image.save('%s/%s%s.png' % (self.swf.dir_name, self.swf.file_name, tag.characterId), 'png')
        else:
            image.save('%s/%s%s.png' % (self.swf.dir_name, self.swf.file_name, tag.characterId), 'png')

    def tag_image_36(self, tag):
        tag_image = TagImage(self, tag)
        buf = tag_image.pack()
        self.buf += buf

        if tag.im:
            tag.im.save('%s/%s%s.png' % (self.swf.dir_name, self.swf.file_name, tag.characterId), "PNG")

    def tag_image_2(self, tag):
        tag_image = TagImage(self, tag, framename=False)
        buf = tag_image.pack()
        self.buf += buf

    def tag_remove(self, tag):
        tag_remove = TagRemove(self, tag)
        buf = tag_remove.pack()
        self.buf += buf

        self.display.remove_display(tag)

    def tag_place(self, tag):
        tag_place = TagPlace(self, tag)
        buf = tag_place.pack()
        self.buf += buf

        if not tag.hasMove and tag.hasCharacter:
            self.display.add_display(tag)
        elif tag.hasMove and not tag.hasCharacter:
            self.display.modify_display(tag)
        elif tag.hasMove and tag.hasCharacter:
            self.display.change_display(tag)

    def tag_end(self, tag):
        tag_end = TagEnd(self, tag)
        buf = tag_end.pack()
        self.buf += buf