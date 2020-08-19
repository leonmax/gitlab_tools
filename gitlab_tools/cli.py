import click

from gitlab_tools.release import release
from gitlab_tools.project import project
from gitlab_tools.merge_request import merge_request
from gitlab_tools.util import remove_offline_runners, find_incompliant_title

@click.group()
def entry_point():
    pass


def main():
    entry_point.add_command(release)
    entry_point.add_command(project)
    entry_point.add_command(merge_request)
    entry_point.add_command(remove_offline_runners)
    entry_point.add_command(find_incompliant_title)
    entry_point()


if __name__ == '__main__':
    main()
