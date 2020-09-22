# -*- coding: utf-8 -*-

__author__ = 'Vlademir Manoel'

"""
Agora que a gente tem todos os formulários da nossa página, vamos tentar
pegar mais informações sobre cada um dos formulários.
"""


def run(form):
    """
    Extrai informações importantes para ajudar na toamda de decisão ao submeter o formulário
    :param form: Formulário que desejamos extrair informações
    :return: Lista com todas informações sobre o formulário.
    """

    data = {
        'action': form.attrs.get('action'),
        'http_method': form.attrs.get('method', 'get'),
        'fields': [],
        'texts': []
    }

    for field in form.find_all('input'):
        field_name = field.attrs.get('name')
        field_type = field.attrs.get('type', 'text')

        data['fields'].append({'name': field_name, 'type': field_type})

    for textarea in form.find_all('textarea'):
        textarea_name = textarea.attrs.get('name')
        data['texts'].append({'name': textarea_name})

    return data
