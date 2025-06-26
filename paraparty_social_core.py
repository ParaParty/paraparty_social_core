import os

from social_core.backends.open_id_connect import OpenIdConnectAuth


class ParaPartyOidc(OpenIdConnectAuth):
    name = "paraparty"

    def __init__(self, *args, **kwargs):
        """
        Initialize the backend, loading the OIDC endpoint from environment.
        """

        endpoint = os.environ.get('PARAPARTY_OIDC_ENDPOINT')
        self.CLIENT_ID = os.environ.get('PARAPARTY_OIDC_CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get('PARAPARTY_OIDC_CLIENT_SECRET')

        # Set the endpoint for this instance
        self.OIDC_ENDPOINT = endpoint.rstrip('/')
        super().__init__(*args, **kwargs)

    def get_key_and_secret(self) -> tuple[str, str]:
        """
        Retrieves the client ID and client secret from environment variables.
        """

        client_id = self.CLIENT_ID
        client_secret = self.CLIENT_SECRET

        return client_id, client_secret

    def get_user_details(self, response):
        attributes = response.get("attributes")

        return {
            "username": attributes.get("username"),
            "email": attributes.get("email"),
            "fullname": attributes.get("name"),
            "first_name": attributes.get("given_name"),
            "last_name": attributes.get("family_name"),
        }
