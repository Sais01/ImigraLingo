from services.geo_service import cep_to_location, location_to_coordinates, places_by_coordinates

def handle_cep_to_places(cep):
  address = cep_to_location(cep)
  if address:
    lat, lon = location_to_coordinates(address)
    places_by_coordinates(lat, lon)

# TESTE
if __name__ == "__main__":
  handle_cep_to_places("96203410")