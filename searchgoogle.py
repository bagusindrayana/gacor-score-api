from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.common.keys import Keys
import json,time


provinsiLinks = []
with open("prov.txt", "r") as f:
    for line in f:
        provinsiLinks.append(line.strip())

 # Inisialisasi driver Chrome
driver = webdriver.Chrome(ChromeDriverManager().install())


def search_google(search_query):
    # Buka halaman pencarian Google
    driver.get("https://www.google.com/search?num=100&q="+search_query)

    # # Cari elemen textarea
    # search_box = driver.find_element(By.NAME, "q")
    # # Ketik query
    # search_box.send_keys(search_query)

    # # Tekan Enter
    # search_box.send_keys(Keys.RETURN)

    # # detect captcha and wait user solve
    check_captcha = driver.find_elements(By.ID, "captcha-form")
    if check_captcha:
        print("Captcha detected, please solve it manually")
        time.sleep(30)
        return search_google(search_query)
    search_results = []

    revealed = driver.find_element(By.ID, "center_col")
    wait = WebDriverWait(driver, timeout=2)
    wait.until(lambda d : revealed.is_displayed())
    results = driver.find_elements(By.XPATH, '//div[contains(concat(" ", normalize-space(@class), " "), " g ")]')
    for result in results:
        title = result.find_element(By.TAG_NAME, "h3").text
        link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
        text = result.find_element(By.TAG_NAME, "span").text
        search_results.append({"title": title, "link": link, "text": text})

    finished = False
    prev_len = len(search_results)
    while finished == False:
        # find span that contains Hasil lainnya
        try:
            next_page = driver.find_element(By.XPATH, '//span[text()="Hasil lainnya"]')
            if next_page is None:
                finished = True
        except:
            finished = True
        if len(search_results) > 100:
            finished = True
        # next_page.click()
        # scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        check_captcha = driver.find_elements(By.ID, "captcha-form")
        if check_captcha:
            print("Captcha detected, please solve it manually")
            time.sleep(30)
        results = driver.find_elements(By.XPATH, '//div[contains(concat(" ", normalize-space(@class), " "), " g ")]')
        for result in results:
            title = result.find_element(By.TAG_NAME, "h3").text
            link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
            search_results.append({"title": title, "link": link})
       
        if prev_len == len(search_results):
            finished = True
        else:
            prev_len = len(search_results)
    time.sleep(3)
    return search_results


resultsData = []
for prov in provinsiLinks:
    print("SCAN : "+prov)
    searchResult = search_google('site:'+prov+' "slot online" OR '+prov+' "gacor"')
    with open("./result-scan-gacor-3/"+prov+".json", "w") as f:
        json.dump(searchResult, f)
        


driver.quit()
