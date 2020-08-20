import click

from gitlab_tools.util import print_returned_json, Api


class Release(Api):
    def get(self, project_id):
        r = self.session.get(f"{self.config.api_url}/projects/{project_id}/releases")
        return r.json()

    def create(self, project_id, tag, description=None):
        data = {
            "tag_name": tag,
            "description": description,
        }
        r = self.session.post(f"{self.config.api_url}/projects/{project_id}/releases", data=data)

    def delete(self, project_id, tag):
        r = self.session.delete(f"{self.config.api_url}/projects/{project_id}/releases/{tag}")


pass_api = click.make_pass_decorator(Release, ensure=True)


@click.group()
def release():
    pass


@release.command()
@click.option('-p', '--project-id', default=47, type=int)
@pass_api
@print_returned_json
def get(project_id):
    return get(project_id)


@release.command()
@click.option('-p', '--project-id', default=47, type=int)
@click.option('-d', '--description', type=str)
@click.argument('tag', nargs=1, type=str)
@pass_api
def create(project_id, tag, description):
    return create(project_id, tag, description)


@release.command()
@click.option('-p', '--project-id', default=47, type=int)
@click.argument('tag', nargs=1, type=str)
@pass_api
def delete(project_id, tag):
    return delete(project_id, tag)
