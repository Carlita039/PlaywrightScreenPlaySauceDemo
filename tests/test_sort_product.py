import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Importación de la arquitectura Screenplay
from screenplay.actors.actor import Actor
from screenplay.tasks.login import Login
from screenplay.tasks.sort_product import SortProducts
from screenplay.questions.inventory_question import ProductPrices, SingleProductPrice

# Vinculación del archivo en inglés
scenarios('../features/swag_labs.feature')


# Cambiamos a parseador por expresiones regulares para evitar conflictos con comillas
@given(parsers.re(r'the user "(?P<username>[^"]+)" logs into the Swag Labs platform'))
def login_step(actor: Actor, username: str) -> None:
    actor.attempts_to(
        Login.with_credentials(username, "secret_sauce")
    )


@when(parsers.re(r'the user decides to sort products by "(?P<option>[^"]+)"'))
def sort_products_step(actor: Actor, option: str) -> None:
    actor.attempts_to(
        SortProducts.by_option(option)
    )


@when('the user views the list of available products')
def view_products_step(actor: Actor) -> None:
    pass


@then('the first product listed should be the lowest price and the last should be the highest price')
def verify_sorting_step(actor: Actor) -> None:
    precios = actor.asks_about(ProductPrices())
    assert precios == sorted(precios), f"Error: Prices are not sorted. Got: {precios}"


# Cambiamos a parseador por expresiones regulares para capturar el nombre del producto y su precio
@then(parsers.re(r'the price of the product "(?P<product_name>[^"]+)" must be "(?P<expected_price>[^"]+)"'))
def verify_individual_product_price_step(actor: Actor, product_name: str, expected_price: str) -> None:
    precio_obtenido = actor.asks_about(SingleProductPrice.for_item(product_name))
    assert precio_obtenido == expected_price, (
        f"Error on '{product_name}': expected '{expected_price}' but read '{precio_obtenido}'."
    )