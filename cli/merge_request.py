import json
import re
import sys
from datetime import date, timedelta

import click

from cli.constant import gitlab_config, session, print_returned_json


@click.group()
def merge_request():
    pass


@merge_request.command()
@click.option('-p', '--project-id', default=47, type=int)
@click.option('--page', default=1, type=int)
@click.option('--state', default="merged", type=str)
@click.option('--created-after', type=str)
@print_returned_json
def get(project_id, page, state, created_after):
    params = {
        "per_page": 100,
        "page": page,
        "state": state,
        "created_after": created_after or (date.today() - timedelta(days=30)).isoformat()
    }
    response = session.get(f"{gitlab_config.api_url}/projects/{project_id}/merge_requests", params=params)

    return response.json()


def find_incompliant_title(project_id, page=1):
    results = []
    totals = 0

    while True:
        resp_json = get(project_id=project_id, page=page)
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
    print(json.dumps(results))


@merge_request.command()
@click.option('-p', '--project-id', default=44, type=int)
@click.option('--merge-request-iid', default=225, type=int)
@print_returned_json
def get_approval(project_id, merge_request_iid):
    response = session.get(f"{gitlab_config.api_url}/projects/{project_id}/merge_requests/{merge_request_iid}/approvals")

    return response.json()


if __name__ == "__main__":
    print(get_approval(project_id=44, merge_request_iid=sys.argv[1])['approvals_left'])
