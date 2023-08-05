# ludicrousdns
Ludicrously speedy, infectious with the async. `ludicrousdns` is designed to be a cleaner, more accurate and more rate-limited version of [massdns](https://github.com/blechschmidt/massdns). 

## Installation
```
pip install ludicrousdns
```

## Usage
`ludicrousdns` can be used both as a library and a binary:
```python
from ludicrousdns import Resolver
r = Resolver()
r.resolve_hosts(["example.com", "google.com"])
```
or
```shell
echo "example.com\ngoogle.com" > hosts.txt
ludicrousdns hosts.txt
```

## Features
- Rate-limited
- Detects wildcard DNS
- Ludicrously speedy

## TODO
- Add benchmark to measure CPU- and network usage
- Add benchmark to measure overall speed (use randomized subdomains to avoid effects of caching)
- Add timeout to connections, for example with [async_timeout](https://github.com/aio-libs/async-timeout)
- Add option to adjust rate-limiting
