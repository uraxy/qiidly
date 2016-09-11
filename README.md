qiidly
======

[![Build Status](https://travis-ci.org/uraxy/qiidly.svg?branch=master)](https://travis-ci.org/uraxy/qiidly)
[![Code Health](https://landscape.io/github/uraxy/qiidly/master/landscape.svg?style=flat)](https://landscape.io/github/uraxy/qiidly/master)
[![Coverage Status](https://coveralls.io/repos/github/uraxy/qiidly/badge.svg?branch=master)](https://coveralls.io/github/uraxy/qiidly?branch=master)

FeedlyのAndroidアプリは快適！
blogを読むだけじゃもったいない、
Qiitaの新着記事もチェックするともっと快適！

そのためには…
- Qiitaでフォロー中のタグ
- Qiitaでフォロー中のユーザー
をカンタンにFeedlyに同期できなきゃ。

そのためのツールがqiidlyなのだ。

-----

qiidlyは、
Qiitaでフォロー中のタグとユーザーのフィードをFeedlyに同期するツールです。

Qiitaでフォロー中のものは、Feedlyに次のカテゴリで登録されます。
- フォロー中のタグ -> Qiita:tags
- フォロー中のユーザー -> Qiita:followees

Qiitaでフォローを解除したものは、Feedlyから削除されます。

フィードが既に他のカテゴリで登録されている場合、
そのカテゴリでの登録は維持されます。
つまり、qiidlyで同期したことで、フィードの登録がなくなったり、カテゴリが消えちゃったりすることはありません。


Install
=======

```shell
$ pip install qiidly
```


API Access token
================

Qiita access token
- https://qiita.com/settings/applications

Feedly developer access token
- https://developer.feedly.com/v3/developer/#how-do-i-generate-a-developer-access-token



Usage
=====

```bash
$ qiidly --help
usage: qiidly [-h] -q QIITA_TOKEN -f FEEDLY_TOKEN

qiidly: Sync following tag feeds at Qiita to Feedly.

optional arguments:
  -h, --help            show this help message and exit
  -q QIITA_TOKEN, --qiita-token QIITA_TOKEN
                        Qiita access token
  -f FEEDLY_TOKEN, --feedly-token FEEDLY_TOKEN
                        Feedly developer access token
$
```

```sh
$ qiidly -q $QIITA_TOKEN -f $FEEDLY_TOKEN
## Category at Qiita: 'Qiita:tags'
+ HTML5
+ FlashAir
- Pandoc
+ Elixir	=> categories['dummy', 'Qiita:tags']
- Phoenix	=> categories['dummy']

Sync to Feedly? [y/n] y
Done!
## Category at Qiita: 'Qiita:followees'
+ uraxy

Sync to Feedly? [y/n] y
Done!
$
```


License
=======
MIT License


Libraries
=========
```shell
$ cat requirements.txt | xargs -n1 yolk -l -f License,Author,Home-page,Summary | egrep -v '^Versions with'
PyYAML (3.12)
    Summary: YAML parser and emitter for Python
    Home-page: http://pyyaml.org/wiki/PyYAML
    Author: Kirill Simonov
    License: MIT

qiita-v2 (0.1.1)
    Summary: Python Wrapper for Qiita API v2
    Home-page: http://github.com/petitviolet/qiita_py
    Author: petitviolet
    License: MIT

requests (2.11.1)
    Summary: Python HTTP for Humans.
    Home-page: http://python-requests.org
    Author: Kenneth Reitz
    License: Apache 2.0

$
```
