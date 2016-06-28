# Media Monitor

_Part of a joint research project between the [School of Computer Science](https://www.cs.cf.ac.uk/) and the [School of Journalism](http://www.cardiff.ac.uk/journalism-media-cultural-studies) at Cardiff University._

### Getting Started

To get started you'll need the following packages
- `twython`
- `pymongo`

To install them run

```python
$ pip3 install twython
$ pip3 install pymongo
```

Next, you'll need to add a `credentials.py` file containing you twitter access tokens.

`credentials.py`

```python
app_key = 'your_app_key'
app_secret = 'your_app_secret'
auth_token = 'your_auth_token'
auth_secret = 'your_auth_secret'

```

To start monitoring run

```python
$ python3 start.py
```
