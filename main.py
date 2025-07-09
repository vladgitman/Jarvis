
import os
import shutil
import requests
import pyautogui as pag
from bs4 import BeautifulSoup
import pyperclip  #Для буферa
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# Инициализация WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# Функция для загрузки файла по ссылке
def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Файл {filename} успешно сохранён.')
    except requests.exceptions.RequestException as e:
        print(f'Произошла ошибка при загрузке файла: {e}')

# Функция для получения URL изображений
def get_image_urls(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.select('button[data-fancybox="gallery"] img')[:11]
        return [img['src'] for img in images if 'src' in img.attrs]  # Проверка наличия атрибута
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при получении страницы: {e}')
        return []
    except Exception as e:
        print(f'Ошибка: {e}')
        return []

# Функция для получения информации о продукте
def get_product_info(url):
    # Установите заголовки
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Выполните GET-запрос
    response = requests.get(url, headers=headers)

    # Проверьте ответ
    if response.ok:
        print("Запрос успешен")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлеките название продукта
        title = soup.find('h1')
        title_text = title.text.strip() if title else "Название отсутствует."  # Обработка NoneType

        # Извлеките цену
        price = soup.find('span', class_='styles_sidebar__main__DaXQC')
        price_text = price.text.strip() if price else 'Цена отсутствует.'  # Обработка NoneType

        # Извлеките описание
        description_div = soup.find('div', class_='styles_description__8_RRa')
        description_text = description_div.text.strip() if description_div else 'Описание отсутствует.'  # Обработка NoneType
        print("Информация скопирована в буфер обмена:\n", title_text, price_text, description_text)
        return title_text, price_text, description_text
    else:
        print(f"Произошла ошибка: {response.status_code}")
        return None, None, None

# Инициализация WebDriver
driver = webdriver.Chrome()  # Убедитесь, что у вас правильно установлен ChromeDriver
try:
    # Переход к странице профиля
    profile_url = "https://999.md/ru/profile/EgorCeban"
    driver.get(profile_url)

    conf = pag.confirm("Продолжить?", "Confirmation")
    if conf == "OK":
        # Получение обновленного URL
        updated_url = driver.current_url  # Получаем текущий URL из браузера

        print(f"Используемый URL: {updated_url}")

        # Получаем данные о продукте
        title_text, price_text, description_text = get_product_info(updated_url)

        if title_text is None or price_text is None or description_text is None:
            print("Не удалось получить информацию о продукте.")

        # Получение изображений
        image_urls = get_image_urls(updated_url)

        if image_urls:
            print(f'Найдено {len(image_urls)} изображений.')
            directory = 'downloaded_images'

            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)
            for i, img_url in enumerate(image_urls):
                # Преобразуем относительный путь к абсолютному URL, если нужно
                if not img_url.startswith('http'):
                    base_url = updated_url.rsplit('/', 1)[0] + "/"
                    img_url = base_url + img_url

                filename = os.path.join(directory, f'image_{i + 1}.jpg')
                download_file(img_url, filename)
        else:
            print('Изображения не найдены.')
        clipboard_text = pyperclip.paste()  # Получаем текст из буфера обмена

    # Получаем текст из буфера обмена для вставки
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Current URL:", driver.current_url)

try:
    # Получаем текст из буфера обмена для вставки
    clipboard_text = pyperclip.paste()  # Получаем текст из буфера обмена
    # Open the login page of the website
    driver.get("https://www.facebook.com")  # Replace with actual login URL if needed

    # Wait for the login input field and enter the username
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='royal-email']"))
    )

    API = "API"
    KEY = "KEY"
    username_input.send_keys(API)

    # Wait for the password input field and enter the password
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='royal-pass']"))
    )

    password_input.send_keys(KEY)
    pag.sleep(5)  # Ждем, чтобы устранить возможные задержки

    # Wait for the "Вход" button and click it
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='login'][data-testid='royal-login-button']"))
    )
    login_button.click()
    conf = pag.confirm("Продолжить?", "Confirmation")
    if conf == "OK":

        print("Продолжить URL")
    # Optionally, wait for the page to load after login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.styles_redirectBtn__o_7FD"))
    )
    
  
    # Wait for the redirect to the 999.md URL
    WebDriverWait(driver, 20).until(EC.url_contains("https://www.facebook.com"))

    # Navigate to the profile page
except Exception as e:
    print(f"An error occurred: {str(e)}")

