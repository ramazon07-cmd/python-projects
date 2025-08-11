import requests
from bs4 import BeautifulSoup
import csv
import json

def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        return None

def parse_products(html):
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    # books.toscrape.com uchun to'g'ri selektorlar:
    for item in soup.select('.product_pod'):
        name_tag = item.select_one('h3 > a')
        price_tag = item.select_one('.price_color')
        rating_tag = item.select_one('p.star-rating')
        name = name_tag['title'].strip() if name_tag and name_tag.has_attr('title') else 'Noma\'lum'
        price = price_tag.text.strip() if price_tag else 'Noma\'lum'
        # Rating klassidan yulduzlar sonini olish
        rating = rating_tag['class'][1] if rating_tag and len(rating_tag['class']) > 1 else 'Noma\'lum'
        products.append({
            'name': name,
            'price': price,
            'rating': rating
        })
    # Bu yerda siz sayt tuzilishiga mos ravishda taglarni o'zgartiring
    for item in soup.select('.product'):  # Misol uchun: '.product'
        name = item.select_one('.product-name')
        price = item.select_one('.product-price')
        rating = item.select_one('.product-rating')
        products.append({
            'name': name.text.strip() if name else 'Noma\'lum',
            'price': price.text.strip() if price else 'Noma\'lum',
            'rating': rating.text.strip() if rating else 'Noma\'lum'
        })
    return products

def save_to_csv(products, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'price', 'rating'])
        writer.writeheader()
        writer.writerows(products)

def save_to_json(products, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

def main():
    url = input("Sayt URLini kiriting: ").strip()
    all_products = []
    page = 1
    while True:
        print(f"{page}-sahifani yuklash...")
        page_url = url.format(page=page)
        html = fetch_page(page_url)
        if not html:
            break
        products = parse_products(html)
        if not products:
            print("Yangi mahsulotlar topilmadi.")
            break
        all_products.extend(products)
        # Sahifalar orasida navigatsiya qilish uchun shart
        next_page = input("Keyingi sahifaga o'tish? (ha/yo'q): ").strip().lower()
        if next_page != 'ha':
            break
        page += 1

    if not all_products:
        print("Hech qanday mahsulot topilmadi.")
        return

    fmt = input("Natijani qaysi formatda saqlashni xohlaysiz? (csv/json): ").strip().lower()
    filename = f"products.{fmt}"
    if fmt == 'csv':
        save_to_csv(all_products, filename)
    else:
        save_to_json(all_products, filename)
    print(f"Natijalar '{filename}' faylida saqlandi.")

if __name__ == "__main__":
    main()