import allure
from screenplay.ui import login_page
from screenplay.interactions.fill_field import FillField
from screenplay.interactions.click_element import ClickElement


class Login:
    """Task to authenticate a user against SauceDemo."""

    def __init__(self, username: str, password: str):
        # Mantenemos tus excelentes validaciones de negocio
        if not username or not username.strip():
            raise ValueError("Username is required and cannot be empty.")
        if not password or not password.strip():
            raise ValueError("Password is required and cannot be empty.")
        self._username = username
        self._password = password

    @staticmethod
    def with_credentials(username: str, password: str) -> "Login":
        """Factory method to create a Login task with fluent interface."""
        return Login(username, password)

    def perform_as(self, actor) -> None:
        # Aseguramos la navegación inicial limpia antes de interactuar
        page = actor.ability.page
        page.goto(actor.ability.base_url)

        with allure.step(f"Login as '{self._username}'"):
            actor.attempts_to(
                FillField(login_page.USERNAME_INPUT, self._username),
                FillField(login_page.PASSWORD_INPUT, self._password),
                ClickElement(login_page.LOGIN_BUTTON),
            )
            # Eliminamos networkidle. Playwright esperará automáticamente 
            # a que el inventario cargue en la siguiente interacción de forma explícita.
