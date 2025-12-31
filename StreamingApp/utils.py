
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

def get_full_image_url(path):
    if not path:
        return "https://via.placeholder.com/500x750?text=No+Image"
    return f"{IMAGE_BASE_URL}{path}"

def format_provider_data(provider_data, country_code='US'):
    """
    Extracts flatrate (streaming), rent, and buy options for a specific country.
    """
    country_data = provider_data.get(country_code)
    if not country_data:
        return None
    
    return {
        'link': country_data.get('link'),
        'flatrate': country_data.get('flatrate', []),
        'rent': country_data.get('rent', []),
        'buy': country_data.get('buy', [])
    }
