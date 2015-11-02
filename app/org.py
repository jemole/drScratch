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

    elif lang == "pt":
        dic = {"code":"CODE",
               "url":"URL",
               "mastery":"Mastery",
               "abstraction":"Abstracció",
               "parallelism":"Parallelism",
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
    return dic
