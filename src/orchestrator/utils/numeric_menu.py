intents = {
    "IntroductionIntent" : {},
    "HelpsIntent"        : {},
    "HowToMakeDocsIntent": {},
    "ImageTextExtractionIntent": {
        "slots": {
          "textOrAudioConditional": ["text_fr", "audio_fr", "text_pt", "audio_pt"],
        }
    },
    "TextAudioTranslaterIntent": {
        "slots": {
          "textOrAudioUserInput"  : ["audio", "text" ],
          "languageConditional"   : ["ptToFr", "frToPt"],
          "textOrAudioConditional": ["text", "audio"]
        }
    },
    "CepToTipIntent": {
        "slots": {
          "pointsOfInterest":["hospital", "police", "restaurant"]
        }
    },
    "EmergencyContactsIntent": {
        "slots": {
            "emergencyContact": ["ambulancia", "policia", "bombeiros"]
        }
    }
}

def numeric_menu(intent, slot, userOptionInput):
    """
    This function receives three parameters: intent, slot and userOptionInput.
    It checks the values of these parameters and returns the corresponding value from the intents dictionary.

    Parameters:
    intent (str): The intent of the user input.
    slot (str): The slot of the user input.
    userOptionInput (str): The user input option.

    Returns:
    str: The corresponding value from the intents dictionary.
    """
    intentSlotsValues = intents.get(intent)
    slotsValues       = intentSlotsValues.get("slots")
    slot              = slotsValues.get(slot)

    return slot[int(userOptionInput) - 1]