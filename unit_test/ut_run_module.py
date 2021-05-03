import click


@click.command()
@click.option('--x', default=1, help='Num x')
@click.option('--y', default=1, help='Num y')
def run(x, y):
    print(click)
    print(x + y)


if __name__ == '__main__':
    # run(["--help"])
    run(["--x=1", "--y=2"])
