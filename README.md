# revsport-api

## Usage as a command-line tool

```
pip install git+https://github.com/bygri/revsport-api.git
revsport -u [USERNAME] [PORTALNAME] [ACTION]
```

The only currently-supported `ACTION` is `members`.


## Usage as a library

```python
api = RevSportAPI("my-portal-name")
api.login_old("username", "password")
data = api.fetch_members()
print(data)
```


## Development

Test the CLI with `inv cli -u [USERNAME] [PORTALNAME] [ACTION]`
