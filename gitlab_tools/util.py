import abc
import json
import os
import sys

import requests
from kebab import kebab_config, Field, load_source


@kebab_config
class GitlabConfig:
    api_url = Field("api_url")
    api_token = Field("api_token")


def load_config() -> GitlabConfig:
    default_config_path = os.path.expanduser("~/.config/gitlab/tools.yaml")
    if not os.path.exists(default_config_path):
        dir = os.path.dirname(default_config_path)
        os.makedirs(dir, exist_ok=True)
        print(f"Please config {default_config_path}", file=sys.stderr)
        sys.exit(1)

    k = load_source(default_urls=default_config_path)
    return k.cast(".", GitlabConfig)


def print_returned_json(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        print(json.dumps(result))
        return result
    wrapper.__name__ = fn.__name__
    return wrapper


class Api(abc.ABC):
    def __init__(self):
        self.config = load_config()
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.config.api_token}",
            "Content-Type": "application/json"
        })
