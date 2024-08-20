import requests
from bs4 import BeautifulSoup
import json
import time
import os
from glob import glob

def fetch_page_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraction des informations
    details = {}
    
    # Titre principal
    title_element = soup.find('h1', class_='main-title')
    details['titre_principal'] = title_element.text.strip() if title_element else 'Non disponible'
    
    # Numéro de pourvoi, ECLI, Solution
    ul_elements = soup.find('div', class_='frame-block print-sommaire').find('ul')
    if ul_elements:
        list_items = ul_elements.find_all('li')
        for item in list_items:
            if 'N° de pourvoi' in item.text:
                details['numero_pourvoi'] = item.text.split(':')[-1].strip()
            elif 'ECLI' in item.text:
                details['ecli'] = item.text.split(':')[-1].strip()
            elif 'Solution' in item.text:
                details['solution'] = item.text.split(':')[-1].strip()
    else:
        details['numero_pourvoi'] = 'Non disponible'
        details['ecli'] = 'Non disponible'
        details['solution'] = 'Non disponible'
    
    # Date de l'audience
    titre_lecture = soup.find('div', class_='titreLecture')
    details['date_audience'] = titre_lecture.find('div').text.split('du ')[-1].strip() if titre_lecture else 'Non disponible'
    
    # Décision attaquée
    decision_attaquee = titre_lecture.find('span') if titre_lecture else None
    details['decision_attaquee'] = decision_attaquee.text.split(': ')[-1].strip() if decision_attaquee else 'Non disponible'
    
    # Président
    president_dl = soup.find('dl')
    president_dd = president_dl.find('dd') if president_dl else None
    details['president'] = president_dd.text.strip() if president_dd else 'Non disponible'
    
    # Avocats
    avocats_section = soup.find_all('dt', string='Avocat(s)')
    avocats_list = []
    for avocat in avocats_section:
        dd = avocat.find_next('dd')
        if dd:
            avocats_list.append(dd.text.strip())

    details['avocats'] = ', '.join(avocats_list) if avocats_list else 'Non disponible'

    # Texte intégral
    texte_integral_section = soup.find('div', class_='content-page').find('div', class_='intro').find_next_sibling('div')
    details['texte_integral'] = texte_integral_section.text.strip() if texte_integral_section else 'Non disponible'

    return details

def save_decision_to_file(decision_details, filename):
    try:
        with open(filename, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(decision_details)

    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=2)

def log_failed_page(url, year):
    with open(f'/tmp/failed_pages_{year}.log', 'a') as log_file:
        log_file.write(f"{url}\n")

def scrape_with_retries(url, year, retries=5, initial_delay=10):
    delay = initial_delay
    for attempt in range(retries):
        try:
            return fetch_page_details(url)
        except requests.exceptions.Timeout as e:
            print(f"Timeout on year {year}, URL {url}. Retrying... ({attempt + 1}/{retries})")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error on year {year}, URL {url}. Retrying... ({attempt + 1}/{retries})")
        except requests.exceptions.RequestException as e:
            print(f"Request error on year {year}, URL {url}: {e}. Retrying... ({attempt + 1}/{retries})")
        except Exception as e:
            print(f"An unexpected error occurred on year {year}, URL {url}: {e}")
            log_failed_page(url, year)
            return None
        
        time.sleep(delay)  # Wait before retrying
    
    print(f"Failed to fetch URL {url} after {retries} attempts.")
    log_failed_page(url, year)
    return None

def get_year_from_date(date_str):
    if date_str and date_str != 'Non disponible':
        return date_str.split()[-1]
    return 'Unknown'

def process_decisions_from_file(input_filename):
    with open(input_filename, 'r') as f:
        decisions = json.load(f)
    
    failed_decisions = []

    for decision in decisions:
        try:
            print(f"Fetching details for {decision['title']}")
            details = scrape_with_retries(decision['link'], year="unknown")
            
            if details:
                year = get_year_from_date(details['date_audience'])
                output_filename = f'/tmp/decisions_details_{year}.json'
                save_decision_to_file(details, output_filename)
                print(f"Details for {decision['title']} saved to {output_filename}.")
            else:
                failed_decisions.append(decision)
            
            time.sleep(2)  # Pause pour éviter les limitations de requêtes
        except Exception as e:
            print(f"Failed to fetch details for {decision['title']}: {e}")
            failed_decisions.append(decision)

    # Tentative de rescraper les décisions ayant échoué
    if failed_decisions:
        print(f"Retrying failed decisions: {[d['title'] for d in failed_decisions]}")
        for decision in failed_decisions:
            try:
                print(f"Retrying details for {decision['title']}")
                details = scrape_with_retries(decision['link'], year="unknown")
                
                if details:
                    year = get_year_from_date(details['date_audience'])
                    output_filename = f'/tmp/decisions_details_{year}.json'
                    save_decision_to_file(details, output_filename)
                    print(f"Details for {decision['title']} (retry) saved to {output_filename}.")
                
                time.sleep(2)
            except Exception as e:
                print(f"Failed to retry details for {decision['title']}: {e}")

def retry_failed_pages(year):
    log_file_path = f'/tmp/failed_pages_{year}.log'
    if not os.path.exists(log_file_path):
        print(f"No failed pages log found for year {year}.")
        return
    
    with open(log_file_path, 'r') as log_file:
        failed_urls = log_file.readlines()

    for url in failed_urls:
        url = url.strip()
        if url:
            details = scrape_with_retries(url, year)
            if details:
                output_filename = f'/tmp/decisions_details_{year}.json'
                save_decision_to_file(details, output_filename)
                print(f"Details for URL {url} (retry) saved to {output_filename}.")

def main():
    # Utiliser glob pour sélectionner plusieurs fichiers
    input_filenames = glob('/tmp/decisions_*.json')

    for input_filename in input_filenames:
        print(f"Processing file: {input_filename}")
        process_decisions_from_file(input_filename)

    # Retry any failed pages
    for year in range(1970, 2023 + 1):
        retry_failed_pages(year)

    print('Scraping completed.')

if __name__ == "__main__":
    main()
