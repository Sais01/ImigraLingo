from core.config import settings
from services.rekognition_service import extract_text_from_image
from utils.response_formatters import prepare_response_text

def handle_image_to_text(event, context):
    try:
        BUCKET_NAME = settings.BUCKET_NAME
        IMAGE_NAME = settings.IMAGE_NAME
        
        response_text_from_image = extract_text_from_image(BUCKET_NAME, IMAGE_NAME)

        text_from_image = response_text_from_image["body"]["phrase"]

        print("1######################")
        print(response_text_from_image["body"])
        print("1@@@@@@@@@@@@@@@@@@@@@@")

        print("2######################")
        print(text_from_image)
        print("2@@@@@@@@@@@@@@@@@@@@@@")


        # slots = event["interpretations"][0]["intent"]["slots"]

        return prepare_response_text(event, text_from_image)



    except Exception as e:
        print(f"Error in image_text_extraction_controller: {e}")
        return prepare_response_text(
            event, f"Erreur lors du traitement de la demande d'achat: {str(e)}"
        )

