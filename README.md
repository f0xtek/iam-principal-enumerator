# IAM Principal Enumerator

CLI application that performs unauthenticated IAM principal enumeration against a target AWS account.

The application accepts a custom wordlist containing principal names, and uses these to check for the existence of IAM principals in a target AWS account by attempting to update the trust policy of an attacker-controlled IAM role with the ARN of an IAM principal (user or role) in the target AWS account.

The error message received when updating the trust policy will determine if the IAM princiapl exists in the target account or not.
