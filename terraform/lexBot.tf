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
                                        Value = "Escolha uma das opções abaixo para acionar a ajuda! (Digite o número da opção)😃 \nChoisissez l'une des options ci-dessous pour demander de l'aide ! (Saisissez le numéro de l'option)😃\n\n 1️⃣ Como Fazer Documentos de Imigração / Comment préparer des documents d'immigration\n 2️⃣ Contatos de Emergência / Contacts d'urgence\n 3️⃣ Locais de Interesse Conforme Região / Points d'intérêt par région\n 4️⃣ Tradutor de Texto e Áudio / Traducteur de texte et audio\n 5️⃣ Extrator de Texto em Imagens / Extracteur de texte dans les images" 
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
                                                    Value = "Você deseja receber o texto extraído da imagem ou um áudio com o texto extraído? (Digite o número da opção) / Souhaitez-vous recevoir le texte extrait de l'image ou un audio avec le texte extrait ? (Entrez le numéro de l'option)\n\n 1️⃣ Texto em Francês / Texte en français\n 2️⃣ Áudio em Francês / Audio en français\n 3️⃣ Texto em Português / Texte en portugais\n 4️⃣ Áudio em Português / Audio en portugais" 
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
                                                    Value = "Por favor, envie a imagem contendo o texto que deseja extrair. / Veuillez envoyer l'image contenant le texte que vous souhaitez extraire, s'il vous plaît."
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
                                            Value = "Obrigado por utilizar o nosso serviço! / Merci d'utiliser notre service !"
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
                                                    Value = "Você quer traduzir um áudio ou um texto? (Digite o número da opção) / Souhaitez-vous traduire un audio ou un texte ? (Veuillez entrer le numéro de l'option)\n\n 1️⃣ Áudio / Audio\n 2️⃣ Texto / Texte"
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
                                                    Value = "Você deseja traduzir do português -> francês ou francês -> português? (Digite o número da opção) / Souhaitez-vous traduire du portugais vers le français ou du français vers le portugais ? (Veuillez entrer le numéro de l'option)\n\n 1️⃣ Português para o francês / Portugais en français\n 2️⃣ Francês para o português / Français en portugais"
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
                                                    Value = "Você deseja receber o texto ou áudio enviado como um áudio ou como texto? (Digite o número da opção) / Souhaitez-vous recevoir le texte ou l'audio envoyé sous forme de texte ou d'audio ? (Veuillez entrer le numéro de l'option)\n\n 1️⃣ Como texto / Comme texte\n 2️⃣ Como áudio / Comme audio"
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
                                                    Value = "Envie o texto ou áudio que deseja traduzir. / Envoyez le texte ou l'audio que vous souhaitez traduire, s'il vous plaît"
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
                                                    Value = "Por favor, envie o cep da sua localização (apenas números). / Veuillez envoyer le code postal de votre emplacement (uniquement les chiffres).\n\n Caso não saiba o seu cep, você pode consultá-lo em: https://buscacepinter.correios.com.br/app/endereco/index.php. / Si vous ne connaissez pas votre code postal, vous pouvez le consulter à l'adresse suivante : https://buscacepinter.correios.com.br/app/endereco/index.php."
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
                                                    Value = "Qual ponto de interesse você deseja saber a localização mais próxima? (Digite o número da opção) / Quel point d'intérêt souhaitez-vous connaître la localisation la plus proche ? (Entrez le numéro de l'option)\n\n 1️⃣ Hospital / Hôpital\n 2️⃣ Policia / Police\n 3️⃣ Restaurante / Restaurant"
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
                                                    Value = "Qual contato de emergência você deseja? (Digite o número da opção) / Quel contact d'urgence souhaitez-vous ? (Entrez le numéro de l'option)\n\n 1️⃣ Ambulância / Ambulance\n 2️⃣ Policia / Police\n 3️⃣ Bombeiros / Pompiers"
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