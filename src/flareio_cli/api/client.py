import flareio


def get_api_client() -> flareio.FlareApiClient:
    client = flareio.FlareApiClient.from_env()

    # Update the User-Agent
    user_agent_maybe: str | bytes = client._session.headers.get("User-Agent") or ""
    user_agent_str: str = (
        user_agent_maybe.decode()
        if isinstance(user_agent_maybe, bytes)
        else user_agent_maybe
    )
    user_agent_str = f"flareio-cli {user_agent_str}"
    client._session.headers["User-Agent"] = user_agent_str

    return client
