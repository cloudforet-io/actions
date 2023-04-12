from module import argparse as ap
from service.actions_service import ActionsService

ARGS = ap.parse_args()


def main():
    actions_srv = ActionsService()

    org = ARGS.org
    dest = ARGS.dest
    if ARGS.type == 'repository':
        dest = org + '/' + dest
    type = ARGS.type
    init = ARGS.init

    actions_srv.deploy(org=org, dest=dest, type=type, init=init)


if __name__ == "__main__":
    main()
