Session
=============

## Creating a session and generating a token for API requests.

Login using token, or username. Optionally include password, or enter it at the prompt.
```python
>>> from hexpy import HexpySession
>>> session = HexpySession.login(username="username@gmail.com", password="secretpassword")
>>> session.save_token()  # saving token to ~/.hexpy/credentials.json
```
or
```python
>>> session = HexpySession.login(username="username@email.com")
Enter password: *********
>>> session.save_token()
```
or instantiate a session using a token
```python
>>> session = HexpySession(token="previously_saved_token")
```
Create instance by loading token from file.  Default is `~/.hexpy/credentials.json`
```python
>>> session = HexpySession.load_auth_from_file()
```
Create instance with context manager to close TCP session automatically when finished
```python
>>> with HexpySession.load_auth_from_file() as session:
...:     client = MonitorAPI(session)
...:     # use client to call API multiple times with same session

>>> # session TCP connection is closed until next call to API
```

## Methods

### login
```python
login(username: str, password: str = None, no_expiration: bool = False) -> HexpySession
```
Instantiate class from username and password.
#### Arguments
* username: account username.
* password: account password.
* no_expiration: True/False token with 24 expiration.

### save_token
```python
save_token(path: str = None) -> None
```
Save authorization token.
#### Arguments
* path: String, path to store credentials. default is `~/.hexpy/credentials.json`

### load_auth_from_file
```python
load_auth_from_file(path: str = None) -> HexpySession
```
Instantiate class from previously saved credentials file.
#### Arguments
* path: String, path to store credentials. default is `~/.hexpy/credentials.json`

### close

```python
close() -> None
```
Close open connection to API server.

