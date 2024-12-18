import requests
from django.contrib import messages


def get_results_api(request, api_url: str | None):
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
