#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

def subject_pass(lang):
    """
    External function to translate
    """

    if lang == "ca":
        subject = "Dr.Scratch: ¿Ha oblidat la seva contrasenya?"
    elif lang == "es":
        subject = "Dr.Scratch: ¿Olvidaste tu contraseña?"
    elif lang == "en":
        subject = "Dr.Scratch: Did you forget your password?"
    elif lang == "gl":
        subject = "Dr.Scratch: Esqueciches o teu contrasinal?"
    elif lang == "pt":
        subject = "Dr.Scratch: Esqueceu sua senha?"
    elif lang == "el":
        subject = "Dr.Scratch: Ξεχάσατε τον κωδικό σας;"
    elif lang == "eu":
        subject = "Dr.Scratch: Did you forget your password?"
    return subject


def subject_welcome_organization(lang):
    """
    External function to translate
    """

    if lang == "ca":
        subject = "Benvingut a Dr.Scratch per a les organitzacions"
    elif lang == "es":
        subject = "Bienvenido a Dr.Scratch para organizaciones"
    elif lang == "en":
        subject = "Welcome to Dr.Scratch for organizations"
    elif lang == "gl":
        subject = "Benvido ao Dr.Scratch para organizacións"
    elif lang == "pt":
        subject = "Bem-vindo ao Dr.Scratch para organizações"
    elif lang == "el":
        subject = "Καλώς ήρθατε στο Dr.Scratch για τους οργανισμούς"
    elif lang == "eu":
        subject = "Welcome to Dr.Scratch for organizations"
    return subject

def subject_welcome_coder(lang):
    """
    External function to translate
    """

    if lang == "ca":
        subject = "Benvingut a Dr.Scratch!"
    elif lang == "es":
        subject = "¡Bienvenido a Dr.Scratch!"
    elif lang == "en":
        subject = "Welcome to Dr.Scratch!"
    elif lang == "gl":
        subject = "Benvido ao Dr.Scratch!"
    elif lang == "pt":
        subject = "Bem-vindo ao Dr.Scratch!"
    elif lang == "el":
        subject = "Καλώς ήρθατε στο Dr.Scratch!"
    elif lang == "en":
        subject = "Welcome to Dr.Scratch!"
    return subject
