import json
import os
import sys

import requests
from kebab import load_source, kebab_config, Field


@kebab_config
class GitlabConfig:
    api_url = Field("url")
    token = Field("token")


default_config_path = os.path.expanduser("~/.config/gitlab/tools.yaml")
if not os.path.exists(default_config_path):
    dir = os.path.dirname(default_config_path)
    os.makedirs(dir, exist_ok=True)
    print(f"Please config {default_config_path}")
    sys.exit(1)

k = load_source(default_urls=default_config_path)
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
