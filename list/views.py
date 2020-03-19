from django.shortcuts import render

from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from .models import Search

# Create Some Variables
BASE_CRAIGSLIST_POSTING_URL = "https://{}.craigslist.org/search/?query={}"
BASE_CRAIGSLIST_IMAGE_URL = "https://images.craigslist.org/{}_300x300.jpg"


# Create your views here.


def index(request):
    search_text = request.POST.get('search-text')
    search_country = request.POST.get('search-country')

    while search_text and search_country is not None:
        final_url = BASE_CRAIGSLIST_POSTING_URL.format(search_country, quote_plus(search_text))

        Search.objects.create(
            search_content=search_text, search_url=final_url, search_country=search_country
        )

        response = requests.get(final_url)
        data = response.text

        soup = BeautifulSoup(data, 'html.parser')
        posting_listings = soup.find_all('li', {'class': 'result-row'})

        final_postings = []

        for posting in posting_listings:
            posting_title = posting.find(class_='result-title').text
            posring_url = posting.find('a').get('href')

            if posting.find(class_='result-price'):
                posting_price = posting.find(class_='result-price').text
            else:
                posting_price = 'N/A'

            if posting.find(class_='result-image').get('data-ids'):
                posting_images_ids = posting.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
                posting_images_urls = BASE_CRAIGSLIST_IMAGE_URL.format(posting_images_ids)
            else:
                posting_images_urls = 'https://www.craigslist.org/images/peace.jpg'

            final_postings.append((posting_title, posring_url, posting_price, posting_images_urls))

        frontend_context = {
            'search_text': search_text,
            'final_postings': final_postings
        }

        return render(request, 'list/index.html', frontend_context)

    return render(request, 'list/index.html')
