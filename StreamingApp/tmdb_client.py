
import requests

class TMDBClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def search_multi(self, query):
        """
        Search for movies and TV shows.
        """
        endpoint = "/search/multi"
        params = {
            "query": query,
            "include_adult": "false",
            "language": "en-US",
            "page": 1
        }
        data = self._get(endpoint, params)
        return data.get('results', [])

    def get_watch_providers(self, content_type, content_id):
        """
        Get watch providers for a movie or TV show.
        content_type: 'movie' or 'tv'
        """
        endpoint = f"/{content_type}/{content_id}/watch/providers"
        data = self._get(endpoint)
        return data.get('results', {})

    def get_details(self, content_type, content_id):
        """
        Get details for a movie or TV show.
        """
        endpoint = f"/{content_type}/{content_id}"
        return self._get(endpoint)
