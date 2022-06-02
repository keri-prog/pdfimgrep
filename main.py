import click

@click.command()
@click.argument('filename')
@click.option('--text', '-t', help="create a text file from the given pdf", prompt="Enter filename or filepath")
def cli(filenme, text):
    '''
    This will create a text file in the same folder as the folder of execution.
    '''
    print("hello world")