# -*- coding: utf-8 -*-

__author__ = 'Vlademir Manoel'

"""
Agora temos todas as informações necessárias para submeter um formulário HTML simples!
"""

from urllib.parse import urljoin
from requests import get, post


def run(**kwargs):
    """
    Executa o submit de um formulário HTML
    :return:
    """
    # Precisamos formatar a URL destino
    if '8080' in kwargs.get('url'): return None

    target_url = urljoin(kwargs.get('url'), kwargs.get('details').get('action'))

    data = {}
    # breakpoint()
    for field in kwargs.get('details').get('fields'):
        """ Precisamos adicionar o atributo value aos campos,
        porém existem campos HTML que não usam value por isso precisamos verificar
        """
        common_field_types = ['text', 'search', 'hidden', 'submit']

        if field.get('type') in common_field_types:
            field['value'] = kwargs.get('payload') # para visualizar no details do scanner
            data[field.get('name')] = kwargs.get('payload')  # esse value é o parametro da função

    for textarea in kwargs.get('details').get('texts'):
        textarea['value'] = kwargs.get('payload')  # para visualizar no details do scanner
        data[textarea.get('name')] = kwargs.get('payload')

    # Precisamos saber se tem dados na nossa estrutura para serem enviados
    if data:
        # para simplificar, verificamos se é post ou get, se não for post então é get!
        if kwargs.get('details').get('http_method') == 'post':
            post(target_url, data=data, cookies=kwargs.get('cookies'))
        else:
            get(target_url, params=data, cookies=kwargs.get('cookies'))

        if kwargs.get('ajax_url'):
            return get(urljoin(kwargs.get('url'), kwargs.get('ajax_url')), cookies=kwargs.get('cookies'))
        else:
            return get(target_url, cookies=kwargs.get('cookies'))