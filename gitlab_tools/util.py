import re
import sys

import click

from .constant import gitlab_config, session, print_returned_json
from gitlab_tools import merge_request


@click.command()
def remove_offline_runners():
    while True:
        r = session.get(f"{gitlab_config.api_url}/runners/all?status=offline")

        if len(r.json()) == 0:
            break
        for runner in r.json():
            print(f"deleting {runner['id']}: {runner['description']}")
            r = session.delete(f"{gitlab_config.api_url}/runners/{runner['id']}")


@click.command()
@click.option('-p', '--project-id', default=47, type=int)
@click.option('--page', default=1, type=int)
@print_returned_json
def find_incompliant_title(project_id, page=1):
    results = []
    totals = 0

    while True:
        resp_json = merge_request.get(project_id=project_id, page=page)
        if not resp_json:
            break
        for mr in resp_json:
            if not re.match(r"Revert .*", mr['title']) and not re.match(r"\[\w+-\d+\].*", mr['title']):
                results += [{
                    k: mr[k]
                    for k in ["id", "iid", "title"]
                }]
        print(f"querying: page {page}", file=sys.stderr)
        page += 1
        totals += len(resp_json)

    print(f"rate: {len(results)}/{totals}", file=sys.stderr)
    return results
