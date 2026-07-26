from screenplay.ui import inventory_page


class ProductPrices:
    """Pregunta que extrae todos los precios numéricos visibles en pantalla de forma sincrónica."""

    def answered_by(self, actor) -> list[float]:
        # Acceso directo y síncrono a la página a través de la propiedad de tu Actor
        page = actor.ability.page
        
        # Playwright localiza todos los elementos y extrae el texto linealmente
        price_locator = page.locator(inventory_page.INVENTORY_ITEM_PRICE)
        price_locator.first.wait_for(state="visible", timeout=5000) # Espera explícita
        
        price_elements = price_locator.all_text_contents()
        
        # Convertimos los textos (ej. "$29.99") a flotantes (29.99) para poder ordenarlos matemáticamente
        return [float(price.replace("$", "")) for price in price_elements]


class SingleProductPrice:
    """Pregunta que extrae el precio en formato texto de un producto específico."""

    def __init__(self, product_name: str):
        self._product_name = product_name

    @staticmethod
    def for_item(product_name: str) -> "SingleProductPrice":
        """Factory method para uso fluido en los steps."""
        return SingleProductPrice(product_name)

    def answered_by(self, actor) -> str:
        page = actor.ability.page
        
        # Construimos el selector dinámico robusto
        selector = inventory_page.ITEM_PRICE_BY_NAME(self._product_name)
        price_locator = page.locator(selector)
        
        # Espera explícita antes de leer el valor de la interfaz
        price_locator.wait_for(state="visible", timeout=5000)
        
        return price_locator.text_content()