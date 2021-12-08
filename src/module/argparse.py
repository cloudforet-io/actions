import argparse
import textwrap

def parse_args():
    parser = argparse.ArgumentParser(
        description='Management github action workflows',
        epilog=textwrap.dedent('''\
            Examples:
                python src/%(prog)s --group all
                python src/%(prog)s --group plugin
                python src/%(prog)s --gruop backend --repo spaceone/inventory
        '''),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--group', required=True, choices=['backend','console','console-api','plugin'],
                        help='Select workflow group')
    parser.add_argument('--repo', metavar='<specific repository name>',
                        help='Select specified repository.')

    return parser.parse_args()