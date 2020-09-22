# -*- coding: utf-8 -*-

__author__ = 'Vlademir Manoel'

import extractor
import submit


def run(forms, url, cookies):
    """
    Itera todos os formulários preenchendo os campos com nossos payloads.
    Se payload for injetado e executado com êxito, significa que a página é vulnerável ao XSS.
    :param forms: Lista de formulários que existem na URL
    :param url: URL alvo que irá servir como base para join com atributo action de formulários
    :param cookies: Informações para auxiliar em caso de acesso restrito
    :return: Flag informando se é ou não vulnerável ao XSS
    """
    ajax_url = input('Informe a URL que está sendo enviada as informações via AJAX se existir: ')

    file_payloads = open("payloads.txt", "r")
    # Carregamos nosso arquivo que possui nossos payloads e para cada payload vamos fazer o teste
    payloads = file_payloads.readlines()
    # Transformamos as linhas do nosso arquivo em lista, para facilitar no loop
    for payload in payloads:
        for form in forms:
            details = extractor.run(form)  # details do formulário
            js = ' '.join(payload.split())
            # breakpoint()
            response = submit.run(details=details, url=url, payload=js, ajax_url=ajax_url, cookies=cookies)
            # breakpoint()  # c2205pegoq1lqetqsnts7o0t06
            if response:
                if payload in response.content.decode():
                    print('--- Formulário Vulnerável ---')
                    print(form)
                    print('--- Payload Executado ---')
                    print(payload)

    file_payloads.close()
