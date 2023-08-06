# TenetAPI

## Description
This is a Python module for the ISP TeNeT API.

## Usage:
```
>>> from tenet import TenetAccount
>>> from tenet.utils import sizeof_fmt
>>> TenetAccount()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "tenet/__init__.py", line 34, in __init__
    "Usage: TenetAccount(username='user', password='pass')"
tenet.exceptions.TenetBaseException: Usage: TenetAccount(username='user', password='pass') or TenetAccount(username='user', md5password='hash')
>>> account = TenetAccount(
...     username='user-00000',
...     md5password='8b46a9e3095d350b2faeb1c503239b5e'
... )
>>> account.update()
>>> print account.id
00000
>>> print account.state
Normal
>>> print account.enabled
True
>>> print account.tariff_plan
Сверхскоростной Интернет и Wi-Fi
>>> print account.saldo
374.60
>>> print account.good_day
False
>>> print account.bonus_state
Enabled
>>> account.toggle_bonus()
>>> print account.bonus_state
Disabled
>>> print sizeof_fmt(account.bonus_rest)
10.0 GiB
```
