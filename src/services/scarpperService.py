import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import chromedriver_autoinstaller

def parse_reviews_from_html(soup):
    """Fonction helper pour extraire les avis d'un objet BeautifulSoup."""
    reviews_on_page = []
    review_items = soup.find_all('li', class_='c-customer-reviews__item')

    for review in review_items:
        try:
            title = review.find('h3').get_text(strip=True) if review.find('h3') else "Sans titre"
            content = review.find('div', class_='o-text').find('p').get_text(strip=True) if review.find('div', class_='o-text') and review.find('div', class_='o-text').find('p') else ""
            
            rating_score = 0
            rating_element = review.find('span', class_='c-stars-result')
            if rating_element and 'data-score' in rating_element.attrs:
                rating_score = int(rating_element['data-score']) / 20

            author = review.find('span', class_='c-customer-review__author').get_text(strip=True).replace('•', '').strip() if review.find('span', class_='c-customer-review__author') else "Anonyme"
            date = review.find('span', class_='ratingPublishDetails').get_text(strip=True) if review.find('span', class_='ratingPublishDetails') else "Date inconnue"
            
            reviews_on_page.append({
                "title": title, "author": author, "rating": rating_score,
                "date": date, "content": content
            })
        except Exception as e:
            print(f"Erreur lors de l'extraction d'un avis : {e}")
            continue
    return reviews_on_page

def scrape_cdiscount_reviews_paginated(url: str):
    """Scrape tous les avis d'une page produit Cdiscount en gérant la pagination."""
    print("Démarrage du scraper avec pagination...")
    options = webdriver.ChromeOptions()

    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    print(f"Page chargée : {url}")

    try:
        wait.until(EC.element_to_be_clickable((By.ID, 'footer_tc_privacy_button_2'))).click()
        print("Cookies acceptés.")
    except TimeoutException:
        print("Pas de pop-up de cookies ou impossible de la fermer.")
        
    all_reviews = []
    page_number = 1

    while True:
        print(f"Extraction des avis de la page {page_number}...")
        
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.c-customer-reviews__item')))
        except TimeoutException:
            print("Timeout en attendant les avis sur la page. Arrêt.")
            break
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        reviews_from_this_page = parse_reviews_from_html(soup)
        
        if not reviews_from_this_page and page_number > 1:
            print("Aucun nouvel avis trouvé sur cette page, probablement la fin.")
            break
        
        new_reviews = [rev for rev in reviews_from_this_page if rev not in all_reviews]
        if not new_reviews and page_number > 1:
            print("Aucun NOUVEL avis trouvé. La pagination semble boucler. Arrêt.")
            break
            
        all_reviews.extend(new_reviews)
        # print(f"{len(new_reviews)} avis extraits. Total : {len(all_reviews)}")

        try:
            next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.js-update-accordion-click[value='Suivant']")))
            driver.execute_script("arguments[0].click();", next_button)
            print("Passage à la page suivante...")
            page_number += 1
            time.sleep(2) 
            
        except TimeoutException:
            print("Fin de la pagination, plus de bouton 'Suivant' trouvable.")
            break

    driver.quit()
    return all_reviews


def scrape_cultura_reviews(url: str) -> list[dict]:
    """
    Scrape tous les avis d'un produit Cultura depuis son URL.

    Retourne une liste de dictionnaires, où chaque dictionnaire
    représente un avis au format spécifié.
    """
    print("Démarrage du scraper pour les avis Cultura...")
    chromedriver_autoinstaller.install()
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    reviews_list = []

    try:
        driver.get(url)
        print(f"Page chargée : {url}")
        
        # 1. Gérer le bandeau des cookies
        try:
            accept_button_selector = (By.ID, 'onetrust-accept-btn-handler')
            cookie_button = wait.until(EC.element_to_be_clickable(accept_button_selector))
            cookie_button.click()
            print("Cookies acceptés.")
            time.sleep(1)
        except TimeoutException:
            print("Pas de pop-up de cookies ou déjà accepté.")

        # 2. Scroller et cliquer sur "Lire les X avis" pour tout afficher
        try:
            # On localise la section des avis pour s'assurer qu'elle est dans la vue
            reviews_section = wait.until(EC.presence_of_element_located((By.ID, 'reviews')))
            ActionChains(driver).move_to_element(reviews_section).perform()
            time.sleep(1)

            # On clique sur le bouton pour afficher la liste complète
            read_all_button_selector = (By.CSS_SELECTOR, 'button.c-reviews__see-all')
            read_all_button = wait.until(EC.element_to_be_clickable(read_all_button_selector))
            read_all_button.click()
            print("Clic sur 'Lire les avis' pour tout afficher.")
            # On attend que les avis soient bien chargés
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'c-review')))
            time.sleep(2)
        except TimeoutException:
            print("Aucun avis trouvé ou le bouton 'Lire les avis' n'a pas été trouvé.")
            return []

        # 3. Parser la page avec BeautifulSoup et extraire chaque avis
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        review_elements = soup.find_all('div', class_='c-review')
        print(f"{len(review_elements)} avis trouvés. Extraction en cours...")

        for review in review_elements:
            try:
                # Titre
                title = review.find('h3', class_='c-review__title').get_text(strip=True)

                # Contenu
                content = review.find('p', class_='c-review__text').get_text(strip=True)

                # Auteur et Date
                author_date_raw = review.find('span', class_='c-review__author').get_text(strip=True)
                # On nettoie et sépare la chaîne "Par [Auteur] le [Date]"
                author_date_parts = author_date_raw.replace('Par ', '').split(' le ')
                author = author_date_parts[0].strip()
                date = author_date_parts[1].strip()

                # Note (rating)
                rating_raw = review.find('div', {'aria-label': True})['aria-label']
                # On extrait le chiffre de "Note de X sur 5"
                rating_match = re.search(r'(\d)', rating_raw)
                rating = float(rating_match.group(1)) if rating_match else 0.0

                reviews_list.append({
                    "author": author,
                    "content": content,
                    "date": date,
                    "rating": rating,
                    "title": title
                })
            except Exception as e:
                # Si un avis a une structure anormale, on l'ignore et on continue
                print(f"Avis ignoré dû à une erreur de parsing: {e}")
                continue
        
        return reviews_list

    except Exception as e:
        print(f"Erreur majeure lors du scraping : {e}")
        with open("cultura_error_page.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return []
    finally:
        driver.quit()
        print("Scraper terminé.")