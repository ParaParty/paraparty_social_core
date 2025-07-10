import json
import os
import html

from social_core.backends.open_id_connect import OpenIdConnectAuth


class ParaPartyOidc(OpenIdConnectAuth):
    name = "paraparty"

    ID_KEY = 'username'
    USERNAME_KEY = 'username'

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

    def uses_redirect(self):
        """
        Make Weblate Happy
        """
        return False

    def auth_html(self):
        """
        Make Weblate Happy

        Return an HTML page that redirects the user to the authorization URL.
        """
        url = self.auth_url()
        safe_url = html.escape(url, quote=True)
        safe_url_json = json.dumps(url)

        return f"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url={safe_url}">
    <title>Redirecting...</title>
    <script>window.location.href = {safe_url_json};</script>
</head>
<body>
    <p>Redirecting to <a href="{safe_url}">this page</a>. If you are not redirected automatically, click the link.</p>
</body>
</html>"""
