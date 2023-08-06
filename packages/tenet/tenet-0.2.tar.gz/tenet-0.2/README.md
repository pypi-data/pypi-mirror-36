# TenetAPI

## Description
This is a Python module for work with ISP TeNeT API.

## Usage:
```
>>> from tenet.api import TenetAPI
>>> from tenet.utils import sizeof_fmt
>>> TenetAPI()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "tenet/api.py", line 35, in __init__
    "Usage: TenetAPI(username='user', passcode='pass')"
AssertionError: Usage: TenetAPI(username='user', passcode='pass') or TenetAPI(username='user', md5passcode='hash')
>>> api = TenetAPI(
...     username='user-00000',
...     md5passcode='8b46a9e3095d350b2faeb1c503239b5e'
... )
>>> api.update()
>>> print api.api.account_id
00000
>>> print api.account_state
Normal
>>> print api.account_enabled
True
>>> print api.service_name
Сверхскоростной Интернет и Wi-Fi
>>> print api.saldo
374.60
>>> print api.good_day
False
>>> print api.bonus_state
Enabled
>>> api.toggle_bonus()
>>> print api.bonus_state
Disabled
>>> print sizeof_fmt(api.bonus_rest)
10.0 GiB
```
