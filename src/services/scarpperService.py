import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

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
    # options.add_argument("--headless") # Désactivez le mode headless pour le débogage si nécessaire
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    driver.get(url)
    print(f"Page chargée : {url}")

    # --- Étape 1 : Gérer les cookies ---
    try:
        wait.until(EC.element_to_be_clickable((By.ID, 'footer_tc_privacy_button_2'))).click()
        print("Cookies acceptés.")
    except TimeoutException:
        print("Pas de pop-up de cookies ou impossible de la fermer.")
        
    all_reviews = []
    page_number = 1

    # --- Étape 2 : Boucler sur les pages d'avis ---
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
        
        # On va s'assurer de ne pas ajouter de doublons
        new_reviews = [rev for rev in reviews_from_this_page if rev not in all_reviews]
        if not new_reviews and page_number > 1:
            print("Aucun NOUVEL avis trouvé. La pagination semble boucler. Arrêt.")
            break
            
        all_reviews.extend(new_reviews)
        print(f"{len(new_reviews)} avis extraits. Total : {len(all_reviews)}")

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

# if __name__ == '__main__':
#     product_url = 'https://www.cdiscount.com/informatique/clavier-souris-webcam/souris-gamer-filaire-logitech-g-g203-light/f-1070214-log5099206089167.html'
    
#     final_reviews = scrape_cdiscount_reviews_paginated(product_url)
    
#     print(f"\n--- EXTRACTION TERMINÉE : {len(final_reviews)} avis au total ---")
    
#     # --- DÉBUT DES LIGNES AJOUTÉES ---
#     # Sauvegarder la liste dans un fichier JSON
#     with open('reviews.json', 'w', encoding='utf-8') as f:
#         json.dump(final_reviews, f, ensure_ascii=False, indent=4)

#     print("\n✅ Résultat sauvegardé avec succès dans le fichier 'reviews.json'")
#     # --- FIN DES LIGNES AJOUTÉES ---