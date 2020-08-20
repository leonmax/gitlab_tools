import sys
from datetime import date, timedelta

import click

from gitlab_tools.util import print_returned_json, Api


class MergeRequest(Api):
    def get(self, project_id, page=1, state="merged", created_after=None):
        params = {
            "per_page": 100,
            "page": page,
            "state": state,
            "created_after": created_after or (date.today() - timedelta(days=30)).isoformat()
        }
        response = self.session.get(f"{self.config.api_url}/projects/{project_id}/merge_requests", params=params)

        return response.json()

    def get_approval(self, project_id, merge_request_iid):
        response = self.session.get(
            f"{self.config.api_url}/projects/{project_id}/merge_requests/{merge_request_iid}/approvals")

        return response.json()


pass_api = click.make_pass_decorator(MergeRequest, ensure=True)


@click.group()
def merge_request():
    pass


@merge_request.command()
@click.option('-p', '--project-id', type=int)
@click.option('--page', default=1, type=int)
@click.option('--state', default="merged", type=str)
@click.option('--created-after', type=str)
@pass_api
@print_returned_json
def get(api, project_id, page, state, created_after):
    return api.get(project_id, page, state, created_after)


@merge_request.command()
@click.option('-p', '--project-id', type=int)
@click.option('--merge-request-iid', type=int)
@pass_api
@print_returned_json
def get_approval(api, project_id, merge_request_iid):
    return api.get_approval(project_id, merge_request_iid)


if __name__ == "__main__":
    print(get_approval(project_id=44, merge_request_iid=sys.argv[1])['approvals_left'])
