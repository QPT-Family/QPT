import click
from qpt.executor import RunExecutableModule


@click.command()
@click.argument("file_path")
@click.option("--debug", type=bool, default=False, help="是否为Debug模式")
def run_module(qpt_file_path, debug):
    # ToDO 增加Debug模式
    module = RunExecutableModule(qpt_file_path)
    module.run()


if __name__ == '__main__':
    run_module(["1"])
