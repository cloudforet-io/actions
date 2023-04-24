import argparse
import textwrap


def parse_args():
    parser = argparse.ArgumentParser(
        description='File push to github repository',
        epilog=textwrap.dedent('''\
            Examples:
                python src/%(prog)s --org exam-org --dest inventory --type repository
                python src/%(prog)s --dest inventory --type repository
                python src/%(prog)s --dest config --type repository
                python src/%(prog)s --dest core/console --type topic
        '''),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--org', metavar='"organization"', default='cloudforet-io',
                        help='organization of github repository (Default=cloudforet-io)')

    parser.add_argument('--dest', metavar='"destination"',
                        required=True, help='destination of workflows')

    parser.add_argument('--type', metavar='"repository|topic"', choices=['repository', 'topic'], type=str.lower,
                        required=True, help='type of destination')

    return parser.parse_args()
