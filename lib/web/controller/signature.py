#!/usr/bin/env python
# coding:utf-8
import _env  # noqa
from hashlib import md5
from solo.config import SECRET
import json


def signature_verify(data, signature, secret=SECRET):
    return signature == make_signature(data, secret=SECRET)


def make_signature(data, secret=SECRET):
    # FIXME: 并不支持JSON嵌套的情况
    '''计算给定数据的签名.

    将data进行urlencode, 按&切割后升序排序, 加上密钥算一个md5值并返回.
    注意, 并不支持json嵌套的情况.

    :param data:
    :param secret:
    '''
    args = []
    for key, value in data.items():
        args.append("%s=%s" % (key,
                               json.dumps(
                                   value,
                                   ensure_ascii=False,
                                   separators=(',', ':')
                               )
                               ))
    args = sorted(args)
    unsign_str = "&".join(args)
    m = md5()
    m.update(unsign_str)
    m.update(secret)
    return m.hexdigest()

if __name__ == '__main__':
    data = {
          "openid": 296116011,
          "username": "Mush Mo",
          "platform": 3,
          "avatar_url": "http://cdn.v2ex.co/avatar/99e9/63b0/70404_large.png",
          "email": "mush@pandorica.io",
          "gender": 1,
          "description": "Dolore maiores unde est quas. Natus velit fugiat laudantium repellat dolore nihil. Suscipit cumque voluptatem molestiae doloremque accusamus voluptas. Ut in dignissimos ut ea voluptas magni est.",
          "location": "Beijing"
    }
    print '"signature": "%s"' % make_signature(data, SECRET)
    print json.dumps(data)
