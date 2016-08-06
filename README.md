qiidly
==================================================

Sync following tag feeds at Qiita to Feedly.


Setup
==================================================

```bash
$ pip install -r requirements.txt
```

- [Python Wrapper for Qiita API v2](https://github.com/petitviolet/qiita_py)


Usage
==================================================

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

```bash
$ python -m qiidly.command_line -q $QIITA_TOKEN -f $FEEDLY_TOKEN
Already up-to-date.
$
```

or

```bash
$ ./qiidly.sh
Already up-to-date.
$
```

or

```bash
$ ./qiidly.sh
## Category at Qiita: 'Qiita:tags'
+ linebot
- gwt
+ onsenui	=> categories['dummy', 'Qiita:tags']
- Cytoscape	=> categories['dummy']

Sync following tag feeds at Qiita to Feedly? [y/n] y
Done!
$
```

Qiita access token
- https://qiita.com/settings/applications

Feedly developer access token
- https://developer.feedly.com/v3/developer/#how-do-i-generate-a-developer-access-token


tests
==================================================

```bash
$ python -m unittest discover tests
```


License
==================================================
MIT
