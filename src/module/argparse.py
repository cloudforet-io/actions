import argparse
import textwrap

def parse_args():
    parser = argparse.ArgumentParser(
        description='File push to github repository',
        epilog=textwrap.dedent('''\
            Examples:
                python src/%(prog)s --repo spaceone/inventory
                python src/%(prog)s --repo spaceone/config --init
        '''),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--repo', required=True, metavar='<owner/repo>',
                        help='Select specified repository.')

    parser.add_argument('--init', action='store_true', default=False,
                        help='Deploy sync workflow only.')

    return parser.parse_args()