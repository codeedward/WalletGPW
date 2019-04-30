import requests
from bs4 import BeautifulSoup

def getRate(shareName):
    try:
        page = requests.get(f'https://www.bankier.pl/inwestowanie/profile/quote.html?symbol={shareName}')
        soup = BeautifulSoup(page.text, 'html.parser')
        foundField = soup.find('div', attrs={'class': 'profilLast'})
        rateString = foundField.text.strip()
        rateValue = float(rateString[:-3].replace(",", "."))
        return rateValue
    except:
        return 0
