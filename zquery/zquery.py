"""query via command-line.

Usage:
    zquery [(-q|-r|-a)] [--depth=<co>] <user>
    zquery question <url>
    zquery answer <url>
    zquery column <url>
    zquery post <url>
    zquery collection <url>

Options:
    -q             提问 
    -r             回答
    -a             文章
    --depth=<co>   显示的条数

Example:
    zquery -a --depth=15 excited-vczh
    zquery excited-vczh
    zquery post https://zhuanlan.zhihu.com/p/19780644
"""
from docopt import docopt
from .queryPprint import *


def cli():
    """command-line interface"""

    args = docopt(__doc__)
    if args["-q"] == True:
        pprint_user_ask(args["<user>"], int(args["--depth"]))
    elif args["-r"] == True:
        pprint_user_answer(args["<user>"], int(args["--depth"]))
    elif args["-a"] == True:
        pprint_user_article(args["<user>"], int(args["--depth"]))
    elif args["post"] == True:
        pprint_post(args['<url>'])
    elif args["question"] == True:
        pprint_question(args['<url>'])
    elif args["column"] == True:
        pprint_column(args['<url>'])
    elif args["answer"] == True:
        pprint_answer(args['<url>'])
    elif args["collection"] == True:
        pprint_collection(args['<url>'])
    else:
        pprint_user_base(args['<user>'])


if __name__ == '__main__':
    cli()
