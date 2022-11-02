"""
SCRAPING A MOUSERCISE
PREREQUISITOS
1.- Descargar ChromeDriver: "https://chromedriver.storage.googleapis.com/index.html?path=106.0.5249.61/" 
y colocarlo dentro del proyecto.
2.- Instalar la librería Selenium: pip install selenium.
3.- Instalar pyautogui, para el manejo del cursor.
4.- Se creó un sistema de reglas (dict). Contiene la orden a seguir dentro de la página,
la localización de elementos a scrapear, la instrucción a ejecutar.

"""

import pyautogui
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time
from pathlib import Path


# Sistema de reglas
dictionary = {
    'Intro: Click en el botón para empezar': {
        'paso1': [By.XPATH, '/html/body/table[2]/tbody/tr[2]/td/form/input','click']
    },
    'Página1: Click en número 1': {
        'paso1': [By.CSS_SELECTOR, 'a.bigger', 'click']
    },
    'Página2: Click en número 2 ': {
        'paso1': [By.CSS_SELECTOR, 'a.bigger', 'click']
    },
    'Página 3: Click en el número 3': {
        'paso1': [By.CSS_SELECTOR, 'a.bigger', 'click']
    },
    'Página 4: Click en el número 4': {
        'paso1': [By.CSS_SELECTOR, 'a.bigger', 'click']
    },
    'Página 5: Click en el número 5': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr/td/a', 'click']
    },
    'Página 6: Click en el número 6': {
        'paso1': [By.CSS_SELECTOR, 'a.smaller', 'click']
    },
    'Página 7: Click en el número 7': {
        'paso1': [By.CSS_SELECTOR, 'a.smaller', 'click']
    },
    'Página 8: Click en el número 8': {
        'paso1': [By.CSS_SELECTOR, 'a.smaller', 'click']
    },
    'Página 9: Click en el número 9': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[3]/td/a[2]', 'click']
    },
    'Página 10: Click en el número 10': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[3]/td/a[2]', 'click']
    },
    'Página 11: Click en el número 11': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[3]/td/a[2]', 'click']
    },
    'Página 12: Click en el número 12': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[3]/td/a[2]', 'click']
    },
    'Página 13: Click en el número 13': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[3]/td/a[2]', 'click']
    },
    'Página 14: Click en Proxima con hipervínculo': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[2]/td[4]/a', 'click']
    },
    'Página 15: Click en ¿Dónde está el ratón?': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[2]/td/a', 'click']
    },
    'Página 16: Click en ¡Pulse ahora!': {
        'paso1': [By.CSS_SELECTOR, '[name="clicker"]', 'click']
    },
    'Página 17: Click en Continua': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr/td/form/input', 'click']
    },
    'Página 18: Click en ¡Oye esto está buenísimo!': {
        'paso1': [By.CSS_SELECTOR, '[type="submit"]', 'click']
    },
    'Página 19: Click en Pulse Aqui ': {
        'paso1': [By.CSS_SELECTOR, '[type="image"]', 'click']
    },
    'Página 20: Pulse en las llaves': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[2]/td[3]/a/img', 'click']
    },
    'Página 21: Pulse en la roca': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[3]/td[2]/a/img', 'click']
    },
    'Página 22: Pulse todos los botones y luego en Continua': {
        'paso1': [By.CSS_SELECTOR, '[name="b1"]', 'click'],
        'paso2': [By.CSS_SELECTOR, '[name="b2"]', 'click'],
        'paso3': [By.CSS_SELECTOR, '[name="b3"]', 'click'],
        'paso4': [By.CSS_SELECTOR, '[name="b4"]', 'click'],
        'paso5': [By.CSS_SELECTOR, '[name="b5"]', 'click'],
        'paso6': [By.CSS_SELECTOR, '[name="b6"]', 'click'],
        'paso7': [By.CSS_SELECTOR, '[name="b7"]', 'click'],
        'paso8': [By.CSS_SELECTOR, '[name="b8"]', 'click'],
        'paso9': [By.CSS_SELECTOR, '[name="b9"]', 'click'],
        'paso10': [By.CSS_SELECTOR, '[name="b10"]', 'click'],
        'paso11': [By.CSS_SELECTOR, '[name="b11"]', 'click'],
        'paso12': [By.CSS_SELECTOR, '[name="advance"]', 'click'],
    },

    'Página 23: Pulse todos los botones y luego en Continua': {
        'paso1': [By.CSS_SELECTOR, '[name="alien"]', 'click'],
        'paso2': [By.XPATH, '/html/body/div/table/tbody/tr[4]/td[1]/img', 'click'],
        'paso3': [By.XPATH, '/html/body/div/table/tbody/tr[3]/td[1]/form/input', 'click'],
        'paso4': [By.XPATH, '/html/body/div/table/tbody/tr[2]/td[1]/form/input', 'click'],
        'paso5': [By.XPATH, '/html/body/div/table/tbody/tr[2]/td[3]/form/input', 'click'],
        'paso6': [By.XPATH, '/html/body/div/table/tbody/tr[3]/td[3]/img', 'click'],
        'paso7': [By.CSS_SELECTOR, '[name="metal"]', 'click'],
        'paso8': [By.CSS_SELECTOR, '[name="advance"]', 'click'],
    },
    'Página 24: Pulse doble click sobre los cohetes y luego click en Continua': {
        'paso1': [By.CSS_SELECTOR, '[name="f1"]', 'dobleclick'],
        'paso2': [By.CSS_SELECTOR, '[name="f2"]', 'dobleclick'],
        'paso3': [By.CSS_SELECTOR, '[name="f3"]', 'dobleclick'],
        'paso4': [By.CSS_SELECTOR, '[name="f4"]', 'dobleclick'],
        'paso5': [By.CSS_SELECTOR, '[name="f5"]', 'dobleclick'],
        'paso6': [By.CSS_SELECTOR, '[name="f6"]', 'dobleclick'],
        'paso7': [By.CSS_SELECTOR, '[name="f7"]', 'dobleclick'],
        'paso8': [By.CSS_SELECTOR, '[name="f8"]', 'dobleclick'],
        'paso9': [By.CSS_SELECTOR, '[name="advance"]', 'click'],
    },
    'Página 25: Pulse el slider y arrástrelos para cambiar color, luego click en Continua': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[1]/div/div[2]', 'handle'],
        'paso2': [By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/div[2]', 'handle'],
        'paso3': [By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td[3]/div/div[2]', 'handle'],
        'paso4': [By.XPATH, '/html/body/table/tbody/tr[3]/td/a', 'click'],

    },
    'Página 26: Scroll down y click en Próxima': {
        'paso1': ['', '', 'scrolldown'],
        'paso2': [By.CSS_SELECTOR, 'a.bigger', 'click']

    },
    'Página 27: Scroll down y click en Próxima': {
        'paso1': ['', '', 'scrolldown'],
        'paso2': [By.CSS_SELECTOR, 'a.bigger', 'click']
    },
    'Página 28: Scroll down y click en Próxima': {
        'paso1': ['', '', 'scrolldown'],
        'paso2': [By.CSS_SELECTOR, 'a.bigger', 'click']

    },
    'Página 29: Scroll right y click en Próxima': {
        'paso1': ['', '', 'scrollright'],
        'paso2': [By.CSS_SELECTOR, 'a.bigger', 'click']

    },
    'Página 30: Scroll down, scroll right y click en Próxima': {
        'paso1': ['', '', 'scrolldown'],
        'paso2': ['', '', 'scrollright'],
        'paso3': [By.XPATH, '/html/body/div/table/tbody/tr/td[2]/p/a', 'click']

    },
    'Página 31: Click en hipervínculo, luego click en Aceptar de la alerta': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr/td/a', 'click'],
        'paso2': [By.XPATH, '/html/body/table/tbody/tr/td/a', 'prompt']

    },
    'Página 32: Mover el puntero por el laberinto, luego clicn en Continua': {
        'paso1': ['', '', 'mouse'],
        'paso2': [By.XPATH, '/html/body/table/tbody/tr/td[2]/span/a', 'click'],
    },
    'Página 33: Check en todas las opciones y luego click en Continua': {
        'paso1': [By.XPATH, '/html/body/form/input[1]', 'click'],
        'paso2': [By.XPATH, '/html/body/form/input[2]', 'click'],
        'paso3': [By.XPATH, '/html/body/form/input[3]', 'click'],
        'paso4': [By.XPATH, '/html/body/form/input[4]', 'click'],
        'paso5': [By.XPATH, '/html/body/form/input[5]', 'click'],
        'paso6': [By.XPATH, '/html/body/form/input[6]', 'click'],
        'paso7': [By.XPATH, '/html/body/form/input[7]', 'click'],
        'paso8': [By.XPATH, '/html/body/form/input[8]', 'click'],
        'paso9': [By.XPATH, '/html/body/form/input[9]', 'click'],
        'paso10': [By.CSS_SELECTOR, '[name="advance"]', 'click'],
    },
    'Página 34: Check en cualquier casilla, luego click en Continua': {
        'paso1': [By.CSS_SELECTOR, '[name="sample"]', 'click'],
        'paso2': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/input[7]', 'click'],
    },
    'Página 35: Click en cada uno de los radiobutton, luego click en Continua': {
        'paso1': [By.XPATH, '/html/body/form/input[1]', 'click'],
        'paso2': [By.XPATH, '/html/body/form/input[2]', 'click'],
        'paso3': [By.XPATH, '/html/body/form/input[3]', 'click'],
        'paso4': [By.XPATH, '/html/body/form/input[4]', 'click'],
        'paso5': [By.XPATH, '/html/body/form/input[5]', 'click'],
        'paso6': [By.XPATH, '/html/body/form/input[6]', 'click'],
        'paso7': [By.XPATH, '/html/body/form/input[7]', 'click'],
        'paso8': [By.XPATH, '/html/body/form/input[8]', 'click'],
        'paso9': [By.XPATH, '/html/body/form/input[9]', 'click'],
        'paso10': [By.CSS_SELECTOR, '[name="advance"]', 'click'],
    },
    'Página 36: Check en cualquier radiobutton, luego click en Continua': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/input[1]', 'click'],
        'paso2': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/input[5]', 'click'],
    },
    'Página 37: Seleccionar Cinco, luego click en Continua': {
        'paso1': [By.CSS_SELECTOR, '[name="theChoices"]', 'click'],
        'paso2': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/select/option[6]', 'click'],
        'paso3': [By.CSS_SELECTOR, '[name="advance"]', 'click'],
    },
    'Página 38: Seleccionar cualquier opción, luego click en Continua': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/select', 'click'],
        'paso2': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/select/option[3]', 'click'],
        'paso3': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/input', 'click'],
    },
    'Página 39: Seleccionar Seis, luego click en Continua': {
        'paso1': [By.CSS_SELECTOR, '[name="theChoices"]', 'scrolltag'],
        'paso2': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/select/option[6]', 'click'],
        'paso3': [By.CSS_SELECTOR, '[name="advance"]', 'click'],
    },
    'Página 40: Seleccionar cualquier opción, luego click en Continua': {
        'paso1': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/select', 'scrolltag'],
        'paso2': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/select/option[6]', 'click'],
        'paso3': [By.XPATH, '/html/body/table/tbody/tr[2]/td/form/input', 'click'],
    },
    'Página 41: Escribir Nombre y Apellido en las respectivos campos, luego click en Continua': {
        'paso1': [By.CSS_SELECTOR, '[name="fname"]', 'Douglas', 'sendkey'],
        'paso2': [By.CSS_SELECTOR, '[name="lname"]', 'Vásquez', 'sendkey'],
        'paso3': [By.XPATH, '/html/body/form/input[3]', 'click'],
    }
}

