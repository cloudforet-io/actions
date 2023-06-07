from module import argparse as ap
from service.actions_service import ActionsService

ARGS = ap.parse_args()


def main():
    actions_srv = ActionsService()

    dest_type = ARGS.type
    org = ARGS.org
    dest = ARGS.dest

    actions_srv.deploy(org=org, dest=dest, dest_type=dest_type)


if __name__ == "__main__":
    main()
