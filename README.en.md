qiidly
======

Sync Qiita feeds for followees and following tags to Feedly.


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

```bash
$ python -m unittest discover tests
```


License
=======
MIT License
