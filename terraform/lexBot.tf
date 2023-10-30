resource "aws_cloudformation_stack" "finalSprintBotStackv1" {
  name = "finalSprintBotStackv1"

  template_body = jsonencode({
    Resources = {
        schoolAssistantBot = {
            Type = "AWS::Lex::Bot"
            Properties = {
                Name                    = "finalSprintBot"
                Description             = "Ajuda imigrantes fracófonos com informações úteis e orientações no Brasil."
                IdleSessionTTLInSeconds = 300
                RoleArn                 = aws_iam_role.finalSprintBotIamRoleStackv1.arn
                AutoBuildBotLocales     = true

                BotTags = [
                    {
                    Key   = "Terraform"
                    Value = "true"
                    }
                ]

                DataPrivacy = {
                    ChildDirected = false
                }

                BotLocales = [{
                    LocaleId               = "pt_BR"
                    NluConfidenceThreshold = 0.4

                    Intents = [
                    {
                        Name = "IntroductionIntent"
                        Description = "Intent de boas vindas ao bot."
                        FulfillmentCodeHook = {
                            Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "ola" },
                            { Utterance = "Bonjour"},
                            { Utterance = "Bonsoir" },
                            { Utterance = "He" },
                            { Utterance = "salut" },
                            { Utterance = "Allo" },
                            { Utterance = "Salutations" }
                        ]
                    },
                    {
                        Name = "HelpsIntent"
                        Description = "Intent que retorna as opções de ajuda para o usuário imigrante."
                        InitialResponseSetting = {
                            InitialResponse = {
                                MessageGroupsList = [{
                                Message = {
                                    # ImageResponseCard = {
                                    #     Title    = "Opções"
                                    #     Subtitle = "Escolha uma das opções abaixo para acionar a ajuda!"
                                    #     Buttons  = [{
                                    #         "Text": "Como fazer documentos",
                                    #         "Value": "HowToMakeDocs"
                                    #     },
                                    #     {
                                    #         "Text": "Contatos de emergência",
                                    #         "Value": "EmergencyContacts"
                                    #     },
                                    #     {
                                    #         "Text": "Dicas de localização",
                                    #         "Value": "CepToTip"
                                    #     },
                                    #     {
                                    #         "Text": "Tradutor de texto e áudio",
                                    #         "Value": "TextAudioTranslater"
                                    #     },
                                    #     {
                                    #         "Text": "Extrator de texto de imagem",
                                    #         "Value": "ImageTextExtraction"
                                    #     }]
                                    # }
                                    PlainTextMessage = {
                                        Value = "Escolha uma das opções abaixo para acionar a ajuda! (Digite o número da opção)\nChoisissez l'une des options ci-dessous pour demander de l'aide ! (Saisissez le numéro de l'option)\n\n 1. Como Fazer Documentos de Imigração\nComment préparer des documents d'immigration\n 2. Contatos de Emergência\nContacts d'urgence\n 3. Locais de Interesse Conforme Região\nPoints d'intérêt par région\n 4. Tradutor de Texto e Áudio\nTraducteur de texte et audio\n 5. Extrator de Texto em Imagens\nExtracteur de texte dans les images"
                                    }
                                }
                                }]
                            }
                        }
                        SampleUtterances = [
                            { Utterance = "ajuda" },
                            { Utterance = "aide" },
                            { Utterance = "J'ai besoin d'assistance" },
                            { Utterance = "Pouvez-vous m'aider, s'il vous plaît ?" },
                            { Utterance = "Je requiers de l'aide" },
                            { Utterance = "Je suis à la recherche d'aide" },
                            
                        ]
                    },
                    {
                        Name        = "ImageTextExtractionIntent"
                        Description = "Recebe uma imagem do usuário imigrante e realiza a extração de texto contido na imagem e retorna para o usuário."
                        FulfillmentCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "ImageTextExtraction" },
                        ]
                        Slots = [
                            {
                                Name         = "textOrAudioConditional"
                                SlotTypeName = "AMAZON.AlphaNumeric" # Recognizes words made up of letters and numbers.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                # ImageResponseCard = {
                                                #     Title = "Você deseja receber o texto extraído da imagem ou um áudio com o texto extraído?"
                                                #     Buttons = [{
                                                #         "Text": "Texto em Francês",
                                                #         "Value": "text_fr"
                                                #     },
                                                #     {
                                                #         "Text": "Áudio em Francês",
                                                #         "Value": "audio_fr"
                                                #     },
                                                #     {
                                                #         "Text": "Texto em Português",
                                                #         "Value": "text_pt"
                                                #     },
                                                #     {
                                                #         "Text": "Áudio em Português",
                                                #         "Value": "audio_pt"
                                                #     }]
                                                # }
                                                PlainTextMessage = {
                                                    Value = "Você deseja receber o texto extraído da imagem ou um áudio com o texto extraído? (Digite o número da opção)\nSouhaitez-vous recevoir le texte extrait de l'image ou un audio avec le texte extrait ? (Entrez le numéro de l'option)\n\n 1. Texto em Francês\nTexte en français\n 2. Áudio em Francês\nAudio en français\n 3. Texto em Português\nTexte en portugais\n 4. Áudio em Português\nAudio en portugais"
                                                }
                                            }
                                        }]
                                    }
                                }
                            },
                            {
                                Name         = "imgFromUser"
                                SlotTypeName = "AMAZON.FreeFormInput" # Recognizes strings that consist of any words or characters.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                PlainTextMessage = {
                                                    Value = "Por favor, envie a imagem contendo o texto que deseja extrair.\nVeuillez envoyer l'image contenant le texte que vous souhaitez extraire, s'il vous plaît."
                                                }
                                            }
                                        }]
                                    }
                                }
                            }
                        ]
                        SlotPriorities = [
                            { Priority = 1, SlotName = "textOrAudioConditional" },
                            { Priority = 2, SlotName = "imgFromUser" }
                        ]
                        IntentClosingSetting = {
                            ClosingResponse = {
                                MessageGroupsList = [{
                                    Message = {
                                        PlainTextMessage = {
                                            Value = "Obrigado por utilizar o nosso serviço!\nMerci d'utiliser notre service !"
                                        }
                                    }
                                }]
                            }
                        }
                    },
                    {
                        Name = "TextAudioTranslaterIntent"
                        Description = "Recebe um texto ou um áudio do usuário imigrante retorna um texto traduzido para portugues ou áudio do texto traduzido."
                        FulfillmentCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "TextAudioTranslater" },
                            { Utterance = "AudioTextTraducteur" }
                        ]
                        Slots = [
                            {
                                Name          = "textOrAudioUserInput"
                                SlotTypeName  = "AMAZON.AlphaNumeric" # Recognizes words made up of letters and numbers.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                # ImageResponseCard = {
                                                #     Title = "Você deseja traduzir um texto ou um áudio do português -> francês ou francês -> português?"
                                                #     Buttons = [{
                                                #         "Text": "Português para o francês",
                                                #         "Value": "ptToFr"
                                                #     },
                                                #     {
                                                #         "Text": "Francês para o português",
                                                #         "Value": "frToPt"
                                                #     }]
                                                # }
                                                PlainTextMessage = {
                                                    Value = "Você quer traduzir um áudio ou um texto? (Digite o número da opção)\nSouhaitez-vous traduire un audio ou un texte ? (Veuillez entrer le numéro de l'option)\n\n 1. Áudio\nAudio\n 2. Texto\nTexte"
                                                }
                                            }
                                        }]
                                    }
                                }
                            },
                            {
                                Name          = "languageConditional"
                                SlotTypeName  = "AMAZON.AlphaNumeric" # Recognizes words made up of letters and numbers.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                # ImageResponseCard = {
                                                #     Title = "Você deseja traduzir um texto ou um áudio do português -> francês ou francês -> português?"
                                                #     Buttons = [{
                                                #         "Text": "Português para o francês",
                                                #         "Value": "ptToFr"
                                                #     },
                                                #     {
                                                #         "Text": "Francês para o português",
                                                #         "Value": "frToPt"
                                                #     }]
                                                # }
                                                PlainTextMessage = {
                                                    Value = "Você deseja traduzir do português -> francês ou francês -> português? (Digite o número da opção)\nSouhaitez-vous traduire du portugais vers le français ou du français vers le portugais ? (Veuillez entrer le numéro de l'option)\n\n 1. Português para o francês\nPortugais en français\n 2. Francês para o português\nFrançais en portugais"
                                                }
                                            }
                                        }]
                                    }
                                }
                            },
                            {
                                Name         = "textOrAudioConditional"
                                SlotTypeName = "AMAZON.AlphaNumeric" # Recognizes words made up of letters and numbers.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                # ImageResponseCard = {
                                                #     Title = "Você deseja receber o texto ou áudio enviado como um áudio ou como texto?"
                                                #     Buttons = [{
                                                #         "Text": "Como texto",
                                                #         "Value": "text"
                                                #     },
                                                #     {
                                                #         "Text": "Como áudio",
                                                #         "Value": "audio"
                                                #     }]
                                                # }
                                                PlainTextMessage = {
                                                    Value = "Você deseja receber o texto ou áudio enviado como um áudio ou como texto? (Digite o número da opção)\nSouhaitez-vous recevoir le texte ou l'audio envoyé sous forme de texte ou d'audio ? (Veuillez entrer le numéro de l'option)\n\n 1. Como texto\nComme texte\n 2. Como áudio\nComme audio"
                                                }
                                            }
                                        }]
                                    }
                                }
                            },
                            {
                                Name         = "textOrAudioReceiver"
                                SlotTypeName = "AMAZON.FreeFormInput" # Recognizes words made up of letters and numbers.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                PlainTextMessage = {
                                                    Value = "Envie o texto ou áudio que deseja traduzir.\nEnvoyez le texte ou l'audio que vous souhaitez traduire, s'il vous plaît"
                                                }
                                            }
                                        }]
                                    }
                                }
                            }
                        ]
                        SlotPriorities = [
                            { Priority = 1, SlotName = "textOrAudioUserInput" },
                            { Priority = 2, SlotName = "languageConditional" },
                            { Priority = 3, SlotName = "textOrAudioConditional" },
                            { Priority = 4, SlotName = "textOrAudioReceiver" }
                        ]
                    },
                    {
                        Name = "CepToTipIntent"
                        Description = "recebe um cep do usuário imigrante e retorna dicas de onde ficam hospitais, restaurates, etc."
                        FulfillmentCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "CepToTip" }
                        ]
                        Slots = [
                            {
                                Name         = "cepFromUser"
                                SlotTypeName = "AMAZON.AlphaNumeric" # Recognizes words made up of letters and numbers.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                PlainTextMessage = {
                                                    Value = "Por favor, envie o cep da sua localização (apenas números). \nVeuillez envoyer le code postal de votre emplacement (uniquement les chiffres).\n\n Caso não saiba o seu cep, você pode consultá-lo em: https://buscacepinter.correios.com.br/app/endereco/index.php.\nSi vous ne connaissez pas votre code postal, vous pouvez le consulter à l'adresse suivante : https://buscacepinter.correios.com.br/app/endereco/index.php."
                                                }
                                            }
                                        }]
                                    }
                                }
                            },
                            {
                                Name         = "pointsOfInterest"
                                SlotTypeName = "AMAZON.AlphaNumeric" # Recognizes words made up of letters and numbers.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                # ImageResponseCard = {
                                                #     Title = "Qual ponto de interesse você deseja saber a localização mais próxima?"
                                                #     Buttons = [{
                                                #         "Text": "Hospital",
                                                #         "Value": "hospital"
                                                #     },
                                                #     {
                                                #         "Text": "Policia",
                                                #         "Value": "police"
                                                #     },
                                                #     {
                                                #         "Text": "Restaurante",
                                                #         "Value": "restaurant"
                                                #     }]
                                                # }
                                                PlainTextMessage = {
                                                    Value = "Qual ponto de interesse você deseja saber a localização mais próxima? (Digite o número da opção)\nQuel point d'intérêt souhaitez-vous connaître la localisation la plus proche ? (Entrez le numéro de l'option)\n\n 1. Hospital\nHôpital\n 2. Policia\nPolice\n 3. Restaurante\nRestaurant"
                                                }
                                            }
                                        }]
                                    }
                                }
                            }
                        ]
                        SlotPriorities = [
                            { Priority = 1, SlotName = "cepFromUser" },
                            { Priority = 2, SlotName = "pointsOfInterest" }
                        ]
                    },
                    {
                        Name = "EmergencyContactsIntent"
                        Description = "retorna contatos de emergência para o usuário imigrante, como ambulancias e policia."
                        FulfillmentCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "EmergencyContacts" },
                            { Utterance = "ContactsUrgences" }
                        ]
                        Slots = [
                            {
                                Name         = "emergencyContact"
                                SlotTypeName = "AMAZON.AlphaNumeric" # Recognizes words made up of letters and numbers.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                # ImageResponseCard = {
                                                #     Title = "Qual contato de emergência você deseja?"
                                                #     Buttons = [{
                                                #         "Text": "Ambulância",
                                                #         "Value": "ambulancia"
                                                #     },
                                                #     {
                                                #         "Text": "Policia",
                                                #         "Value": "policia"
                                                #     },
                                                #     {
                                                #         "Text": "Bombeiros",
                                                #         "Value": "bombeiros"
                                                #     }]
                                                # }
                                                PlainTextMessage = {
                                                    Value = "Qual contato de emergência você deseja? (Digite o número da opção)\nQuel contact d'urgence souhaitez-vous ? (Entrez le numéro de l'option)\n\n 1. Ambulância\nAmbulance\n 2. Policia\nPolice\n 3. Bombeiros\nPompiers"
                                                }
                                            }
                                        }]
                                    }
                                }
                            }
                        ]
                        SlotPriorities = [
                            { Priority = 1, SlotName = "emergencyContact" }
                        ]
                    },
                    {
                        Name = "HowToMakeDocsIntent"
                        Description = "retorna informações sobre como fazer documentos para o usuário imigrante."
                        FulfillmentCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "HowToMakeDocs" },
                            { Utterance = "CommentCreerDesDocuments" }
                        ]
                    },
                    {
                        Name                  = "FallbackIntent"
                        ParentIntentSignature = "AMAZON.FallbackIntent"
                        Description           = "Intent que é acionada quando o usuário digita algo que não é reconhecido"
                    }]
                }]
            }
        }
    }
    })
}