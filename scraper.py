import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import time
import random


def scrape_real_data():
    print("Запуск undetected-chromedriver (обхід захисту)...")


    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")

    options.add_argument('--blink-settings=imagesEnabled=false')

    driver = uc.Chrome(options=options)
    data = {"Text": [], "Category": [], "Source": []}

    # Словник сайтів з їхніми CSS-класами
    sites = [
        {
            "url": "https://lun.ua/sale/kyiv/flats?room_count=3",
            "cat": "3-room",
            "src": "LUN",
            "card_class": "RealtyCard_root__1GQfg",
            "text_class": "RealtyCard_description__Ee20h RealtyCard_descriptionClamp__9Ry9Z"
        },
        {
            "url": "https://flatfy.ua/uk/%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6-%D0%B1%D1%83%D0%B4%D0%B8%D0%BD%D0%BA%D1%96%D0%B2-%D0%BA%D0%B8%D1%97%D0%B2",
            "cat": "house",
            "src": "Flatfy",
            "card_class": "feed-layout__item-holder",
            "text_class": "realty-preview-description closed"
        },
        {
            "url": "https://dom.ria.com/uk/search/?excludeSold=1&category=4&realty_type=8&operation=1&state_id=10&price_cur=1&wo_dupl=1&sort=inspected_sort&firstIteraction=false&limit=20&market=3&type=list&client=searchV2&ch=226_223,242_239,247_252",
            "cat": "duplex",
            "src": "DOM.RIA",
            "card_class": "realty-photo-rotate is_shadow",
            "text_class": "mt-15 pointer desc-hidden p-rel"
        }
    ]

    for site in sites:
        print(f"\nПідключення до {site['src']}...")
        driver.get(site["url"])

        # Імітація поведінки людини: випадкові затримки та скролінг
        time.sleep(random.uniform(4.0, 7.0))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(random.uniform(2.0, 4.0))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(random.uniform(3.0, 5.0))

        soup = BeautifulSoup(driver.page_source, 'html.parser')


        descriptions = soup.find_all('div', class_=site['text_class'])

        if not descriptions:
            # Альтернативний пошук, якщо перший клас не спрацював
            descriptions = soup.find_all('span', class_=site['text_class'])

        print(f"Знайдено оголошень: {len(descriptions)}")

        for desc in descriptions:
            text = desc.get_text(strip=True)
            if len(text) > 20:
                data["Text"].append(text)
                data["Category"].append(site['cat'])
                data["Source"].append(site['src'])

    driver.quit()

    if len(data["Text"]) > 0:
        df = pd.DataFrame(data)
        df.to_csv("kyiv_real_estate_PRO.csv", index=False, encoding='utf-8')
        print(f"\nУспіх! Зібрано {len(data['Text'])} реальних описів. Файл збережено.")
    else:
        print("\nНе вдалося зібрати дані. Потрібно оновити CSS-класи в коді!")


if __name__ == "__main__":
    scrape_real_data()