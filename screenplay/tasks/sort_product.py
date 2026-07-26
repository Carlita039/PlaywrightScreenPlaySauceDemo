import allure
from screenplay.ui import inventory_page


class SortProducts:
    """Task to sort products in the inventory page by a specific option."""

    def __init__(self, option: str):
        if not option or not option.strip():
            raise ValueError("The sorting option cannot be empty.")
        self._option = option

    @staticmethod
    def by_option(option: str) -> "SortProducts":
        """Factory method to create the task using a fluent interface."""
        return SortProducts(option)

    def perform_as(self, actor) -> None:
        # Extraemos la instancia de la página desde la habilidad del actor
        page = actor.ability.page

        with allure.step(f"Sort products by: '{self._option}'"):
            # Localizador robusto centralizado
            dropdown = page.locator(inventory_page.SORT_DROPDOWN)
            
            # Espera explícita implícita: espera que el componente sea visible y accionable
            dropdown.wait_for(state="visible", timeout=5000)
            
            # Playwright selecciona directamente por el texto visible (Label)
            dropdown.select_option(label=self._option)