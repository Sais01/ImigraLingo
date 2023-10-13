from services.geo_service import cep_to_location, location_to_coordinates, places_by_coordinates
from utils import prepare_response_text

def handle_cep_to_places(event, context):
  slots = event['interpretations'][0]['intent']['slots']
  cep = slots['cep']['value']['interpretedValue']
  place_type = slots['place_type']['value']['interpretedValue']
  address = cep_to_location(cep)
  if address:
    lat, lon = location_to_coordinates(address)
    response = places_by_coordinates(lat, lon, place_type)

    return prepare_response_text(event, response)

# TESTE
# if __name__ == "__main__":
#   handle_cep_to_places("96203410")