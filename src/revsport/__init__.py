import argparse
from getpass import getpass
from revsport.api import RevSportAPI


def execute_cli() -> None:
    parser = argparse.ArgumentParser(description="Fetch data from revolutioniseSPORT.")
    parser.add_argument("portal", metavar="PORTAL-NAME")
    parser.add_argument("action", metavar="ACTION")
    parser.add_argument("-u", "--username", required=True)
    parser.add_argument("--tfa")
    args = parser.parse_args()

    password = getpass()

    api = RevSportAPI(args.portal)
    if args.tfa:
        api.login(args.username, password, args.tfa)
    else:
        api.login_old(args.username, password)

    match args.action:
        case "members":
            print(api.fetch_members())
        case _:
            print("Invalid or unknown action specified.")
