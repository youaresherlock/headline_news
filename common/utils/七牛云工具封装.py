#!usr/bin/python
# -*- coding:utf8 -*-
import qiniu.config
from qiniu import Auth, put_data, etag


def upload_file(data):
    """
    七牛云上传文件
    :param data: 上传的二进制数据
    :return: 七牛云上的文件名
    """
    # 需要填写你的 Access Key 和 Secret Key
    access_key = 'kJ8wVO7lmFGsdvtI5M7eQDEJ1eT3Vrygb4SmR00E'
    secret_key = 'rGwHyAvnlLK7rU4htRpNYzpuz0OHJKzX2O1LWTNl'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'sh31'

    # 上传后保存的文件名
    key = None  # 如果设置为None,七牛云会自动给文件起名

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    ret, info = put_data(token, key, data)
    if info.status_code == 200:  # 上传成功
        return 'http://q7f6ieukf.bkt.clouddn.com/' + ret.get('key')  # 返回七牛云上的文件名
    else:
        raise Exception('上传失败')


if __name__ == '__main__':
   with open('cat.jpg', 'rb') as f:
       data = f.read()
       file_url = upload_file(data)
       print(file_url)















