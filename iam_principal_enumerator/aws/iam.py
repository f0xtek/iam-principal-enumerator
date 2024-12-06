import json
import re

from loguru import logger


def is_valid_aws_account_id(account_id: str) -> bool:
    """
    Validate that the AWS account ID is a 12-digit number.

    :param account_id: AWS account ID to validate
    :return: True if valid, False otherwise
    """
    return re.fullmatch(r"\d{12}", str(account_id)) is not None


def is_valid_arn(arn: str) -> str:
    return (
        re.fullmatch(
            r"^(?:\d{12}|(arn:(aws|aws-us-gov|aws-cn):iam::\d{12}(?:|:(?:root|user\/[0-9A-Za-z\+\.@_,-]{1,64}))))$",
            arn,
        )
        is not None
    )


def build_arn(account_id: str, principal: str) -> str:
    return f"arn:aws:iam::{account_id}:{principal}"


def create_role_trust_policy(principal_arn: str) -> str:
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                "Principal": {"AWS": principal_arn},
            }
        ],
    }
    return json.dumps(trust_policy)


def create_iam_role(client, role_name: str, trust_policy: str) -> str:
    """
    Create an IAM role with a trust policy for the current AWS account.

    :param role_name: Name of the IAM role to create
    :return: None
    """

    try:
        resp = client.create_role(
            RoleName=role_name, AssumeRolePolicyDocument=trust_policy
        )
        arn = resp["Role"]["Arn"]
        logger.info(f"IAM role created: {arn}")
        return arn
    except client.exceptions.EntityAlreadyExistsException:
        logger.error(f"IAM role {role_name} already exists.")
    except client.exceptions.MalformedPolicyDocumentException as e:
        logger.error(f"Malformed policy document for role {role_name}: {e}")
        raise


def delete_iam_role(client, role_name):
    """
    Delete the specified IAM role.

    :param role_name: Name of the IAM role to delete
    :return: None
    """
    try:
        client.delete_role(RoleName=role_name)
        logger.info(f"IAM role {role_name} deleted")
    except client.exceptions.NoSuchEntityException:
        logger.error(f"Role {role_name} does not exist.")
