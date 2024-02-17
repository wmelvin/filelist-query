from importlib import metadata

import click

from filelist_query.ui import UI

DIST_NAME = "fileist_query"
MOD_VERSION = "cli-240217.1"


def get_app_version() -> str:
    try:
        return metadata.version(DIST_NAME)
    except metadata.PackageNotFoundError:
        return MOD_VERSION


@click.command()
@click.version_option(get_app_version())
@click.argument("db_file", required=False, type=click.Path(exists=True))
def run(db_file: str = None) -> None:
    ui = UI(db_file)
    ui.run()


if __name__ == "__main__":
    print(get_app_version())
