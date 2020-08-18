import json

import requests
from kebab import default_source, kebab_config, Field


@kebab_config
class GitlabConfig:
    api_url = Field("url")
    token = Field("token")


k = default_source()
gitlab_config = k.cast("gitlab", GitlabConfig)

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {gitlab_config.token}",
    "Content-Type": "application/json"
})


def print_returned_json(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        print(json.dumps(result))
        return result
    wrapper.__name__ = fn.__name__
    return wrapper
