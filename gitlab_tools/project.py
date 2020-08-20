import click

from gitlab_tools.util import print_returned_json, Api


class Project(Api):
    def search(self, term):
        r = self.session.get(f"{self.config.api_url}/projects?search={term}")
        projects = [
            {
                'id': p['id'],
                'name_with_namespace': p['name_with_namespace']
            }
            for p in r.json()
        ]
        return projects

    def get(self, project_id):
        r = self.session.get(f"{self.config.api_url}/projects/{project_id}")
        return r.json()


pass_api = click.make_pass_decorator(Project, ensure=True)


@click.group()
def project():
    pass


@project.command()
@click.argument('project_id', nargs=1, type=str)
@pass_api
@print_returned_json
def get(api, project_id):
    return api.get(project_id)


@project.command()
@click.argument('term', nargs=1, type=str)
@pass_api
@print_returned_json
def search(api, term):
    return api.search(term)
