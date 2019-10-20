#!/bin/python
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
import subprocess

logger = logging.getLogger(__name__)


def create_argparser():
    parser = argparse.ArgumentParser(description="runs the bot.")
    subparsers = parser.add_subparsers(help="sub-command help")
    create_user = subparsers.add_parser("create", help="creates a new Rasa X user")
    create_user.add_argument(
        "role",
        choices=["admin", "annotator", "tester"],
        help="Role of the user that gets created.",
    )

    create_user.add_argument("username", help="Name of the user to create")
    create_user.add_argument("password", help="Password to use for the user")
    create_user.add_argument(
        "--update", action="store_true", help="Update the password of an existing user"
    )
    create_user.set_defaults(func=create_rasa_x_user)

    delete_user = subparsers.add_parser("delete", help="delete a Rasa X user")
    delete_user.add_argument("username", help="Name of the user to delete")
    delete_user.set_defaults(func=delete_rasa_x_user)
    return parser


def create_rasa_x_user(args):
    create_cmd = "/app/scripts/manage_users.py create '{}' '{}' {}".format(
        args.username, args.password, args.role
    )

    if args.update:
        create_cmd += " --update"
    retcode = subprocess.call(
        "docker-compose exec rasa-x bash " '-c "python {}"'.format(create_cmd),
        shell=True,
    )

    if retcode == 0:
        logger.info("Created user.")
    else:
        logger.error("Failed to create user.")
        exit(retcode)


def delete_rasa_x_user(args):
    delete_cmd = "/app/scripts/manage_users.py delete {}".format(args.username)

    retcode = subprocess.call(
        "docker-compose exec rasa-x bash " '-c "python {}"'.format(delete_cmd),
        shell=True,
    )

    if retcode == 0:
        logger.info("Deleted user.")
    else:
        logger.error("Failed to delete user.")
        exit(retcode)


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")

    parsed = create_argparser().parse_args()
    # call the function associated with the sub parser (set_defaults)
    parsed.func(parsed)
