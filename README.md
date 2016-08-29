qiidly
======

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


Setup
=====

Libraries
---------
```sh
$ pip install -r requirements.txt
```

- [Python Wrapper for Qiita API v2](https://github.com/petitviolet/qiita_py) ([MIT License](https://petitviolet.mit-license.org/))


API Access token
----------------

Qiita access token
- https://qiita.com/settings/applications

Feedly developer access token
- https://developer.feedly.com/v3/developer/#how-do-i-generate-a-developer-access-token



Usage
=====

```bash
$ python -m qiidly.command_line -h
usage: command_line.py [-h] -q QIITA_TOKEN -f FEEDLY_TOKEN

qiidly: Qiita to Feedly.

optional arguments:
  -h, --help            show this help message and exit
  -q QIITA_TOKEN, --qiita-token QIITA_TOKEN
                        Qiita access token
  -f FEEDLY_TOKEN, --feedly-token FEEDLY_TOKEN
                        Feedly developer access token
$
```

```sh
$ ./qiidly.sh  # == python -m qiidly.command_line -q $QIITA_TOKEN -f $FEEDLY_TOKEN
## Category at Qiita: 'Qiita:tags'
+ linebot
- gwt
+ onsenui	=> categories['dummy', 'Qiita:tags']
- Cytoscape	=> categories['dummy']

Sync following tag feeds at Qiita to Feedly? [y/n] y
Done!
## Category at Qiita: 'Qiita:followees'
- uraxy

Sync to Feedly? [y/n] y
Done!
$
```


Tests
=====

with unittest
-------------

```bash
$ python -m unittest discover tests
```

with [nose2](http://nose2.readthedocs.io/en/latest/index.html)
--------------------------------------------------------------

- [Docs » Plugins for nose2 » Test coverage reporting](http://nose2.readthedocs.io/en/latest/plugins/coverage.html)

```bash
$ pip install nose2
$ pip install cov-core
$ nose2 --with-coverage
..........
----------------------------------------------------------------------
Ran 10 tests in 0.004s

OK
----------- coverage: platform linux, python 3.5.1-final-0 -----------
Name                     Stmts   Miss  Cover
--------------------------------------------
qiidly/__init__.py           0      0   100%
qiidly/command_line.py      43     43     0%
qiidly/feedly.py            35     14    60%
qiidly/main.py             108     84    22%
qiidly/qiita.py             45     25    44%
setup.py                     2      2     0%
tests/test_feedly.py        32      0   100%
tests/test_main.py          21      0   100%
tests/test_qiita.py         31      0   100%
--------------------------------------------
TOTAL                      317    168    47%
$ nose2 --with-coverage --coverage-report html
..........
----------------------------------------------------------------------
Ran 10 tests in 0.004s

OK
----------- coverage: platform linux, python 3.5.1-final-0 -----------
Coverage HTML written to dir htmlcov
y$ nose2 --with-coverage --coverage-report annotate
..........
----------------------------------------------------------------------
Ran 10 tests in 0.004s

OK
----------- coverage: platform linux, python 3.5.1-final-0 -----------
Coverage annotated source written next to source
$
```



License
=======
MIT License
