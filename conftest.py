"""
Shared test configuration and fixtures for SauceDemo Playwright test automation.
Provides browser lifecycle management, Actor fixture, and Allure evidence generation.
"""

import os
import logging
import pytest
import allure

from playwright.sync_api import sync_playwright, Page

from screenplay.actors.actor import Actor
#from screenplay.interactions import BrowseTheWeb
from screenplay.actors.browse_the_web import BrowseTheWeb

logger = logging.getLogger(__name__)

# Configuración de URLs y Tiempos para SauceDemo
SAUCEDEMO_BASE_URL = "https://saucedemo.com"
DEFAULT_TIMEOUT_MS = 5000  # 5 segundos de espera explícita máxima por elemento

def pytest_addoption(parser):
    """Add custom CLI options for browser configuration without duplicates."""
    known_options = set()
    for group in parser._groups:
        for opt in group.options:
            known_options.update(opt.names())

    if "--headed" not in known_options:
        parser.addoption(
            "--headed",
            action="store_true",
            default=False,
            help="Run browser in headed mode (visible window).",
        )

    parser.addoption(
        "--screenshot-mode",
        action="store",
        default="on-failure",  # Recomendado en CI/CD para optimizar almacenamiento
        choices=["always", "on-failure"],
        help="When to capture screenshots: 'always' or 'on-failure'.",
    )


@pytest.fixture(scope="function")
def page(request) -> Page:
    """Fixture que gestiona el ciclo de vida del navegador de forma sincrónica."""
    headed = request.config.getoption("--headed")
    
    with sync_playwright() as p:
        # Iniciamos el navegador según el parámetro CLI
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context()
        page = context.new_page()
        
        # Seteamos el tiempo de espera por defecto solicitado por el profesor
        page.set_default_timeout(DEFAULT_TIMEOUT_MS)
        
        yield page
        
        # Cierre seguro de instancias
        page.close()
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def actor(page: Page) -> Actor:
    """Fixture que provee el Actor inicializado con la habilidad de navegar."""
    ability = BrowseTheWeb(page, base_url=SAUCEDEMO_BASE_URL)
    return Actor(ability)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captura evidencias (Screenshots) automáticamente y las adjunta a Allure."""
    outcome = yield
    report = outcome.get_result()
    
    # Obtenemos la configuración de captura seleccionada por CLI
    screenshot_mode = item.config.getoption("--screenshot-mode")
    
    # Validamos las condiciones de captura (Si falló, o si la regla es 'siempre')
    should_screenshot = (
        (report.when == "call" and report.failed) or 
        (report.when == "call" and screenshot_mode == "always")
    )
    
    if should_screenshot:
        # Extraemos de forma segura la instancia de la fixture 'page' utilizada en el test
        page = item.funcargs.get("page")
        if page:
            # 1. Evidencia en archivo local para Jenkins Artifacts
            evidences_dir = "reports/screenshots"
            os.makedirs(evidences_dir, exist_ok=True)
            screenshot_path = f"{evidences_dir}/{item.name}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            
            # 2. Evidencia incrustada en Reporte Allure automáticamente
            try:
                allure.attach(
                    page.screenshot(full_page=True),
                    name=f"Evidence_{item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                logger.warning("Could not attach screenshot to Allure: %s", e)