"""Page object for SleekFlow login and OAuth flows."""
from pages.sleekflow_auth_page import SleekFlowAuthPage
from utils.config_reader import config


class SleekFlowLoginPage(SleekFlowAuthPage):
    """Interactions with the SleekFlow hosted login screen."""

    LOGIN_HEADING = "h1:has-text('Welcome back')"
    LOGIN_SUBHEADING = "p"
    LANGUAGE_SELECT = "#language-select"
    LANGUAGE_LABEL = "#selected-language-label"
    LANGUAGE_DROPDOWN = "#language-dropdown"
    LANGUAGE_OPTION = "#language-dropdown"
    LOGO_IMAGE = "img[src*='Black_logo']"
    EDIT_IDENTIFIER_LINK = "a:has-text('Edit')"
    SHOW_PASSWORD_BUTTON = "button[aria-label='Show password']"
    HIDE_PASSWORD_BUTTON = "button[role='switch'][aria-checked='true']"

    def open_login(self) -> None:
        """Open the login screen."""
        self.navigate(self.LOGIN_URL)
        self.wait_for_element(self.EMAIL_INPUT, timeout=self.page_load_timeout)
        self.wait_for_element(self.LOGIN_HEADING, timeout=self.page_load_timeout)
        self.wait_for_element(self.LOGO_IMAGE, timeout=self.page_load_timeout)

    def fill_email(self, email: str) -> None:
        """Enter an email address on the login screen."""
        self.fill(self.EMAIL_INPUT, email)

    def submit_identifier(self) -> None:
        """Submit the login identifier and wait for the password step."""
        self.click(self.CONTINUE_BUTTON)

    def assert_login_error(self, expected_message: str) -> None:
        """Assert that the login page displays the expected error message."""
        page_text = self.page.locator("body").inner_text()
        assert (
            expected_message in page_text
        ), f"Expected login error was not displayed: {expected_message}"

    def get_button(self, name: str):
        """Return a login-page button by its accessible name."""
        return self.page.get_by_role("button", name=name, exact=True)

    def assert_login_buttons(self, expected_buttons: list[str]) -> None:
        """Assert that configured login buttons are visible, enabled, and labeled."""
        for button_name in expected_buttons:
            button = self.get_button(button_name)
            assert button.is_visible(), f"Login button is not visible: {button_name}"
            assert button.is_enabled(), f"Login button is disabled: {button_name}"
            assert button.inner_text().strip() == button_name

    def assert_login_text(self, expected: dict[str, str]) -> None:
        """Assert the configured login-page text and navigation link."""
        assert self.get_text(self.LOGIN_HEADING) == expected["heading"]
        assert (
            self.page.locator(self.LOGIN_SUBHEADING)
            .filter(has_text=expected["subheading"])
            .is_visible()
        )
        assert self.page.get_by_text(
            expected["account_prompt"], exact=False
        ).first.is_visible()
        assert self.page.get_by_role(
            "link", name=expected["signup_link"], exact=True
        ).is_visible()

    def open_signup_from_login(self) -> None:
        """Navigate to signup using the link on the login page."""
        self.click(self.page.get_by_role("link", name="Sign up", exact=True))
        self.page.wait_for_url("**/u/signup/**", timeout=self.navigation_timeout)
        self.wait_for_element(self.EMAIL_INPUT)

    def open_language_dropdown(self) -> None:
        """Open the login-page language selector."""
        self.click(self.LANGUAGE_LABEL)
        self.wait_for_element(self.LANGUAGE_DROPDOWN)

    def select_language(self, option_id: str) -> None:
        """Select a language from the language dropdown."""
        self.click(f"{self.LANGUAGE_OPTION} #{option_id}")

    def continue_login(self) -> None:
        """Advance from the login email step to the password step."""
        self.submit_identifier()
        self.wait_for_element(self.PASSWORD_INPUT)
        self.wait_for_element(self.page.get_by_text("Edit", exact=True))
        self.wait_for_element(
            self.page.get_by_role("switch", name="Show password", exact=True)
        )

    def edit_login_identifier(self) -> None:
        """Return from the password step to edit the login identifier."""
        self.page.get_by_text("Edit", exact=True).click()
        self.wait_for_element(self.EMAIL_INPUT, timeout=self.page_load_timeout)

    def toggle_password_visibility(self) -> None:
        """Toggle visibility of the password field."""
        self.page.get_by_role("switch", name="Show password", exact=True).click()

    def select_google_login(self) -> None:
        """Select Google authentication from the login screen."""
        self.click(self.GOOGLE_BUTTON)

    def select_apple_login(self) -> None:
        """Select Apple authentication from the login screen."""
        self.click(self.APPLE_BUTTON)

    def enter_google_credentials(self, username: str, password: str) -> None:
        """Enter configured Google credentials and submit the OAuth form."""
        self.wait_for_url("https://accounts.google.com/**", timeout=self.oauth_timeout)
        self.fill(self.GOOGLE_EMAIL_INPUT, username)
        self.click(self.GOOGLE_NEXT_BUTTON)
        self.wait_for_element(
            self.GOOGLE_PASSWORD_INPUT, timeout=self.oauth_timeout
        )
        self.fill(self.GOOGLE_PASSWORD_INPUT, password)
        self.click(self.GOOGLE_PASSWORD_NEXT_BUTTON)

    def wait_for_google_login_redirect(self) -> None:
        """Wait for Google OAuth to return to the SleekFlow app."""
        self.wait_for_url(self.APP_URL_PATTERN, timeout=self.oauth_timeout)

    def login(self, email: str, password: str) -> None:
        """Complete the two-step email and password login flow."""
        self.fill_email(email)
        self.continue_login()
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.CONTINUE_BUTTON)

    def wait_for_login_redirect(self) -> None:
        """Wait until authentication leaves the hosted SSO page."""
        self.wait_for_url(self.APP_URL_PATTERN, timeout=self.navigation_timeout)

    def verify_logged_in(self) -> bool:
        """Verify that the browser is on the authenticated SleekFlow app."""
        return (
            self.SSO_HOST not in self.page.url
            and self.page.url.startswith(f"{config.base_url}/")
        )

    def capture_authenticated_element(self) -> str:
        """Capture a visible element from the authenticated landing page."""
        self.wait_for_element(
            self.AUTHENTICATED_HEADING, timeout=self.verification_timeout
        )
        element_text = self.get_text(self.AUTHENTICATED_HEADING)
        self.logger.info("Authenticated element captured: %s", element_text)
        return element_text
