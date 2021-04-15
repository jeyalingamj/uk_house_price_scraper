import requests
from bs4 import BeautifulSoup
import csv
import time

class ZooplaScraper:
    results = []
    def fetch(self, url):
        print('HTTP GET request to URL: %s' % url, end='')
        res = requests.get(url)
        print(' | Status code: %s' % res.status_code)

        return res

    def parse(self, html):
        content = BeautifulSoup(html, 'lxml')

        #titles = [title.text for title in content.find_all(attrs={'class':'css-qwtjnc-Heading2-StyledAddress e2uk8e14'})]
        #print(titles)
        page = content.find('body')
        dates = page.find_all('span',{'class':"css-1xux213-Text eczcs4p0"})
        cards = content.findAll('div', {'class': 'css-wfndrn-StyledContent e2uk8e18'})
        for card in cards:
            for date in dates:
                list_date = date.text
            date = page.text
            self.results.append({
                "title" : card.find(attrs={'class':'css-qwtjnc-Heading2-StyledAddress e2uk8e14'}).text,
                "address" : card.find('p', attrs={'class':'css-3hse11-Text eczcs4p0'}).text,
                "price" : card.find('p', attrs={'class':'css-6v9gpl-Text eczcs4p0'}).text.replace('\u00a3',''),
                "listdate": list_date.replace('Listed on ','')
            })

    def to_csv(self):
        with open('zoopla.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

            print('Stored results to "zoopla.csv"')

    def run(self):

        for page in range(1, 5):
            #url = 'https://www.zoopla.co.uk/for-sale/property/london/rotherhithe-new-road/bermondsey-trading-estate/se16-3ll/?q=se16%203ll&results_sort=newest_listings&search_source=for-sale'
            #url = 'https://www.zoopla.co.uk/for-sale/property/london/bromley/?page_size=25&q=Bromley%2C%20London&radius=0.25&results_sort=newest_listings'
            #Bromely
            #url = 'https://www.zoopla.co.uk/for-sale/property/london/bromley/?page_size=25&q=Bromley%2C%20London&radius=0.25&results_sort=newest_listings&pn='
            #Dartford
            url = 'https://www.zoopla.co.uk/for-sale/property/dartford/?page_size=25&q=Dartford%2C%20Kent&radius=0.25&results_sort=newest_listings&pn='
            url += str(page)
            #print(url)
            res = self.fetch(url)
            self.parse(res.text)
            time.sleep(2)

        self.to_csv()


if __name__ == '__main__':
    scraper = ZooplaScraper()
    scraper.run()