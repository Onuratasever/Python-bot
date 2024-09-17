from selenium import webdriver
from selenium.webdriver.chrome.service import Service #This is for the service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import pygame
# import requests
import time

ALARM_SOUND = 'a.mp3'

# Pygame'i başlat
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(ALARM_SOUND)


obs_link = "https://obs.gtu.edu.tr/oibs/std/login.aspx"

username = "############"
password = "####"

def init_driver(obs_link: str) -> webdriver.Chrome:
    service = Service(executable_path="chromedriver.exe") 
    driver = webdriver.Chrome(service=service)

    # make full screen
    driver.maximize_window()

    driver.get(obs_link)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "txtParamT01")))
    
    return driver

def login(driver: webdriver.Chrome, username: str, password: str):
    input_element = driver.find_element(By.ID, "txtParamT01")
    input_element.clear() # This is
    input_element.send_keys(username + Keys.ENTER) 

    input_element = driver.find_element(By.ID, "txtParamT02")
    input_element.clear() # This is
    input_element.send_keys(password)

    driver.find_element(By.ID, "txtSecCode").click()

    time.sleep(5)

    input_element = driver.find_element(By.ID, "btnLogin")
    input_element.click()

def navigate_to_secmeli_secme(driver: webdriver.Chrome):
    driver.switch_to.default_content()
    ders_ve_donem = driver.find_element(By.PARTIAL_LINK_TEXT, "Ders ve Dönem İşlemleri")
    ders_ve_donem.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Ders Kayıt"))
    )

    ders_kayit = driver.find_element(By.PARTIAL_LINK_TEXT, "Ders Kayıt")
    ders_kayit.click()

    time.sleep(3)

    tamam_buton = driver.find_element(By.CLASS_NAME, "swal2-close")
    tamam_buton.click()
    # input_element.send_keys(Keys.ENTER)

    time.sleep(3)

    # WebDriverWait(driver, 15).until(
    #     EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "3. Sınıf"))
    # )

    driver.switch_to.frame("IFRAME1")

    frame_button = driver.find_element(By.ID, "grdMufDers_btnDK_3")
    frame_button.click()

    driver.switch_to.default_content()

    # WebDriverWait(driver, 5).until(
    #     EC.presence_of_element_located((By.CLASS_NAME, "swal2-close"))
    # )

    time.sleep(3)

    close_button = driver.find_element(By.CLASS_NAME, "swal2-close")
    close_button.click()

    time.sleep(3)

    driver.switch_to.frame("IFRAME1")

    driver.switch_to.frame("bailwal_overlay_frame")

    tüm_dersler = driver.find_element(By.ID, "btnShowAll")
    tüm_dersler.click()

    time.sleep(1)

    kontenjan_buton = driver.find_element(By.ID, "btnKontenjanGoster")
    kontenjan_buton.click()

    time.sleep(2)

def check_kontenjan(driver: webdriver.Chrome):
    print("\n")
    while True:
        driver.switch_to.default_content()
        hid_timer = int(driver.find_element(By.ID, "hidTimer").get_attribute("value"))

        print(f"\033[2Ahid_timer: {hid_timer:4d}")
        if(hid_timer < 200):
            driver.refresh()
            navigate_to_secmeli_secme(driver)
            driver.switch_to.default_content()

        driver.switch_to.frame("IFRAME1")
        driver.switch_to.frame("bailwal_overlay_frame")

        print("HELLLLOOOOO")
        # driver.switch_to.default_content()
        # kontenjan_buton.click()
        # Kontejan gostere tikla
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "btnKontenjanGoster"))
            )
            kontenjan_buton = driver.find_element(By.ID, "btnKontenjanGoster")
            kontenjan_buton.click()
        except (StaleElementReferenceException, NoSuchElementException) as e:
            print(f"Element btnKontenjanGoster bulunamadı veya geçersiz: {e}")
        
        # Kontenjani kontrol et
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "grdDersler_lblKONad_0"))
            )
            span1 = driver.find_element(By.ID, "grdDersler_lblKONad_0")
            span1_text = span1.text
            parts = span1_text.split('/')
            number_before_slash = int(parts[0])
            if number_before_slash < 35:
                print("Kontenjan Açıldı")
                pygame.mixer.music.play()
                # break
        except (StaleElementReferenceException, NoSuchElementException) as e:
            print(f"Element grdDersler_lblKONad_0 bulunamadı veya geçersiz: {e}")
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "grdDersler_lblKONad_4"))
            )
            span2 = driver.find_element(By.ID, "grdDersler_lblKONad_4")
            span2_text = span2.text
            parts = span2_text.split('/')
            number_before_slash = int(parts[0])
            if number_before_slash < 35:
                print("Kontenjan Açıldı")
                pygame.mixer.music.play()
                break
        except (StaleElementReferenceException, NoSuchElementException) as e:
            print(f"Element grdDersler_lblKONad_4 bulunamadı veya geçersiz: {e}")
        time.sleep(5)


driver = init_driver(obs_link=obs_link)
login(driver=driver, username=username, password=password)
navigate_to_secmeli_secme(driver=driver)
check_kontenjan(driver=driver)

time.sleep(3)


pygame.quit()
driver.quit()
