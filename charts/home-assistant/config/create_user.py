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
        example curl:
        curl 'https://home-assistant.example.com/api/onboarding/analytics' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Origin: https://home-assistant.example.com' -H 'DNT: 1' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzNDNjZGYzMjkzNjk0MTY1YWE1ZDFiNjZiNWM0Nzc4MCIsImlhdCI6MTcxMjU2ODEzMywiZXhwIjoxNzEyNTY5OTMzfQ.YTZCFBcNyj-w9ebxHyFFngNTT9O2W8aiMtFwMeIEvt4' -H 'Connection: keep-alive' -H 'Content-Length: 0'
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

        Example curl to do the same thing:
        curl 'https://home-assistant.example.com/api/onboarding/core_config' --compressed -X POST -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Origin: https://home-assistant.example.com' -H 'DNT: 1' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzNDNjZGYzMjkzNjk0MTY1YWE1ZDFiNjZiNWM0Nzc4MCIsImlhdCI6MTcxMjU2ODEzMywiZXhwIjoxNzEyNTY5OTMzfQ.YTZCFBcNyj-w9ebxHyFFngNTT9O2W8aiMtFwMeIEvt4' -H 'Connection: keep-alive' -H 'Content-Length: 0' -H 'TE: trailers'
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

        # update the self cache to include the authorization token
        self.auth_code = response.json()["auth_code"]

    def create_token(self) -> dict:
        """
        create a token for further actions

        Example transaction, assuming auth code is:
        c920912280624b3da66bf1bac3a2a378

        curl 'https://home-assistant.example.com/auth/token' \
                --compressed \
                -X POST \
                -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0' \
                -H 'Accept: */*' \
                -H 'Accept-Language: en-US,en;q=0.5' \
                -H 'Accept-Encoding: gzip, deflate, br' \
                -H 'Content-Type: multipart/form-data; boundary=---------------------------12687640052594540745146787337' \
                -H 'Origin: https://home-assistant.example.com' \
                -H 'DNT: 1' \
                -H 'Sec-Fetch-Dest: empty' \
                -H 'Sec-Fetch-Mode: cors' \
                -H 'Sec-Fetch-Site: same-origin' \
                -H 'Connection: keep-alive' \
                -H 'TE: trailers' \
                --data-binary $'-----------------------------12687640052594540745146787337\r\nContent-Disposition: form-data; name="client_id"\r\n\r\nhttps://home-assistant.example.com/\r\n-----------------------------12687640052594540745146787337\r\nContent-Disposition: form-data; name="code"\r\n\r\nc920912280624b3da66bf1bac3a2a378\r\n-----------------------------12687640052594540745146787337\r\nContent-Disposition: form-data; name="grant_type"\r\n\r\nauthorization_code\r\n-----------------------------12687640052594540745146787337--\r\n'

        """
        token_url = f"{self.base_url}/auth/token"
        print("🐶".center(50,"🐕"))
        print(f"We're going to post to {token_url} for a new auth code")

        data_binary = f'-----------------------------12687640052594540745146787337\r\nContent-Disposition: form-data; name="client_id"\r\n\r\n{self.external_url}\r\n-----------------------------12687640052594540745146787337\r\nContent-Disposition: form-data; name="code"\r\n\r\n{self.auth_code}\r\n-----------------------------12687640052594540745146787337\r\nContent-Disposition: form-data; name="grant_type"\r\n\r\nauthorization_code\r\n-----------------------------12687640052594540745146787337--\r\n'

        headers = {
          'Accept-Encoding': 'gzip, deflate, br',
          'Content-Type': 'multipart/form-data; boundary=---------------------------12687640052594540745146787337',
          'Origin': self.external_url.rstrip('/'),
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-origin',
          'Connection': 'keep-alive',
          'TE': 'trailers'
        }

        response = requests.request("POST",
                                    token_url,
                                    headers=headers,
                                    data=data_binary)
        print(response.text)

        # update the headers to include the bearer token
        token = response.json().get("access_token", "")
        if token:
            # for ha_auth_provider: "homeassistant"
            self.headers['Authorization'] = f"Bearer {token}"

        # don't know if we need this, but might as well keep it in cache
        self.refresh_token = response.json().get("refresh_token", "")

        print("🐶".center(50,"🐕"))


if __name__ == '__main__':
    onboarding_obj = RunHomeAssistantOnboarding()
    onboarding_obj.create_user()
    onboarding_obj.create_token()
    onboarding_obj.run_core_config()
    onboarding_obj.run_integration_config()
    onboarding_obj.run_analytics_config()
