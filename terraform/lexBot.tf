resource "aws_cloudformation_stack" "finalSprintBotStackv1" {
  name = "finalSprintBotStackv1"

  template_body = jsonencode({
    Resources = {
        schoolAssistantBot = {
            Type = "AWS::Lex::Bot"
            Properties = {
                Name                    = "finalSprintBotv1"
                Description             = "Ajuda imigrantes haitianos/franceses com informações úteis e orientações"
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
                        # InitialResponseSetting = {
                        #     InitialResponse = {
                        #         MessageGroupsList = [{
                        #         Message = {
                        #             PlainTextMessage = {
                        #                 Value = "Boas vindas ao ImigraLingo, bot de ajuda ao imigrante! O que deseja fazer?"
                        #             }
                        #         }
                        #         }]
                        #     }
                        # }
                        SampleUtterances = [
                            { Utterance = "ola" }
                        ]
                    },
                    {
                        Name = "HelpsIntent"
                        Description = "Intent que retorna as opções de ajuda para o usuário imigrante."
                        InitialResponseSetting = {
                            InitialResponse = {
                                MessageGroupsList = [{
                                Message = {
                                    ImageResponseCard = {
                                        Title    = "Opções"
                                        Subtitle = "Escolha uma das opções abaixo para acionar a ajuda!"
                                        Buttons  = [{
                                            "Text": "Como fazer documentos",
                                            "Value": "HowToMakeDocs"
                                        },
                                        {
                                            "Text": "Contatos de emergência",
                                            "Value": "EmergencyContacts"
                                        },
                                        {
                                            "Text": "Dicas de localização",
                                            "Value": "CepToTip"
                                        },
                                        {
                                            "Text": "Tradutor de texto e áudio",
                                            "Value": "TextAudioTranslater"
                                        },
                                        {
                                            "Text": "Extrator de texto de imagem",
                                            "Value": "ImageTextExtraction"
                                        }]
                                    }
                                }
                                }]
                            }
                        }
                        SampleUtterances = [
                            { Utterance = "ajuda" }
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
                                Name         = "imgFromUser"
                                SlotTypeName = "AMAZON.FreeFormInput" # Recognizes strings that consist of any words or characters.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                PlainTextMessage = {
                                                    Value = "Por favor, envie a imagem contendo o texto que deseja extrair."
                                                }
                                            }
                                        }]
                                    },
                                    SlotCaptureSetting = {
                                        CodeHook = {
                                            EnableCodeHookInvocation = true
                                            IsActive = true
                                            PostCodeHookSpecification = {
                                                SuccessResponse = {
                                                    MessageGroupsList = [{
                                                        Message = {
                                                            PlainTextMessage = {
                                                                Value = "Essa mensagem não é usada."
                                                            }
                                                        }
                                                    }]
                                                }
                                            }
                                        }
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
                                                ImageResponseCard = {
                                                    Title = "Você deseja receber o texto extraído da imagem ou um áudio com o texto extraído?"
                                                    Buttons = [{
                                                        "Text": "Texto em Francês",
                                                        "Value": "text_fr"
                                                    },
                                                    {
                                                        "Text": "Áudio em Francês",
                                                        "Value": "audio_fr"
                                                    },
                                                    {
                                                        "Text": "Texto em Português",
                                                        "Value": "text_pt"
                                                    },
                                                    {
                                                        "Text": "Áudio em Português",
                                                        "Value": "audio_pt"
                                                    }]
                                                }
                                            }
                                        }]
                                    },
                                    SlotCaptureSetting = {
                                        CodeHook = {
                                            EnableCodeHookInvocation = true
                                            IsActive = true
                                            PostCodeHookSpecification = {
                                                SuccessResponse = {
                                                    MessageGroupsList = [{
                                                        Message = {
                                                            PlainTextMessage = {
                                                                Value = "Essa mensagem não é usada."
                                                            }
                                                        }
                                                    }]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                        SlotPriorities = [
                            { Priority = 1, SlotName = "imgFromUser" },
                            { Priority = 2, SlotName = "textOrAudioConditional" }
                        ]
                    },
                    {
                        Name = "TextAudioTranslaterIntent"
                        Description = "Recebe um texto ou um áudio do usuário imigrante retorna um texto traduzido para portugues ou áudio do texto traduzido."
                        FulfillmentCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "TextAudioTranslater" },
                        ]
                        Slots = [
                            {
                                Name          = "languageConditional"
                                SlotTypeName  = "AMAZON.AlphaNumeric" # Recognizes words made up of letters and numbers.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                ImageResponseCard = {
                                                    Title = "Você deseja traduzir um texto ou um áudio do português -> francês ou francês -> português?"
                                                    Buttons = [{
                                                        "Text": "Português para o francês",
                                                        "Value": "ptToFr"
                                                    },
                                                    {
                                                        "Text": "Francês para o português",
                                                        "Value": "frToPt"
                                                    }]
                                                }
                                            }
                                        }]
                                    },
                                    SlotCaptureSetting = {
                                        CodeHook = {
                                            EnableCodeHookInvocation = true
                                            IsActive = true
                                            PostCodeHookSpecification = {
                                                SuccessResponse = {
                                                    MessageGroupsList = [{
                                                        Message = {
                                                            PlainTextMessage = {
                                                                Value = "Essa mensagem não é usada."
                                                            }
                                                        }
                                                    }]
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                Name         = "textOrAudioReceiver"
                                SlotTypeName = "AMAZON.AlphaNumeric" # Recognizes words made up of letters and numbers.
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 1
                                        MessageGroupsList = [{
                                            Message = {
                                                PlainTextMessage = {
                                                    Value = "Por favor, envie o texto ou áudio a ser traduzido."
                                                }
                                            }
                                        }]
                                    },
                                    SlotCaptureSetting = {
                                        CodeHook = {
                                            EnableCodeHookInvocation = true
                                            IsActive = true
                                            PostCodeHookSpecification = {
                                                SuccessResponse = {
                                                    MessageGroupsList = [{
                                                        Message = {
                                                            PlainTextMessage = {
                                                                Value = "Essa mensagem não é usada."
                                                            }
                                                        }
                                                    }]
                                                }
                                            }
                                        }
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
                                                ImageResponseCard = {
                                                    Title = "Você deseja receber o texto ou áudio enviado como um áudio ou como texto?"
                                                    Buttons = [{
                                                        "Text": "Como texto",
                                                        "Value": "text"
                                                    },
                                                    {
                                                        "Text": "Como áudio",
                                                        "Value": "audio"
                                                    }]
                                                }
                                            }
                                        }]
                                    },
                                    SlotCaptureSetting = {
                                        CodeHook = {
                                            EnableCodeHookInvocation = true
                                            IsActive = true
                                            PostCodeHookSpecification = {
                                                SuccessResponse = {
                                                    MessageGroupsList = [{
                                                        Message = {
                                                            PlainTextMessage = {
                                                                Value = "Essa mensagem não é usada."
                                                            }
                                                        }
                                                    }]
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                        SlotPriorities = [
                            { Priority = 1, SlotName = "languageConditional" },
                            { Priority = 2, SlotName = "textOrAudioReceiver" },
                            { Priority = 3, SlotName = "textOrAudioConditional" }
                        ]
                    },
                    {
                        Name = "CepToTipIntent"
                        Description = "recebe um cep do usuário imigrante e retorna dicas de onde ficam hospitais, restaurates, etc."
                        FulfillmentCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "CepToTip" },
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
                                                    Value = "Por favor, envie o cep da sua localização (apenas números)."
                                                }
                                            }
                                        }]
                                    },
                                    SlotCaptureSetting = {
                                        CodeHook = {
                                            EnableCodeHookInvocation = true
                                            IsActive = true
                                            PostCodeHookSpecification = {
                                                SuccessResponse = {
                                                    MessageGroupsList = [{
                                                        Message = {
                                                            PlainTextMessage = {
                                                                Value = "Essa mensagem não é usada."
                                                            }
                                                        }
                                                    }]
                                                }
                                            }
                                        }
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
                                                ImageResponseCard = {
                                                    Title = "Qual ponto de interesse você deseja saber a localização mais próxima?"
                                                    Buttons = [{
                                                        "Text": "Hospital",
                                                        "Value": "hospital"
                                                    },
                                                    {
                                                        "Text": "Policia",
                                                        "Value": "police"
                                                    },
                                                    {
                                                        "Text": "Restaurante",
                                                        "Value": "restaurant"
                                                    }]
                                                }
                                            }
                                        }]
                                    },
                                    SlotCaptureSetting = {
                                        CodeHook = {
                                            EnableCodeHookInvocation = true
                                            IsActive = true
                                            PostCodeHookSpecification = {
                                                SuccessResponse = {
                                                    MessageGroupsList = [{
                                                        Message = {
                                                            PlainTextMessage = {
                                                                Value = "Essa mensagem não é usada."
                                                            }
                                                        }
                                                    }]
                                                }
                                            }
                                        }
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
                                                ImageResponseCard = {
                                                    Title = "Qual contato de emergência você deseja?"
                                                    Buttons = [{
                                                        "Text": "Ambulância",
                                                        "Value": "ambulancia"
                                                    },
                                                    {
                                                        "Text": "Policia",
                                                        "Value": "policia"
                                                    },
                                                    {
                                                        "Text": "Bombeiros",
                                                        "Value": "bombeiros"
                                                    }]
                                                }
                                            }
                                        }]
                                    },
                                    SlotCaptureSetting = {
                                        CodeHook = {
                                            EnableCodeHookInvocation = true
                                            IsActive = true
                                            PostCodeHookSpecification = {
                                                SuccessResponse = {
                                                    MessageGroupsList = [{
                                                        Message = {
                                                            PlainTextMessage = {
                                                                Value = "Essa mensagem não é usada."
                                                            }
                                                        }
                                                    }]
                                                }
                                            }
                                        }
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