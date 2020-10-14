#!usr/bin/python
# -*- coding:utf8 -*-
import imghdr


# with open('123.jpg', 'rb') as f:
#     # 检查文件的类型 一般是比对文件的头部字节
#     content = f.read()
#     print(content)


with open('123.jpg', 'rb') as f:
    # 方式1: 设置第一个参数,传递文件路径/文件对象
    # 如果是图片,返回图片类型,不是图片返回None
    # type = imghdr.what('test.png')
    # type = imghdr.what(f)
    # print(type)

    # 方式2: 设置第二个参数,传递二进制数据
    file_bytes = f.read()
    type = imghdr.what(None, file_bytes)
    print(type)