def main():
    # Localizar la ruta del driver de Chrome.
    driver_path = str(Path.cwd())+"\prueba3\chromedriver.exe"
    options = webdriver.ChromeOptions()
    # Configuración de ejecución: Se deshabilitan las extensiones que tenga instalado el navegador y se manda la orden que se maximice.
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    # Abrimos el driver con la respectiva configuración.
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    # Se envía la página a scrapear
    driver.get('http://www.pbclibrary.org/raton/mousercise.htm')
    
    # En cada iteración se va a ejecutar cada una de las instrucciones dadas en el sistema de reglas.
    for elem in dictionary.values():
        action = ActionChains(driver)
        for x in elem.values():
            if x[-1] == 'click':
                # Se ejecuta un click
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((x[0], x[1]))).click()
                time.sleep(1)
            elif x[-1] == 'dobleclick':
                doble_click = driver.find_element(x[0], x[1])
                action.double_click(doble_click).perform()
                time.sleep(1)
            elif x[-1] == 'handle':
                handle = driver.find_element(x[0], x[1])
                action.click_and_hold(handle).move_by_offset(
                    0, 100).release().perform()
                time.sleep(1)
            elif x[-1] == 'scrolldown':
                driver.execute_script(
                    'window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(1)
            elif x[-1] == 'scrollright':
                driver.execute_script('window.scrollTo(1000,0)')
                time.sleep(1)
            elif x[-1] == 'prompt':
                alert = driver.switch_to.alert
                alert.accept()
                time.sleep(1)
            elif x[-1] == 'mouse':
                pyautogui.moveTo(1500,400,2)
                pyautogui.moveTo(1650,400,2)
                pyautogui.moveTo(1650,200,2)
                pyautogui.moveTo(1870,200,2)
                pyautogui.moveTo(1870,450,2)
                pyautogui.moveTo(1650,450,2)
                pyautogui.moveTo(1650,550,2)
            elif x[-1] == 'scrolltag':
                tag = driver.find_element(x[0], x[1])
                scroll_origin = ScrollOrigin.from_element(tag)
                action.scroll_from_origin(scroll_origin,0,200).perform()
                time.sleep(1)
            elif x[-1] == 'sendkey':
                text_input = driver.find_element(x[0],x[1])
                action.send_keys_to_element(text_input, x[2]).perform()
                time.sleep(1)
            
    driver.close()

if __name__ == '__main__':
    main()