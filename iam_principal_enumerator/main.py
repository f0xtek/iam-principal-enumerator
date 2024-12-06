"""
IAM Principal Enumeration Script

This script is used to enumerate valid IAM principals in an AWS account.
It creates a temporary IAM role, tests a list of potential principal ARNs, 
and cleans up the role afterward. The results of valid principals are printed.

Dependencies:
- boto3
"""

from argparse import ArgumentParser
import sys

from loguru import logger
import boto3

from .aws.iam import (
    build_arn,
    create_iam_role,
    create_role_trust_policy,
    delete_iam_role,
    is_valid_arn,
    is_valid_aws_account_id,
)
from .aws.sts import get_current_account_id
from .util import generate_random_string


def parse_args():
    """
    Parse command-line arguments.

    :return: Parsed arguments
    """
    parser = ArgumentParser(
        description="Enumerate valid IAM principals in an AWS account."
    )
    parser.add_argument(
        "-r",
        "--enum-role-name",
        type=str,
        default="IAMEnum",
        help="The name of the IAM role used for enumeration. "
        "The role name will be suffixed with an 8-character random string.",
    )
    return parser.parse_args()


def main():
    logger.info("IAM Principal Enumerator")
    args = parse_args()

    iam_client = boto3.client("iam")
    sts_client = boto3.client("sts")

    my_account_id = get_current_account_id(client=sts_client)
    if not is_valid_aws_account_id(account_id=my_account_id):
        print(f"Invalid source account ID: {my_account_id}")
        sys.exit(1)

    my_account_principal_arn = build_arn(account_id=my_account_id, principal="root")

    if is_valid_arn(arn=my_account_principal_arn):
        initial_trust_policy = create_role_trust_policy(
            principal_arn=my_account_principal_arn
        )
        role_name = f"{args.enum_role_name}-{generate_random_string()}"
        role_arn = create_iam_role(
            client=iam_client, role_name=role_name, trust_policy=initial_trust_policy
        )
        delete_iam_role(client=iam_client, role_name=role_name)
    else:
        print(f"Invalid arn: {my_account_principal_arn}")


if __name__ == "__main__":
    main()
