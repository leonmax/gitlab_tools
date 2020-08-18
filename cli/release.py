import click

from .constant import gitlab_config, session


@click.group()
def release():
    pass


@release.command()
@click.option('-p', '--project-id', default=47, type=int)
@click.option('-d', '--description', type=int)
@click.argument('tag', nargs=1, type=str)
def create(project_id, tag, description):
    data = {
        "tag_name": tag,
        "description": description,
    }
    r = session.post(f"{gitlab_config.api_url}/projects/{project_id}/releases", data=data)


@release.command()
@click.option('-p', '--project-id', default=47, type=int)
@click.argument('tag', nargs=1, type=str)
def delete(project_id, tag):
    r = session.delete(f"{gitlab_config.api_url}/projects/{project_id}/releases/{tag}")
