"""Page objects for SleekFlow authentication flows."""
from pages.sleekflow_login_page import SleekFlowLoginPage
from pages.sleekflow_signup_page import SleekFlowSignupPage


class SleekFlowAutomationPage(SleekFlowLoginPage, SleekFlowSignupPage):
    """Page object for SleekFlow signup and login automation."""

    def signup(self, email: str, password: str) -> None:
        """Submit a new email through the signup flow."""
        self.open_signup()
        self.fill_email(email)
        self.accept_terms()
        self.submit_signup()
        self.complete_password_step(password)

    def signup_and_wait_for_verification(self, email: str, password: str) -> None:
        """Submit signup and wait for the verification handoff."""
        self.signup(email, password)
        self.wait_for_signup_confirmation()

    def signup_with_otp(self, email: str, password: str, otp_api_url: str) -> dict:
        """Submit signup, fetch its OTP from an API, and enter it without provider verification."""
        import json
        from urllib.parse import quote
        from urllib.request import urlopen

        self.signup_and_wait_for_verification(email, password)
        with urlopen(f"{otp_api_url}/api/test/otp?email={quote(email)}", timeout=10) as response:
            otp_response = json.load(response)
        if otp_response.get("email") != email or not otp_response.get("otp"):
            raise ValueError("OTP API response must contain matching email and a non-empty otp")
        self.enter_otp(otp_response["otp"])
        return otp_response

    def signup_and_capture_dummy_otp(
        self, email: str, password: str, otp_api_url: str
    ) -> dict:
        """Backward-compatible alias for entering the API-driven OTP."""
        return self.signup_with_otp(email, password, otp_api_url)

    def signup_and_enter_dummy_otp(
        self, email: str, password: str, otp_api_url: str
    ) -> dict:
        """Enter a locally supplied OTP while leaving provider verification explicit."""
        return self.signup_with_otp(email, password, otp_api_url)

    def login_with_credentials(self, email: str, password: str) -> None:
        """Complete the two-step SleekFlow login flow."""
        self.open_login()
        self.login(email, password)
        self.wait_for_login_redirect()

    def login_with_google(self) -> None:
        """Open Google's authorization flow from SleekFlow."""
        self.open_login()
        self.select_google_login()

    def login_with_google_credentials(self, username: str, password: str) -> None:
        """Open Google OAuth and submit supplied test credentials."""
        self.login_with_google()
        self.enter_google_credentials(username, password)
        self.wait_for_google_login_redirect()

    def login_with_apple(self) -> None:
        """Open Apple's authorization flow from SleekFlow."""
        self.open_login()
        self.select_apple_login()
