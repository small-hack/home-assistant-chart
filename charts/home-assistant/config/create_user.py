import json
from os import environ as env
import requests


class RunHomeAssistantOnboarding():
    """
    Runs through home assistant onboarding to create a new user and disable registration

    home assistant user onboarding urls found here:
    https://github.com/home-assistant/core/tree/dev/homeassistant/components/onboarding/views.py
    """
    def __init__(self):
        self.headers = {
          'Content-Type': 'application/json',
        }
        self.base_url = f"http://{env.get('SERVICE', 'home-assistant:8124')}"
        self.external_url = env.get('EXTERNAL_URL', '')

    def run_analytics_config(self) -> dict:
        """
        runs the analytics config step of onboarding via the home assistant api
        """
        analytics_url = f"{self.base_url}/api/onboarding/analytics"
        print(f"We're going to post to {analytics_url} for analytics setup")

        response = requests.request("POST", analytics_url, headers=self.headers)
        print(response.text)

    def run_integration_config(self) -> dict:
        """
        runs the integration config step of onboarding via the home assistant api
        """
        integration_url = f"{self.base_url}/api/onboarding/integration"
        print(f"We're going to post to {integration_url} for integration config")

        response = requests.request("POST", integration_url, headers=self.headers)
        print(response.text)

    def run_core_config(self) -> dict:
        """
        runs the core config step of onboarding via the home assistant api
        """
        core_config_url = f"{self.base_url}/api/onboarding/core_config"
        print(f"We're going to post to {core_config_url} for finishing the core config")

        response = requests.request("POST", core_config_url, headers=self.headers)
        print(response.text)

    def create_user(self) -> dict:
        """
        creates a user via the home assistant api
        """
        user_url = f"{self.base_url}/api/onboarding/users"
        print(f"We're going to post to {user_url} for user creation")

        client_id = self.external_url
        if not client_id:
            client_id = self.base_url + "/"

        payload = json.dumps({
          "client_id": client_id,
          "name": env.get('ADMIN_NAME', 'admin'),
          "username": env.get('ADMIN_USERNAME', 'admin'),
          "password": env.get('ADMIN_PASSWORD', 'test'),
          "language": env.get('ADMIN_LANGUAGE', 'en')
        })

        # this is the api request actually creates the new user and returns something like:
        # {"auth_code":"23456y7uiobgdfghjm54873hfjkdfghj"}
        response = requests.request("POST", user_url, headers=self.headers, data=payload)
        print(response.text)

        # update the headers to include the authorization token
        token = response.json()["auth_code"]
        self.headers['Authorization'] = f"auth_code {token}"

    def create_token(self) -> dict:
        token_url = f"{self.base_url}/auth/token"
        print("🐶".center(50,"🐕"))
        print(f"We're going to post to {token_url} for a new auth code")

        payload = json.dumps({
          "client_id": self.base_url,
          "username": env.get('ADMIN_USERNAME', 'admin'),
          "password": env.get('ADMIN_PASSWORD', 'test'),
          "grant_type": "authorization_code"

        })

        response = requests.request("POST", token_url, headers=self.headers, data=payload)
        print(response.text)
        # update the headers to include the authorization token
        token = response.json().get("auth_code", "")
        if token:
            self.headers['Authorization'] = f"auth_code {token}"

        print("🐶".center(50,"🐕"))
        print(f"We're going to post to {token_url} for a new token")

        payload = json.dumps({
          "client_id": self.base_url,
          "username": env.get('ADMIN_USERNAME', 'admin'),
          "password": env.get('ADMIN_PASSWORD', 'test'),
          "grant_type": "refresh_token"

        })

        response = requests.request("POST", token_url, headers=self.headers, data=payload)
        print(response.text)
        print("🐶".center(50,"🐕"))


if __name__ == '__main__':
    onboarding_obj = RunHomeAssistantOnboarding()
    onboarding_obj.create_user()
    onboarding_obj.create_token()
    onboarding_obj.run_core_config()
    onboarding_obj.run_integration_config()
    onboarding_obj.run_analytics_config()
