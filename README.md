qiidly
==================================================

Qiitaでフォロー中のタグのフィードを、
Feedlyのフォロー（購読）対象として同期します。

Setup
==================================================

```bash
$ pip install -r requirements.txt
```

- [Python Wrapper for Qiita API v2](https://github.com/petitviolet/qiita_py)


Usage
==================================================

```bash
$ python qiidly/qiidly.py -h
usage: qiidly.py [-h] -q QIITA_TOKEN -f FEEDLY_TOKEN

qiidly: Qiita to Feedly.

optional arguments:
  -h, --help            show this help message and exit
  -q QIITA_TOKEN, --qiita-token QIITA_TOKEN
                        Qiita access token
                        (https://qiita.com/settings/applications)
  -f FEEDLY_TOKEN, --feedly-token FEEDLY_TOKEN
                        Feedly developer access token
                        (https://developer.feedly.com/v3/developer/#how-do-i-
                        generate-a-developer-access-token)
$
```


License
==================================================
MIT
