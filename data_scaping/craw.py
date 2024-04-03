from bs4 import BeautifulSoup
from cloudscraper import CloudScraper
import pandas as pd
from urllib.parse import urljoin

visited_urls = set()
custom_headers = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
    'Referer': 'https://www.google.com/'
}
def get_product_info(url):
    session = CloudScraper()
    try:
        response = session.get(url, headers=custom_headers)
        if response.status_code != 200:
            print(f"Error {response.status_code}")
            return None
        soup = BeautifulSoup(response.text, 'lxml')
        #title
        title_el = soup.select_one('#productTitle')
        title = title_el.text.strip() if title_el else None
        #rating
        rating_element = soup.select_one("#acrPopover")
        rating_text = rating_element.attrs.get("title") if rating_element else None
        rating = rating_text.replace("out of 5 stars", "") if rating_text else None
        #image
        img_el = soup.select_one('#landingImage')
        img = img_el.attrs.get('src') if img_el else None
        #price
        price_el = soup.select_one('span.a-offscreen')
        price = price_el.text if price_el else None
        #color
        color = soup.find('span', class_ = 'selection').text.strip() if soup.find('span', class_ = 'selection') else None
        #product detail
        table = soup.find('table', id='productDetails_detailBullets_sections1')
        product_details = {}
        for row in table.find_all('tr')[1:]:
            detail_name = row.find('th').text.strip()
            detail_value = row.find('td').text.strip()
            product_details[detail_name] = detail_value

        descrip_el = soup.select_one('#productDescription')
        descrip = descrip_el.text.strip() if descrip_el else None
        
        return {
            "title": title,
            "rating": rating,
            "image": img,
            "price": price,
            "color": color,
            "product_details": product_details,
            "description": descrip
        }
    except Exception as e:
        print(f'Error getting product info {e}')
        return None
def parse_listing(listing_url):
    global visited_urls
    session = CloudScraper()
    try:
        response = session.get(listing_url, headers=custom_headers)
        print(response.status_code)
        soup_search = BeautifulSoup(response.text, "lxml")
        link_elements = soup_search.select("[data-asin] h2 a")
        page_data = []

        for link in link_elements:
            full_url = urljoin(listing_url, link.attrs.get("href"))
            if full_url not in visited_urls:
                visited_urls.add(full_url)
                print(f"Scraping product from {full_url[:100]}", flush=True)
                product_info = get_product_info(full_url)
                if product_info:
                    page_data.append(product_info)

        next_page_el = soup_search.select_one('a.s-pagination-next')
        if next_page_el:
            next_page_url = next_page_el.attrs.get('href')
            next_page_url = urljoin(listing_url, next_page_url)
            print(f'Scraping next page: {next_page_url}', flush=True)
            page_data += parse_listing(next_page_url)

        return page_data
    except Exception as e:
        print(f'erro: {e}')
        return None
#run test
"""     
url = 'https://www.amazon.com/SAMSUNG-Unlocked-Smartphone-Advanced-Expandable/dp/B0CN1Q2X3B/ref=sr_1_1_sspa?crid=2UBB2O2ZQ1XWD&dib=eyJ2IjoiMSJ9.appjRMx7PTlrQkQz90VUuzZrUWtC4WuucY-Eq8EOmL6ZzrMWtAmpi8j9MOcPqEwhU35kkDgiBIYKGMhaVGWgvm7BU3wMvCiBQtLdQryklzogtizMsPf5t6g0Fd4Zw8wKghk_pErZ0tcLN4TrT5v_EE83O4RPDemtzXwYxw67p_NfXLiiLciGNzBtY3byBduT9PH6SYiwQjtdBxNS4iqEKhyRmv08R_CpxPbPwxPOr4E.vgJnkKl-pHq1CovSWNXUynU94LkRGSb703bwYoeW48w&dib_tag=se&keywords=phone&qid=1712134246&sprefix=%2Caps%2C278&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1'
get_product_info(url)
 """
 
if __name__ == '__main__':
    data = []
    search_url = 'https://www.amazon.com/s?k=phone&crid=2UBB2O2ZQ1XWD&sprefix=%2Caps%2C278&ref=nb_sb_ss_recent_2_0_recent'
    data = parse_listing(search_url)
    df = pd.DataFrame(data)
    df.to_json('phone.json', orient='records')
    