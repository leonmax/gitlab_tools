import click

from .constant import gitlab_config, session, print_returned_json


def get(project_id):
    r = session.get(f"{gitlab_config.api_url}/projects/{project_id}/releases")
    return r.json()


def create(project_id, tag, description=None):
    data = {
        "tag_name": tag,
        "description": description,
    }
    r = session.post(f"{gitlab_config.api_url}/projects/{project_id}/releases", data=data)


def delete(project_id, tag):
    r = session.delete(f"{gitlab_config.api_url}/projects/{project_id}/releases/{tag}")


@click.group()
def release():
    pass


@release.command("get")
@click.option('-p', '--project-id', default=47, type=int)
@print_returned_json
def get_command(project_id):
    return get(project_id)


@release.command("create")
@click.option('-p', '--project-id', default=47, type=int)
@click.option('-d', '--description', type=str)
@click.argument('tag', nargs=1, type=str)
def create_command(project_id, tag, description):
    return create(project_id, tag, description)


@release.command("delete")
@click.option('-p', '--project-id', default=47, type=int)
@click.argument('tag', nargs=1, type=str)
def delete_command(project_id, tag):
    return delete(project_id, tag)
