from pytest_bdd import scenarios, given, when, then, parsers
from screenplay.actors import Actor
from screenplay.interactions import BrowseTheWeb
from screenplay.tasks.login import Login
from screenplay.questions.inventory_question import ProductPrices
from screenplay.ui import inventory_page
from playwright.async_api import Page
import pytest

scenarios('../features/swag_labs.feature')

@pytest.fixture
def actor(page: Page):
    # Inicializa el actor con la habilidad de navegar
    return Actor("Tester").can(BrowseTheWeb(page))

@given(parsers.parse('que el usuario "{usuario}" ingresa a la plataforma Swag Labs'))
async def login_step(actor, usuario):
    await actor.attempts_to(Login.with_credentials(usuario, "secret_sauce"))

@when(parsers.parse('decide ordenar los productos por "{option}"'))
async def sort_products(actor, option):
    page = BrowseTheWeb.as_(actor)
    # Playwright maneja internamente la espera para interactuar
    await page.select_option(inventory_page.SORT_DROPDOWN, label=option)

@then('debería observar que el primer producto listado es el de menor precio y el último el de mayor precio')
async def verify_sorting(actor):
    precios = await actor.asks_for(ProductPrices())
    assert precios == sorted(precios), f"Los precios no están ordenados ascendentemente: {precios}"

@then(parsers.parse('el precio del producto "{item_name}" debe ser "{expected_price}"'))
async def verify_item_price(actor, item_name, expected_price):
    page = BrowseTheWeb.as_(actor)
    locator = inventory_page.ITEM_NAME_SELECTOR(item_name)
    actual_price = await page.locator(locator).text_content()
    assert actual_price == expected_price, f"Esperado {expected_price} pero se obtuvo {actual_price}"