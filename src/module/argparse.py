import argparse
import textwrap


def parse_args():
    parser = argparse.ArgumentParser(
        description='File push to github repository',
        epilog=textwrap.dedent('''\
            Examples:
                python src/%(prog)s --org cloudforet-io --dest inventory --type repository
                python src/%(prog)s --dest inventory --type repository
                python src/%(prog)s --dest config --type repository --init
                python src/%(prog)s --dest core/python-service --type topic
                python src/%(prog)s --dest core/console --type topic --init
        '''),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--org', metavar='"organization"', default='cloudforet-io',
                        required=True, help='organization of github repository (Default=cloudforet-io)')

    parser.add_argument('--dest', metavar='"destination"',
                        required=True, help='destination of workflows')

    parser.add_argument('--type', metavar='"repository|topic"', choices=['repository, topic'],
                        required=True, help='type of destination')

    parser.add_argument('--init', action='store_true', default=False,
                        help='init deployment flag (Default=false)')

    return parser.parse_args()
