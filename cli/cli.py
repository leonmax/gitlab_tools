import click

from cli.release import release
from cli.project import project
from cli.merge_request import merge_request


@click.group()
def entry_point():
    pass


def main():
    entry_point.add_command(release)
    entry_point.add_command(project)
    entry_point.add_command(merge_request)
    entry_point()


if __name__ == '__main__':
    main()
