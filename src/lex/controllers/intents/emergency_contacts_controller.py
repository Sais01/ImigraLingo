from utils.response_formatters import prepare_response_text

def handle_emergency_contacts(event, context):
    """
    Handles the emergency contacts intent in a Lex bot. Parses the input slot for the type of emergency contact requested
    (police, ambulance, or firefighters) and returns a response with the appropriate emergency contact number.
    
    Args:
    - event (dict): The event data passed by the AWS service to the Lambda function.
    - context (object): The context object passed by the AWS service to the Lambda function.
    
    Returns:
    - dict: A response object containing the appropriate emergency contact number based on the input slot value.
    """
    try:
        slots          = event['interpretations'][0]['intent']['slots']
        emergencyInput = slots['emergencyContact']['value']['interpretedValue']

        if emergencyInput == 'policia':
            return prepare_response_text(event, "Vous pouvez contacter la police au 190.")
        elif emergencyInput == 'ambulancia':
            return prepare_response_text(event, "Vous pouvez contacter les ambulance au 192.")
        elif emergencyInput == 'bombeiro':
            return prepare_response_text(event, "Vous pouvez contacter les pompiers au 193.")
        
    except Exception as e:
        print(f"Error in cep_to_places_controller: {e}")
        return prepare_response_text(event, f"Erreur lors du traitement de la demande d'achat: {str(e)}")