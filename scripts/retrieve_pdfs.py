import argparse
import csv
import urllib.request

# Installation of selenium and the crome web driver is required, assuming
# chrome browser is installed on the machine.
# https://chromedriver.chromium.org/downloads
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

import os
import time
import shutil

papers = [
    ('journals/pacmpl/GhoshHMM20', 'https://doi.org/10.1145/3428300'),
    ('journals/pacmpl/MajumdarYZ20', 'https://doi.org/10.1145/3428202')
]

def read_csv(file_path):
    papers = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if len(row) == 6:
                paper = (row[4], row[5])
                papers.append(paper)
    return papers

PAPER_DIRECTORY = 'papers'

opener = urllib.request.build_opener()
opener.addheaders = [
    ('Accept', 'application/vnd.crossref.unixsd+xml'),
    ('User-Agent', 'PostmanRuntime/7.6.0')
]

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('prefs', {
        "plugins.plugins_disabled": ["Chrome PDF Viewer"],
        "download.default_directory": f'{os.getcwd()}/{PAPER_DIRECTORY}/new_downloads',
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    }
)

print('Starting browser...')
browser = webdriver.Chrome(options=chrome_options)

print('Starting loop...')

parser = argparse.ArgumentParser(description='Read data from a CSV file and generate a data structure.')
parser.add_argument('csv_file', help='Path to the CSV file')

args = parser.parse_args()
csv_file_path = args.csv_file

papers = read_csv(csv_file_path)

while len(papers) > 0:
    current_paper = papers.pop(0)
    file_title = current_paper[0].replace('/', '@')

    if not os.path.exists(f'{PAPER_DIRECTORY}/{file_title}.pdf'):
        print('='*80)
        print(f'Looking up {current_paper[0]}')
        try:
            if 'doi.org/' in current_paper[1]:
                print(f'Retrieving full text from doi: {current_paper[1]}')
                r = opener.open(current_paper[1])
                link = r.headers['Link'].split(', ')[1].split('; ')[0][1:-1]
                if 'ieeexplore' in link and '-aam.pdf' in link:
                    print('Linkie:', link)
                    ieee_id = link.split('-aam.pdf')[0][-7:]
                    print(ieee_id)
                    link = f'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={ieee_id}'
                elif 'xplorestaging' in link:
                    ieee_id = link.split('=')[-1]
                    link = f'https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={ieee_id}'
                elif 'elsevier' in link:
                    pii = link.split('PII:')[-1][:17]
                    link = f'https://www.sciencedirect.com/science/article/pii/{pii}/pdf'
            else:
                link = current_paper[1]
            print(f'Going to download from link: {link}')

            # browser.implicitly_wait(5)
            response = browser.get(link)

            print(f'Awaiting download')

            while True:
                # Wait a bit
                time.sleep(0.5)

                if not os.path.isdir(f'{PAPER_DIRECTORY}/new_downloads'):
                    raise FileNotFoundError(f'No PDF could be downloaded for {current_paper[0]}')

                downloaded_files = os.listdir(f'{PAPER_DIRECTORY}/new_downloads')

                # Check if a downloaded file exists
                if len(downloaded_files) == 1:
                    extension = downloaded_files[0].split('.')[-1].lower()

                    # If there is still a download in progress, keep waiting.
                    if extension == 'crdownload':
                        continue
                    # If the PDF is downloaded, move it to folder using db name.
                    elif extension == 'pdf':
                        os.rename(f'{PAPER_DIRECTORY}/new_downloads/{downloaded_files[0]}', f'{PAPER_DIRECTORY}/{file_title}.pdf')
                        print(f'Download success!')
                        break
                    else:
                        raise Exception(f'Invalid file type for {current_paper[0]}')
                elif len(downloaded_files) == 0:
                    raise FileNotFoundError(f'No PDF could be downloaded for {current_paper[0]}')
                else:
                    raise Exception(f'Too many files for {current_paper[0]}')


        except Exception as e:
            print(f'Something went wrong for {current_paper[0]}: {e}')
            papers.append(current_paper)

        if os.path.isdir(f'{os.getcwd()}/{PAPER_DIRECTORY}/new_downloads'):
            shutil.rmtree(f'{os.getcwd()}/{PAPER_DIRECTORY}/new_downloads')
