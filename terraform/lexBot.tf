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
                        InitialResponseSetting = {
                            InitialResponse = {
                                MessageGroupsList = [{
                                Message = {
                                    PlainTextMessage = {
                                        Value = "Boas vindas ao Bot de ajuda ao imigrante! O que deseja fazer?"
                                    }
                                }
                                }]
                            }
                        }
                        SampleUtterances = [
                            { Utterance = "ola" }
                        ]
                    },
                    {
                        Name        = "ImageTextExtractionIntent"
                        Description = "Recebe uma imagem do usuário imigrante e realiza a extração de texto contido na imagem e retorna para o usuário."
                        DialogCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "ImageTextExtraction" },
                        ]
                        Slots = [
                            {
                                Name         = "DadoAluno"
                                SlotTypeName = "AMAZON.AlphaNumeric"
                                ValueElicitationSetting = {
                                    SlotConstraint = "Required"
                                    PromptSpecification = {
                                        MaxRetries = 2
                                        MessageGroupsList = [{
                                            Message = {
                                                ImageResponseCard = {
                                                    Title = "Consulta de dados do aluno"
                                                    Buttons = [{
                                                        "Text": "1",
                                                        "Value": "1"
                                                    },
                                                    {
                                                        "Text": "2",
                                                        "Value": "2"
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
                                                                Value = "Aguarde enquanto consulto os dados do aluno"
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
                            { Priority = 1, SlotName = "DadoAluno" }
                        ]
                    },
                    {
                        Name = "TextAudioTranslater"
                        Description = "recebe um texto ou um áudio do usuário imigrante retorna um texto traduzido para portugues ou áudio do texto traduzido."
                        DialogCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "TextAudioTranslater" },
                        ]
                    },
                    {
                        Name = "CepToTip"
                        Description = "recebe um cep do usuário imigrante e retorna dicas de onde ficam hospitais, restaurates, etc."
                        DialogCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "CepToTip" },
                        ]
                    },
                    {
                        Name = "EmergencyContacts"
                        Description = "retorna contatos de emergência para o usuário imigrante, como ambulancias e policia."
                        DialogCodeHook = {
                          Enabled = true
                        }
                        SampleUtterances = [
                            { Utterance = "EmergencyContacts" },
                        ]
                    },
                    {
                        Name = "HowToMakeDocs"
                        Description = "retorna informações sobre como fazer documentos para o usuário imigrante."
                        DialogCodeHook = {
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