import requests
from config.config import GOOGLE_API_KEY  

def get_nearby_locations(query_input: str) -> list:
    """
    Makes a request to the Google Places API to fetch nearby locations based on a query.

    Args:
        query_input (str): A string that specifies the type of doctor and location to search for.

    Returns:
        list: A list of dictionaries containing the names and addresses of the found locations.

    Raises:
        Exception: If the API request fails or returns an error status code.
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "key": GOOGLE_API_KEY,  
        "query": query_input,
        "radius": 10000, 
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        return [
            {
                "name": place.get("name", "Nome não disponível"),  
                "address": place.get("formatted_address", "Endereço não disponível"), 
            }
            for place in results
        ]
    else:
        raise Exception(f"Erro ao chamar a API: {response.status_code} - {response.text}")

def get_location(query_input: str) -> str:
    """
    Handles the input, calls the get_nearby_locations function, and formats the result for output.

    Args:
        query_input (str): The query string.

    Returns:
        str: The formatted result containing the names and addresses of nearby locations.
    
    Raises:
        Exception: If any error occurs while processing the location request.
    """
    try:
        locations = get_nearby_locations(query_input)

        max_locations = 8
        locations = locations[:max_locations]
        
        locais = "Encontrei os seguintes locais próximos:\n\n" + "\n\n".join(
            f"📍Nome: {local.get('name', 'Nome não disponível')}\n"
            f"📫Endereço: {local.get('address', 'Endereço não disponível')}"
            for local in locations
        )
    
        return locais
    
    except Exception as e:
        return f"Erro: {str(e)}"