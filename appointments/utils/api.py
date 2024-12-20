import requests
from django.contrib import messages


def get_results_api(request, api_url: str | None) -> list:
    """
    Fetches data from an external API and returns the results.

    Args:
        request (HttpRequest): The HTTP request object used for displaying messages.
        api_url (Optional[str]): The URL of the API to fetch data from. If not provided,
            an error message is shown.

    Returns:
        list: A list of results from the API response. If no results are found or an error occurs,
            an empty list is returned.

    Raises:
        requests.exceptions.RequestException: If there is an error in the HTTP request.
    """
    if not api_url:
        messages.error(request, 'URL da API não está configurada.')
        return []

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json().get('results', [])
        return data

    except requests.exceptions.RequestException as e:
        messages.error(
            request, f'Erro ao pegar informações: {str(e)}')
        return []
