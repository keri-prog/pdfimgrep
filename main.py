import click
from utils.clifunc import pdf_to_text, display_location, grep_all


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('regex')
@click.option('--grep', '-g', is_flag=True, help="greps all the lines with occurances of the given regex in the given pdf")
@click.option('--find', '-f', is_flag=True, help="find and display all the occurances of the given regex in the given pdf")
@click.option('--text', '-t', is_flag=True, help="create a text file from the given pdf")
def cli(regex, filename, grep, find, text):
    """Helps you traverse through image-text pdf files with the help of grep, find and convert to text functions."""
    if grep:
        print(grep_all(filename, regex))
    if find:
        display_location(filename, regex)
    if text:
        pdf_to_text(filename, regex)
