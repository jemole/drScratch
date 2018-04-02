#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-

def translate_CT(lang):
    """
    External function to translate CT Skills
    """

    if lang == "ca":
        dic = {"code":"CODI",
               "url":"URL",
               "mastery":"Mastery",
               "abstraction":"Abstracció",
               "parallelism":"Paral·lelisme",
               "logic":"Lògica ",
               "sync":"Sincronització",
               "flow_control":"Controls de flux ",
               "user_inter":"Interactivitat de l'usuari",
               "data_rep":"Representació de dades",
               "dup_scripts":"Programes duplicats",
               "sprite_naming":"Noms per defecte",
               "dead_code":"Codi mort",
               "attr_init":"Atributs no inicialitzats correctament",
               "error":"Error analitzant el projecte"}

    elif lang == "es":
        dic = {"code":"CÓDIGO",
               "url":"URL",
               "mastery":"Mastery",
               "abstraction":"Abstracción",
               "parallelism":"Paralelismo",
               "logic":"Pensamiento lógico",
               "sync":"Sincronización",
               "flow_control": "Control de flujo",
               "user_inter":"Interactividad con el usuario",
               "data_rep":"Representación de la información",
               "dup_scripts":"Código repetido",
               "sprite_naming":"Nombres por defecto",
               "dead_code":"Código muerto",
               "attr_init":"Inicialización atributos",
               "error":"Error analizando el proyecto"}

    elif lang == "en":
        dic = {"code":"CODE",
               "url":"URL",
               "mastery":"Mastery",
               "abstraction":"Abstraction",
               "parallelism":"Parallelism",
               "logic":"Logic",
               "sync":"Synchronization",
               "flow_control": "Flow control",
               "user_inter":"User interactivity",
               "data_rep":"Data representation",
               "dup_scripts":"Duplicate scripts",
               "sprite_naming":"Sprite naming",
               "dead_code":"Dead code",
               "attr_init":"Sprite attributes",
               "error":"Error analyzing project"}

    elif lang == "gl":
        dic = {"code":"CÓDIGO",
               "url":"URL",
               "mastery":"Mastery",
               "abstraction":"Abstracción",
               "parallelism":"Paralelismo",
               "logic":"Lóxica",
               "sync":"Sincronización",
               "flow_control": "Control de fluxo",
               "user_inter":"Interactividade do susario",
               "data_rep":"Representación dos datos",
               "dup_scripts":"Programas duplicados",
               "sprite_naming":"Nomes non axeitados",
               "dead_code":"Código morto",
               "attr_init":"Inicialización de atributos incorrecta",
               "error":"Error analizando proxecto"}

    elif lang == "pt":
        dic = {"code":"CODE",
               "url":"URL",
               "mastery":"Mastery",
               "abstraction":"Abstração",
               "parallelism":"Paralelismo",
               "logic":"Lógica",
               "sync":"Sincronização",
               "flow_control": "Controle de fluxo",
               "user_inter":"Interatividade com o usuário",
               "data_rep":"Representação de dados",
               "dup_scripts":"Scripts duplicados",
               "sprite_naming":"Nomeação de personagens",
               "dead_code":"Código morto",
               "attr_init":"Inicialização de atributos",
               "error":"Error analyzing project"}

    elif lang == "el":
        dic = {"code":"CODE",
               "url":"URL",
               "mastery":"Mastery",
               "abstraction":"Αφαίρεση",
               "parallelism":"Παραλληλισμός",
               "logic":"Λογική",
               "sync":"Συγχρονισμός",
               "flow_control": "Έλεγχος ροής",
               "user_inter":"Αλληλεπίδραση χρήστη",
               "data_rep":"Αναπαράσταση δεδομένων",
               "dup_scripts":"Διπλασιασμένα προγράμματα",
               "sprite_naming":"Ονόματα αντικειμένων",
               "dead_code":"Κώδικας που δεν εκτελείται",
               "attr_init":"Αρχικοποίηση ιδιοτήτων",
               "error":"Error analyzing project"}
    return dic
