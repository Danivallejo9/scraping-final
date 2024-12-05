# -*- coding: utf-8 -*-
"""scraping-final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YWKrZJbiLTJfrRkktM_ES0-yXxH7xILP
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller
import pandas as pd

# Instalar automáticamente el ChromeDriver
chromedriver_autoinstaller.install()

# Configuración del navegador
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Modo sin cabeza (sin interfaz gráfica)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def main_function():
    # Configuración y scraping de eBay
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)

    # Acceder a la página de eBay
    driver.get('https://www.ebay.com/sch/i.html?_nkw=monitor')

    time.sleep(5)

    productos = []
    precios = []

    while True:
        items = driver.find_elements(By.CSS_SELECTOR, '.s-item__title')
        prices = driver.find_elements(By.CSS_SELECTOR, '.s-item__price')
        
        for item, price in zip(items, prices):
            productos.append(item.text)
            precios.append(price.text)

        try:
           next_button = driver.find_element(By.CSS_SELECTOR, '.pagination__next')
           next_button.click()
           time.sleep(5)
        except Exception as e:
            break

    # Cierra el navegador
    driver.quit()

    # Devuelve los datos en formato DataFrame
    data = pd.DataFrame({
        'Producto': productos,
        'Precio': precios
    })

    # Guardar el DataFrame como CSV
    data.to_csv('productos_ebay.csv', index=False, encoding='utf-8')
    print("Archivo CSV guardado como 'productos_ebay.csv'.")

    return data