import typer
from rat import __version__

app = typer.Typer(help='RAT — Make the terminal yours.', no_args_is_help=True, rich_markup_mode=None)


def version(value: bool):
    if value:
        typer.echo(f'rat {__version__}')
        raise typer.Exit()


@app.callback()
def options(ctx: typer.Context, version_flag: bool = typer.Option(False, '--version', callback=version, is_eager=True), no_color: bool = typer.Option(False, '--no-color')):
    ctx.obj = {'no_color': no_color}


def main():
    app()


from rat.cli import config, doctor, ls, tree, git, init, theme, cat  # noqa: E402,F401
