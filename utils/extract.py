# utils/extract.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://fashion-studio.dicoding.dev/page{}"

def extract_product_data():
    all_data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(1, 51):
        try:
            print(f"Scraping page {page}...")
            if page == 1:
                url = "https://fashion-studio.dicoding.dev/"
            else:
                url = BASE_URL.format(page)
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            products = soup.find_all("div", class_="collection-card")

            for product in products:
                try:
                    title = product.find("h3", class_="product-title").get_text(strip=True)

                    # Price: cek jika "Price Unavailable"
                    price_tag = product.find("span", class_="price") or product.find("p", class_="price")
                    if price_tag:
                        price_text = price_tag.get_text(strip=True)
                        price = None if "unavailable" in price_text.lower() or "Price Unavailable" in price_text else price_text.replace("$", "")
                    else:
                        price = None

                    # Rating
                    rating_p = product.find_all("p")
                    rating = None
                    for p in rating_p:
                        if "Rating" in p.text:
                            rating_text = p.text.strip().replace("Rating:", "").strip()
                            if "Not Rated" in rating_text or "Invalid" in rating_text:
                                rating = None
                            else:
                                rating = float(rating_text.split("⭐")[1].split("/")[0].strip())
                            break

                    # Colors
                    colors = None
                    for p in rating_p:
                        if "Colors" in p.text:
                            colors = p.text.strip().split(" ")[0]  # Ambil angka, misal "3 Colors"
                            break

                    # Size
                    size = None
                    for p in rating_p:
                        if "Size:" in p.text:
                            size = p.text.strip().split("Size:")[1].strip()
                            break

                    # Gender
                    gender = None
                    for p in rating_p:
                        if "Gender:" in p.text:
                            gender = p.text.strip().split("Gender:")[1].strip()
                            break
                    
                    # Timestamp
                    timestamp = datetime.now().isoformat()

                    all_data.append({
                        "Title": title,
                        "Price": price,
                        "Rating": rating,
                        "Colors": colors,
                        "Size": size,
                        "Gender": gender,
                        "Timestamp": timestamp
                    })
                except Exception as e:
                    print(f"❌ Error extracting product on page {page}: {e}")
        except Exception as e:
            print(f"❌ Failed to retrieve page {page}: {e}")

    return all_data
