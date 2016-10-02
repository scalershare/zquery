"""query via command-line.

Usage:
    zhihuquery.py [-qra] [--depth=<co>] <user>
    zhihuquery.py relation <user1> <user2>

Options:
    -q             提问 
    -r             回答
    -a             文章
    --depth=<co>  显示的条数
"""
from docopt import docopt


def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    print(arguments)

if __name__ == '__main__':
    cli()
