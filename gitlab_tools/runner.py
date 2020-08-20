import click

from gitlab_tools.util import print_returned_json, Api


class Runner(Api):
    def get(self, status=None, page=1):
        params = {
            "per_page": 100,
            "page": page,
        }
        if status:
            params["status"] = status
        response = self.session.get(f"{self.config.api_url}/runners/all", params=params)

        return response.json()

    def delete(self, runner_id):
        response = self.session.delete(
            f"{self.config.api_url}/runners/{runner_id}")


pass_api = click.make_pass_decorator(Runner, ensure=True)


@click.group()
def runner():
    pass


@runner.command()
@click.option('--status', type=str)
@click.option('--page', default=1, type=int)
@pass_api
@print_returned_json
def get(api, status, page):
    return api.get(status, page)


@runner.command()
@click.option('-r', '--runner-id', type=int)
@pass_api
def delete(api, runner_id):
    return api.delete(runner_id)
