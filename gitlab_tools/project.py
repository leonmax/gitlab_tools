import click

from .constant import gitlab_config, session, print_returned_json


def search(term):
    r = session.get(f"{gitlab_config.api_url}/projects?search={term}")
    projects = [
        {
            'id': p['id'],
            'name_with_namespace': p['name_with_namespace']
        }
        for p in r.json()
    ]
    return projects


def get(project_id):
    r = session.get(f"{gitlab_config.api_url}/projects/{project_id}")
    return r.json()


@click.group()
def project():
    pass


@project.command()
@click.argument('term', nargs=1, type=str)
@print_returned_json
def search_command(term):
    return search(term)


@project.command()
@click.argument('project_id', nargs=1, type=str)
@print_returned_json
def get_command(project_id):
    return get(project_id)