path = ["wash.png", "/Users/egorceban/PycharmProjects/pythonProject/brave3690/freeze.png", "/Users/egorceban/PycharmProjects/pythonProject/brave3690/oven.png", "micro.png", "dish.png", "coffee.png"] # Картинки
Wash = r"C:\Program Files\JetBrains\PyCharm 2023.3.4\FB.create\wash.png"
Freeze, Oven, Micro, Dish, Coffee = "freeze.png", "oven.png", "micro.png", "dish.png", "coffee.png" # Картинки

# Основная функция
def main():
    while True:
        try:
            conf = pag.confirm("Продолжить?", "Confirmation")

            washing_link = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//a[@itemprop='item' and contains(@href, '/ru/list/household-appliances/washing-machines')]//span[@itemprop='name' and text()='Стиральные и сушильные машины']"
                    ))
                )
            if washing_link:
                print(f"Кнопка найдена")
                # Переход к странице добавления объявления
                url = "https://www.facebook.com/marketplace/create/item"
                driver.get(url)
                button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Дополнительная информация']/ancestor::div[@role='button']"))
                )
                print("Текст кнопки:", button.text)
                button.click()
 
                button.send_keys(Keys.TAB)  # Нажатие клавиши Tab
                pyperclip.copy(description_text)  # Копируем текст цены в буфер обмена
                driver.switch_to.active_element.send_keys(pyperclip.paste())  # Вставляем текст из буфера обмена  button.send_keys(Keys.SHIFT + Keys.TAB)  # Нажатие клавиши Shift + Tab                
                pag.sleep(2)  # Ждем, чтобы устранить возможные задержки
                pag.sleep(2)  # Ждем, чтобы устранить возможные задержки

                for _ in range(2):  # Цикл для двух нажатий клавиши Tab
                    button.send_keys(Keys.SHIFT + Keys.TAB)  # Нажатие клавиши Shift + Tab
                    
                    # Additional logic for elements with specific classes
                    active_element = driver.switch_to.active_element
                    if 'x78zum5' in active_element.get_attribute('class') or 'xh8yej3' in active_element.get_attribute('class'):
                        print("Элемент с классами x78zum5 или xh8yej3 найден.")
                        active_element.click() 

                for _ in range(3):  # Цикл для двух нажатий клавиши Tab
                    active_element.send_keys(Keys.ARROW_DOWN)  # Нажатие клавиши Tab  description_field = button.send_keys(Keys.SHIFT)  # Отпустить клавишу Shift
                # Нажатие клавиши Tab  description_field = button.send_keys(Keys.SHIFT)  # Отпустить клавишу Shift
                driver.switch_to.active_element.send_keys(Keys.ENTER)  # Нажатие клавиши Space
                for _ in range(1):  # Цикл для двух нажатий клавиши Tab
                     active_element.send_keys(Keys.SHIFT + Keys.TAB)  # Нажатие клавиши Shift + Tab
                     driver.switch_to.active_element  # Получаем активный элемент
                     driver.switch_to.active_element.click()
                for _ in range(4):  # Цикл для нажатий клавиши Tab
                    driver.switch_to.active_element.send_keys(Keys.TAB)  # Нажатие клавиши Tab  description_field = button.send_keys(Keys.SHIFT)  # Отпустить клавишу Shift

                driver.switch_to.active_element.send_keys(Keys.ENTER)  # Нажатие клавиши Tab  description_field = button.send_keys(Keys.SHIFT)  # Отпустить клавишу Shift
                driver.switch_to.active_element.send_keys(Keys.SHIFT + Keys.TAB)  # Нажатие клавиши Shift + Tab
                driver.switch_to.active_element  # Получаем активный элемент
                print("Активный элемент:", driver.switch_to.active_element.text, driver.switch_to.active_element.get_attribute('aria-pressed'), driver.switch_to.active_element.get_attribute('class'))
                driver.switch_to.active_element.click()

                pyperclip.copy(price_text)  # Копируем текст цены в буфер обмена
                driver.switch_to.active_element.send_keys(pyperclip.paste())  # Вставляем текст из буфера обмена  button.send_keys(Keys.SHIFT + Keys.TAB)  # Нажатие клавиши Shift + Tab
                driver.switch_to.active_element.send_keys(Keys.SHIFT + Keys.TAB)  # Нажатие клавиши Shift + Tab
                driver.switch_to.active_element  # Получаем активный элемент
                print("Активный элемент:", driver.switch_to.active_element.text, driver.switch_to.active_element.get_attribute('aria-pressed'), driver.switch_to.active_element.get_attribute('class'))

                pyperclip.copy(title_text)  # Копируем текст в буфер обмена
                driver.switch_to.active_element.send_keys(pyperclip.paste())  # Вставляем текст из буфера обмена  button.send_keys(Keys.SHIFT + Keys.TAB)  # Нажатие клавиши Shift + Tab

                for _ in range(3):  # Цикл для двух нажатий клавиши Tab
                    driver.switch_to.active_element.send_keys(Keys.SHIFT + Keys.TAB)  # Нажатие клавиши Shift + Tab
                photo = driver.switch_to.active_element  # Получаем активный элемент
                photo = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'x1i10hfl x1qjc9v5 xjbqb8w xjqpnuy xc5r6h4 xqeqjp1 x1phubyo x13fuv20 x18b5jzi x1q0q8m5 x1t7ytsu x972fbf x10w94by x1qhh985 x14e42zd x9f619 x1ypdohk xdl72j9 x2lah0s xe8uvvx xdj266r x14z9mp xat24cr x1lziwak x2lwn1j xeuugli xexx8yu xyri2b x18d9i69 x1c1uobl x1n2onr6 x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1fmog5m xu25z0z x140muxe xo1y3bh x1q0g3np x87ps6o x1lku1pv x78zum5 x1iyjqo2 x18bame2 x1a2a7pz xvetz19')]")
                    )
                )
                photo.click()


                print("Активный элемент:", driver.switch_to.active_element.text, driver.switch_to.active_element.get_attribute('aria-pressed'), driver.switch_to.active_element.get_attribute('class'))
                driver.switch_to.active_element.click()
                driver.execute_script("window.alert('This is a mock alert');")
                pag.sleep(2)  # Ждем, чтобы alert стал видимым
                alert = driver.switch_to.alert  # Переключаемся на alert
                print(f"Alert text: {alert.text}")  # Выводим текст alert
                pag.sleep(10)  # Ждем, чтобы устранить возможные задержки

                # Закрываем alert, нажав "ОК" или отменяем, если не нажато "ОК"
                if alert.text == "This is a mock alert":
                    alert.accept()  # Закрываем alert, нажав "ОК"
                else:
                    print("Alert not accepted. Exiting.")
                    driver.quit()  # Закрываем браузер
                    return  

                # Загрузка изображений
                 # Нажатие на кнопку "Далее" с проверкой кликабельностиAdd commentMore actions
                next_button = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'x1lliihq') and text()='Далее']/ancestor::div[@role='none']"))
                )
                next_button.click()
                print("Кнопка 'Далее' нажата.")
                for x in range(69):                    
                    driver.switch_to.active_element.send_keys(Keys.TAB)  # Нажатие клавиши Tab
                    driver.switch_to.active_element.send_keys(Keys.ENTER)  # Нажатие клав

                pag.sleep(30)  # Ждем, чтобы устранить возможные задержки
                driver.switch_to.active_element
                print("Активный элемент:", driver.switch_to.active_element.text, driver.switch_to.active_element.get_attribute('aria-pressed'), driver.switch_to.active_element.get_attribute('class'))
                driver.switch_to.active_element.click()
                pag.sleep(2)  # Ждем, чтобы устранить возможные задержки


                for _ in range(2):  # Цикл для двух нажатий клавиши Tab
                    driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN)  # Нажатие клавиши Tab  description_field = button.send_keys(Keys.SHIFT)  # Отпустить клавишу Shift
                driver.switch_to.active_element.send_keys(Keys.ENTER)  # Нажатие клавиши Space
                pag.sleep(2)  # Ждем, чтобы устранить возможные задержки

                driver.switch_to.active_element.send_keys(Keys.TAB)  # Нажатие клавиши Tab

                for x in range(69):                    
                    driver.switch_to.active_element.send_keys(Keys.TAB)  # Нажатие клавиши Tab
                    driver.switch_to.active_element.send_keys(Keys.ENTER)  # Нажатие клав


                send_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Отправить' and contains(@class, 'x1i10hfl xjbqb8w x1ejq31n x18oe1m7 x1sy0etr xstzfhl x972fbf x10w94by x1qhh985 x14e42zd x1ypdohk xe8uvvx xdj266r x14z9mp xat24cr x1lziwak xexx8yu xyri2b x18d9i69 x1c1uobl x16tdsg8 x1hl2dhg xggy1nq x1fmog5m xu25z0z x140muxe xo1y3bh x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3')]")
                    )
                )
                send_button.click()

            else:
                print(f"Кнопка найдена?")
                return True

        except Exception:
            error = pag.confirm("Произошла ошибка. Продолжить?", "Error")
            if error == "OK":
                print("Продолжение работы программы.")
                pass
            else:
                print("Программа завершена.")
                driver.quit()                


if __name__ == "__main__":
    main()
