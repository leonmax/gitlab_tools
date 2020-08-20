import os
import re
import sys

import click

from gitlab_tools.merge_request import MergeRequest
from gitlab_tools.runner import Runner
from gitlab_tools.util import print_returned_json


@click.command()
@click.option('-s', '--shell', type=str)
def completion(shell):
    if not shell:
        shell = os.path.basename(os.environ['SHELL'])
    if shell == "bash" or shell == "zsh":
        click.echo('''
        You can do
        For Bash, add this to ~/.bashrc:
            ```
            eval "$(_FOO_BAR_COMPLETE=source_bash foo-bar)"
            ```
        For Zsh, add this to ~/.zshrc:
            ```
            eval "$(_FOO_BAR_COMPLETE=source_zsh foo-bar)"
            ```
        
        The above will be a bit slow, a preferably solution is:
            ```
            _LAB_COMPLETE=source_bash lab > lab-complete.sh
            ```
        In .bashrc or .zshrc, source the script instead of the eval command:
            ```
            . /path/to/lab-complete.sh
            ```
        ''')
    if shell == "fish":
        click.echo('''
        Add the below to `~/.config/fish/completions/lab.fish` 
            ```
            eval (env _LAB_COMPLETE=source_fish)
            ```
        ''')


@click.command()
def remove_offline_runners():
    api = Runner()
    while True:
        json = api.get(status="offline")

        if len(json) == 0:
            break
        for runner in json:
            print(f"deleting {runner['id']}: {runner['description']}")
            r = api.delete(runner['id'])


@click.command()
@click.option('-p', '--project-id', default=47, type=int)
@click.option('--page', default=1, type=int)
@print_returned_json
def find_incompliant_title(project_id, page=1):
    merge_request = MergeRequest()
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
