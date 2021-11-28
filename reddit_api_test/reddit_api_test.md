
# API Rules

[Rules](https://github.com/reddit-archive/reddit/wiki/API):

* Use OAuth2 (PRAW).
* Up to 60 requests per minute (PRAW).
* Monitor `X-Ratelimit-Used`, `X-Ratelimit-Remaining`, `X-Ratelimit-Reset` (PRAW).
* Use unique User-Agent, format: `<platform>:<app ID>:<version string> (by /u/<reddit username>)`.
* Requests for multiple resources at a time are always better than requests for single-resources.

# Generate API credentials

Go to [app preferences](https://www.reddit.com/prefs/apps):

* **name**: `Evaluation of Competencies`
* **web app**
* **description**: `Evaluation of Competencies in Reddit`
* **about url**: _empty_
* **redirect uri**: `http://www.example.com/unused/redirect/uri`

[Register](https://docs.google.com/forms/d/e/1FAIpQLSezNdDNK1-P8mspSbmtC2r86Ee9ZRbC66u929cG2GX0T9UMyw/viewform) app.

Credentials:

* **secret**: _client_secret_
* **App ID**: _client_id_
* **User-Agent**: `python:com.example.evaluationofcompetencies:v0.1 (by /u/gonzalocl1024)`

# PRAW configuration

Copy default configuration file: 
```bash
cp /usr/lib/python3.9/site-packages/praw/praw.ini .
```

Add API credentials:
```bash
echo '

[api_test]
client_id=
client_secret=
' >> praw.ini
```

[reddit api documentation](https://www.reddit.com/wiki/api)  
[b](https://www.reddit.com/prefs/apps)  
[c](https://docs.google.com/forms/d/e/1FAIpQLSezNdDNK1-P8mspSbmtC2r86Ee9ZRbC66u929cG2GX0T9UMyw/viewform)  
[a](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example)  
[PRAW documentation](https://praw.readthedocs.io/en/stable/)  
[d](https://www.reddit.com/dev/api)  
[e](https://github.com/reddit-archive/reddit/wiki/JSON)  