from module import argparse as ap
from service.actions_service import ActionsService

ARGS = ap.parse_args()


def main():
    actions_srv = ActionsService()

    type = ARGS.type
    org = ARGS.org
    dest = ARGS.dest
    if ARGS.type == 'repository':
        dest = org + '/' + dest

    actions_srv.deploy(org=org, dest=dest, type=type)


if __name__ == "__main__":
    main()
