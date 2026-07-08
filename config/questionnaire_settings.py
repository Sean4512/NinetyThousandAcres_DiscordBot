# -*- coding: utf-8 -*-
"""
@File    : questionnaire_settings.py
@Time    : 2026/6/16 下午 03:30
@Author  : Sean
@Project : NinetyThousandAcres_DiscordBot
@Desc    : 
"""

from config.settings import get_nta_settings
from utils import questionnaire_field
from utils.Types.questionnaire import Questionnaire


G_PLAYER_REGISTER_QUESTIONNAIRE: Questionnaire = questionnaire_field.load_questionnaire_fields_from_yaml(
    get_nta_settings().PLAYER_REGISTER_FIELDS_YAML_PATH
)
G_PLAYER_REGISTER_QUESTIONNAIRE.steps = questionnaire_field.build_questionnaire_steps(
    G_PLAYER_REGISTER_QUESTIONNAIRE.fields
)

def get_player_register_questionnaire():
    return G_PLAYER_REGISTER_QUESTIONNAIRE



G_MATCH_SIGNUP_QUESTIONNAIRE: Questionnaire = questionnaire_field.load_questionnaire_fields_from_yaml(
    get_nta_settings().MATCH_SIGNUP_FIELDS_YAML_PATH
)
G_MATCH_SIGNUP_QUESTIONNAIRE.steps = questionnaire_field.build_questionnaire_steps(
    G_MATCH_SIGNUP_QUESTIONNAIRE.fields
)
def get_match_signup_questionnaire():
    return G_MATCH_SIGNUP_QUESTIONNAIRE



G_CREATE_MATCH_SIGNUP_QUESTIONNAIRE: Questionnaire = questionnaire_field.load_questionnaire_fields_from_yaml(
    get_nta_settings().CREATE_MATCH_SIGNUP_FIELDS_YAML_PATH
)
G_CREATE_MATCH_SIGNUP_QUESTIONNAIRE.steps = questionnaire_field.build_questionnaire_steps(
    G_CREATE_MATCH_SIGNUP_QUESTIONNAIRE.fields
)
def get_create_match_signup_questionnaire():
    return G_CREATE_MATCH_SIGNUP_QUESTIONNAIRE










