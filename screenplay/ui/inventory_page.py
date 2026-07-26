# screenplay/ui/inventory_page.py

# Selector robusto (data-test) solicitado por tu profesor
SORT_DROPDOWN = "data-test=product-sort-container"
INVENTORY_ITEM_PRICE = "data-test=inventory-item-price"

def ITEM_PRICE_BY_NAME(product_name: str) -> str:
    """Locator dinámico robusto para extraer el precio de un producto específico."""
    return f"xpath=//div[@data-test='inventory-item-name' and text()='{product_name}']/ancestor::div[@data-test='inventory-item']//div[@data-test='inventory-item-price']"