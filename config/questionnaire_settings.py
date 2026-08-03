# -*- coding: utf-8 -*-
"""
@File    : questionnaire_settings.py
@Time    : 2026/6/19 下午 09:27
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from typing import Optional

from config.settings import get_nta_settings
from utils import questionnaire_field
from utils.models.questionnaire import Questionnaire


G_PLAYER_REGISTER_QUESTIONNAIRE: Optional[Questionnaire] = None
G_MATCH_SIGNUP_QUESTIONNAIRE: Optional[Questionnaire] = None
G_MATCH_SIGNUP_CREATION_QUESTIONNAIRE: Optional[Questionnaire] = None

def get_player_register_questionnaire():
    global G_PLAYER_REGISTER_QUESTIONNAIRE
    if G_PLAYER_REGISTER_QUESTIONNAIRE is None:
        raise ValueError("Player register questionnaire not initialized")
    return G_PLAYER_REGISTER_QUESTIONNAIRE

def get_match_signup_questionnaire():
    global G_MATCH_SIGNUP_QUESTIONNAIRE
    if G_MATCH_SIGNUP_QUESTIONNAIRE is None:
        raise ValueError("Match signup questionnaire not initialized")
    return G_MATCH_SIGNUP_QUESTIONNAIRE

def get_match_signup_creation_questionnaire():
    global G_MATCH_SIGNUP_CREATION_QUESTIONNAIRE
    if G_MATCH_SIGNUP_CREATION_QUESTIONNAIRE is None:
        raise ValueError("Create match signup questionnaire not initialized")
    return G_MATCH_SIGNUP_CREATION_QUESTIONNAIRE

def setup_player_register_questionnaire():
    global G_PLAYER_REGISTER_QUESTIONNAIRE
    G_PLAYER_REGISTER_QUESTIONNAIRE = questionnaire_field.load_questionnaire_fields_from_yaml(
        get_nta_settings().PLAYER_REGISTER_FIELDS_YAML_PATH
    )
    if G_PLAYER_REGISTER_QUESTIONNAIRE is None:
        raise ValueError("Player register questionnaire not initialized")
    G_PLAYER_REGISTER_QUESTIONNAIRE.steps = questionnaire_field.build_questionnaire_steps(
        G_PLAYER_REGISTER_QUESTIONNAIRE.fields
    )

def setup_match_signup_questionnaire():
    global G_MATCH_SIGNUP_QUESTIONNAIRE
    G_MATCH_SIGNUP_QUESTIONNAIRE = questionnaire_field.load_questionnaire_fields_from_yaml(
        get_nta_settings().MATCH_SIGNUP_REGISTRATION_FIELDS_YAML_PATH
    )
    if G_MATCH_SIGNUP_QUESTIONNAIRE is None:
        raise ValueError("Match signup questionnaire not initialized")
    G_MATCH_SIGNUP_QUESTIONNAIRE.steps = questionnaire_field.build_questionnaire_steps(
        G_MATCH_SIGNUP_QUESTIONNAIRE.fields
    )

def setup_match_signup_creation_questionnaire():
    global G_MATCH_SIGNUP_CREATION_QUESTIONNAIRE
    G_MATCH_SIGNUP_CREATION_QUESTIONNAIRE = questionnaire_field.load_questionnaire_fields_from_yaml(
        get_nta_settings().MATCH_SIGNUP_CREATION_FIELDS_YAML_PATH
    )
    if G_MATCH_SIGNUP_CREATION_QUESTIONNAIRE is None:
        raise ValueError("Match signup creation questionnaire not initialized")
    G_MATCH_SIGNUP_CREATION_QUESTIONNAIRE.steps = questionnaire_field.build_questionnaire_steps(
        G_MATCH_SIGNUP_CREATION_QUESTIONNAIRE.fields
    )

def setup_all_questionnaires():
    setup_player_register_questionnaire()
    setup_match_signup_questionnaire()
    setup_match_signup_creation_questionnaire()


