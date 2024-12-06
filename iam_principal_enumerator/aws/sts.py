def get_current_account_id(client) -> str:
    return client.get_caller_identity()["Account"]
