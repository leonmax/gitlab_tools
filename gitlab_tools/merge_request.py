import sys
from datetime import date, timedelta

import click

from .constant import gitlab_config, session, print_returned_json


def get(project_id, page=1, state="merged", created_after=None):
    params = {
        "per_page": 100,
        "page": page,
        "state": state,
        "created_after": created_after or (date.today() - timedelta(days=30)).isoformat()
    }
    response = session.get(f"{gitlab_config.api_url}/projects/{project_id}/merge_requests", params=params)

    return response.json()


def get_approval(project_id, merge_request_iid):
    response = session.get(
        f"{gitlab_config.api_url}/projects/{project_id}/merge_requests/{merge_request_iid}/approvals")

    return response.json()


@click.group()
def merge_request():
    pass


@merge_request.command("get")
@click.option('-p', '--project-id', default=47, type=int)
@click.option('--page', default=1, type=int)
@click.option('--state', default="merged", type=str)
@click.option('--created-after', type=str)
@print_returned_json
def get_command(project_id, page, state, created_after):
    return get(project_id, page, state, created_after)


@merge_request.command("get_approval")
@click.option('-p', '--project-id', default=44, type=int)
@click.option('--merge-request-iid', default=225, type=int)
@print_returned_json
def get_approval_command(project_id, merge_request_iid):
    return get_approval(project_id, merge_request_iid)


if __name__ == "__main__":
    print(get_approval(project_id=44, merge_request_iid=sys.argv[1])['approvals_left'])
