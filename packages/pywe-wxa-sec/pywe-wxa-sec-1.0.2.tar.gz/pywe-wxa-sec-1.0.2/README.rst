============
pywe-wxa-sec
============

Wechat MiniProgram Security Module for Python.

Sandbox
=======

* https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login

Installation
============

::

    pip install pywe-wxa-sec


Usage
=====

::

    from pywe_wxa_sec.pywxasec import Security, msg_sec_check, img_sec_check


Method
======

::

    class Security(BaseToken):
        def __init__(self, appid=None, secret=None, token=None, storage=None):
            super(Security, self).__init__(appid=appid, secret=secret, token=token, storage=storage)

    def img_sec_check(self, media_file=None, media_file_path=None, appid=None, secret=None, token=None, storage=None):

    def msg_sec_check(self, content, appid=None, secret=None, token=None, storage=None):

