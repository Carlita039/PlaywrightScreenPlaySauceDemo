Feature: Inventory Management in Swag Labs

  Background:
    Given the user "standard_user" logs into the Swag Labs platform

  Scenario: Successful login and sorting validation by price low to high
    When the user decides to sort products by "Price (low to high)"
    Then the first product listed should be the lowest price and the last should be the highest price

  Scenario: Price consistency validation in the catalog
    When the user views the list of available products
    Then the price of the product "Sauce Labs Backpack" must be "$29.99"
    And the price of the product "Sauce Labs Onesie" must be "$7.99"