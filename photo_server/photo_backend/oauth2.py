from social_core.backends.cognito import CognitoOAuth2


class Cognito(CognitoOAuth2):
    EXTRA_DATA = [
        ("picture", "picture"),
        ("email", "email"),
        ("name", "name"),
    ]

    def get_user_details(self, response):
        res = super().get_user_details(response)
        res["name"] = response["name"]
        return res

    def user_data(self, access_token, *args, **kwargs):
        """Grab user profile information from Cognito."""

        response = self.get_json(
            url=self.user_data_url(),
            headers={"Authorization": "Bearer {}".format(access_token)},
        )

        user_data = {
            "given_name": response.get("given_name"),
            "family_name": response.get("family_name"),
            "username": response.get("username"),
            "email": response.get("email"),
            "picture": response.get("picture"),
            "name": response.get("name"),
        }

        return user_data
