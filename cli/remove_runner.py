import click

from .constant import gitlab_config, session


@click.command()
def remove_offline_runners():
    while True:
        r = session.get(f"{gitlab_config.api_url}/runners/all?status=offline")

        if len(r.json()) == 0:
            break
        for runner in r.json():
            print(f"deleting {runner['id']}: {runner['description']}")
            r = session.delete(f"{gitlab_config.api_url}/runners/{runner['id']}")


if __name__ == "__main__":
    remove_offline_runners()
