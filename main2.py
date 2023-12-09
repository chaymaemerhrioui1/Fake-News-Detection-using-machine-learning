import csv
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import date
from datetime import datetime

class MySpider(scrapy.Spider):
    name = 'myspider'

    start_urls = [
        'https://www.ft.com/fake-news',

        #f'https://www.theonion.com/opinion?startIndex{page}' for page in range(20, 5001, 20)
          # Remplacez ceci par l'URL de votre page
    ]

    def parse(self, response):
        data = []
        # Extracting date
        date1 = response.xpath('.//time/@datetime').get()
        formatted_date = datetime.strptime(date1, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')
        # Extract data from the page using specified HTML elements
        titles = response.xpath('//div[@class="o-teaser__heading"]/text()').get()
        paragraphs =response.xpath('//p/text()').getall()

        # Append extracted data to the list
        for title, paragraph in zip(titles, paragraphs):
            title_text = title.strip()
            paragraph_text = paragraph.strip()

            # Check if the title should be excluded based on specific keywords
            if 'video' in title_text.lower() or 'shows' in title_text.lower() or 'top stories' in title_text.lower() or 'live' in title_text.lower():
                continue  # Skip this title if it contains any of these keywords

            data.append([title_text, paragraph_text, formatted_date])

        # Write data to a CSV file
        with open('hii.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write each row of data to the CSV file
            for row in data:
                # Strip extra spaces and unwanted characters before writing to the CSV
                cleaned_row = [entry.strip() if isinstance(entry, str) else entry for entry in row]
                writer.writerow(cleaned_row)

process = CrawlerProcess(settings={
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
})

process.crawl(MySpider)
process.start()
