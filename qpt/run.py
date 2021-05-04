import click
from qpt.module import RunModule


@click.command()
@click.argument("file_path")
@click.option("--debug", type=bool, default=False, help="是否为Debug模式")
def run_qpt(file_path, debug):
    print(file_path)
    pass


if __name__ == '__main__':
    run_qpt(["1"])
