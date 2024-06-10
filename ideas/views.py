import requests
from django.shortcuts import render
from django.core.paginator import Paginator
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

API_URL = 'https://suitmedia-backend.suitdev.com/api/ideas'

def ideas_list(request):
    page_number = request.GET.get('page', 1)
    page_size = request.GET.get('size', 10)
    sort = request.GET.get('sort', '-published_at')

    data = {
        'page[number]': page_number,
        'page[size]': page_size,
        'append[]': ['small_image', 'medium_image'],
        'sort': sort,
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    try:
        response = requests.get(API_URL, json=data, headers=headers)
        response.raise_for_status()
        response_data = response.json()
                
        if 'data' not in response_data:
            logger.error("API response does not contain 'data' key")
            response_data['data'] = []  # Fallback to empty list if 'data' key is missing
        
        ideas = response_data['data']
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        ideas = []

    for idea in ideas:
        idea['published_at_formatted'] = datetime.strptime(idea['published_at'], '%Y-%m-%d %H:%M:%S').strftime('%d %B %Y')
        



    paginator = Paginator(ideas, page_size)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'ideas': ideas,
        'page_size': page_size,
        'sort': sort,
    }

    return render(request, 'ideas/ideas_list.html', context)
