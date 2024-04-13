import csv
from bs4 import BeautifulSoup
import requests

def find_news_articles():
    try:
        response = requests.get('http://norumors.net')
        response.raise_for_status()  # Raise an exception for any HTTP errors
        html_text = response.text
        soup = BeautifulSoup(html_text, 'lxml')

        articles = soup.find_all('div', class_='rumor__meta')
        with open('combined_articles.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['المقال', 'التصنيفات', 'صحة الخبر', 'تاريخ النشر']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for index, article in enumerate(articles):
                try:
                    h2_tag = article.find('h2')
                    article_name = h2_tag.text.strip() if h2_tag else None

                    ul_tag = article.find('ul')
                    categories = [li.text.strip() for li in ul_tag.find_all('li')] if ul_tag else []

                    writer.writerow({
                        'المقال': article_name.strip(),
                        'التصنيفات': ', '.join(categories),
                        'صحة الخبر': 'إشاعة',
                        'تاريخ النشر': ''
                    })
                except Exception as e:
                    print(f"Error occurred while scraping article {index+1}: {e}")

        print("Articles from website 1 scraped successfully.")
    except Exception as e:
        print(f"Error occurred while scraping website 1: {e}")

def find_news_articles2():
    try:
        response = requests.get('https://fatabyyano.net/')
        response.raise_for_status()
        html_text = response.text
        soup = BeautifulSoup(html_text, 'lxml')

        articles = soup.find_all('article', class_='w-grid-item')

        with open('combined_articles.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['المقال', 'التصنيفات', 'صحة الخبر', 'تاريخ النشر'])
            for article in articles:
                try:
                    h2_tag = article.find('h2', class_='w-post-elm post_title usg_post_title_1 has_text_color entry-title color_link_inherit')
                    article_name = h2_tag.text.strip() if h2_tag else None

                    taxonomy_div = article.find('div', class_='w-post-elm post_taxonomy usg_post_taxonomy_2 style_badge color_link_inherit')
                    categories = [a_tag.text.strip() for a_tag in taxonomy_div.find_all('a')] if taxonomy_div else []

                    date_tag = article.find('time', class_='w-post-elm post_date usg_post_date_1 has_text_color entry-date published')
                    date_str = date_tag['datetime'] if date_tag else None

                    writer.writerow({
                        'المقال': article_name,
                        'التصنيفات': ', '.join(categories),
                        'صحة الخبر': '',
                        'تاريخ النشر': date_str
                    })
                except Exception as e:
                    print(f"Error occurred while scraping article: {e}")

        print("Articles from website 2 scraped successfully.")
    except Exception as e:
        print(f"Error occurred while scraping website 2: {e}")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def find_news_articles3():
    try:
        # Set up Chrome webdriver with Selenium
        service = Service('C:/Users/pc/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe')  
        driver = webdriver.Chrome(service=service)
        driver.maximize_window()

        # Charger la page du site Web 3
        driver.get('https://verify-sy.com/')

        # Attendre que les éléments d'intérêt soient chargés
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'blog_post_style2_img')))

        # Utiliser BeautifulSoup pour extraire le contenu de la page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        articles = soup.find_all('div', class_='blog_post_style2_img width-f')

        with open('combined_articles.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['المقال', 'التصنيفات', 'صحة الخبر', 'تاريخ النشر'])
            for article in articles:
                try:
                    article_name = article.find('img', class_='img-fluid')['alt'].strip()

                    categories = [a_tag.text.strip() for a_tag in article.find_all('a', class_='blog_meta_tags stat-tags')]

                    date_tag = article.find('span', class_='date-format')
                    date_str = date_tag.get_text(strip=True) if date_tag else None

                    writer.writerow({
                        'المقال': article_name,
                        'التصنيفات': ', '.join(categories),
                        'صحة الخبر': '',
                        'تاريخ النشر': date_str
                    })
                except Exception as e:
                    print(f"Error occurred while scraping article: {e}")

        print("Articles from website 3 scraped successfully.")
    except Exception as e:
        print(f"Error occurred while scraping website 3: {e}")
    finally:
        # Fermer le navigateur après le scraping
        driver.quit()


if __name__ == "__main__":
    find_news_articles()
    find_news_articles2()
    find_news_articles3()
    print("Scraping process completed.")
