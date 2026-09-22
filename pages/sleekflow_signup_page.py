"""Page object for SleekFlow signup flows."""
from pages.sleekflow_auth_page import SleekFlowAuthPage


class SleekFlowSignupPage(SleekFlowAuthPage):
    """Interactions with the SleekFlow hosted signup screen."""

    EMAIL_INPUT = "input#email, input[type='email'], input[name='username']"
    PASSWORD_INPUT = "input#password"
    TERMS_CHECKBOX = "input[name='ulp-terms-of-service']"
    SIGNUP_BUTTON = "button[type='submit'][name='action'][value='default']"
    EMAIL_VERIFICATION_HEADING = "text=Confirm your email address"
    OTP_INPUT = (
        "input[name='code'], input[autocomplete='one-time-code'], "
        "input[inputmode='numeric'], input[maxlength='1']"
    )
    VERIFIED_EMAIL_CONTROL = "text=I've verified my email"
    CONTINUE_BUTTON = "button[type='submit'][name='action'][value='default']"
    SIGN_IN_LINK = "a:has-text('Sign in')"
    BODY = "body"

    def open_signup(self) -> None:
        """Open the signup screen."""
        self.navigate(self.SIGNUP_URL)
        self.wait_for_element(self.EMAIL_INPUT, timeout=self.page_load_timeout)
        self.wait_for_element(self.TERMS_CHECKBOX, timeout=self.page_load_timeout)
        self.wait_for_element(self.SIGNUP_BUTTON, timeout=self.page_load_timeout)

    def fill_email(self, email: str) -> None:
        """Enter an email address on the signup screen."""
        self.fill(self.EMAIL_INPUT, email)

    def accept_terms(self) -> None:
        """Accept the signup terms and privacy policy."""
        self.page.locator(self.TERMS_CHECKBOX).check(force=True)

    def submit_signup(self) -> None:
        """Submit the signup email form."""
        self.click(self.SIGNUP_BUTTON)

    def assert_signup_error(self, expected_message: str) -> None:
        """Assert that the signup form displays the expected validation text."""
        page_text = self.page.locator(self.BODY).inner_text().lower()
        validation_message = ""
        email_input = self.page.locator(self.EMAIL_INPUT).first
        if email_input.is_visible():
            validation_message = email_input.evaluate(
                "(element) => element.validationMessage"
            )
        assert (
            expected_message.lower() in page_text
            or expected_message.lower() in validation_message.lower()
        ), f"Expected signup validation was not displayed: {expected_message}"

    def complete_password_step(self, password: str) -> None:
        """Complete the password step shown after submitting a signup email."""
        self.wait_for_element(self.PASSWORD_INPUT, timeout=self.page_load_timeout)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SIGNUP_BUTTON)

    def open_login_from_signup(self) -> None:
        """Navigate to login using the link on the signup page."""
        self.click(self.page.locator(self.SIGN_IN_LINK))
        self.page.wait_for_url("**/u/login/**", timeout=self.navigation_timeout)
        self.wait_for_element(self.EMAIL_INPUT)

    def wait_for_signup_confirmation(self) -> None:
        """Wait until signup has advanced to email verification."""
        self.wait_for_element(
            self.EMAIL_VERIFICATION_HEADING, timeout=self.verification_timeout
        )

    def enter_otp(self, otp: str) -> None:
        """Enter the OTP displayed by the signup verification step."""
        inputs = self.page.locator(self.OTP_INPUT)
        inputs.first.wait_for(state="visible", timeout=self.verification_timeout)
        if inputs.count() == 1:
            inputs.fill(otp)
            return
        if inputs.count() < len(otp):
            raise ValueError("Verification code inputs do not match OTP length")
        for index, digit in enumerate(otp):
            inputs.nth(index).fill(digit)

    def submit_otp(self) -> None:
        """Submit the OTP verification form."""
        verified_control = self.page.locator(self.VERIFIED_EMAIL_CONTROL)
        if verified_control.is_visible():
            verified_control.click()
            return
        """"Implement functionality after signup is success"""
