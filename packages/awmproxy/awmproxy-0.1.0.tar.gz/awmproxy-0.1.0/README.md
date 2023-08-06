# **awmproxy API Python Wrapper**

This package simplifies using awmproxy.net api to grab proxies so you can go scraping or whatever it is you need.

Requirements: paid account with api key


Usage:


```
import awmproxy
awm = awmproxy.AwmProxy('abcdef0123456abcdef123456apikeyapikey')

```
Get results as list in ip:port:
```
awm.get_proxy()
```

Get only universal ports that change ips every request:

```
awm.get_proxy(universal_port=701)
```

Get only US proxies, as list of json dict, with all available proxy information:

```
awm.get_proxy(json=True, info=True, country_only='US')

```

Get 25 fast proxies, not Russian, with full info as a list of tuples:

```
awm.get_proxy(country_not='RU', info=True, limit=25, fast=True)
```