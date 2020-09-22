# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     x3scanner
   Description : Arquivo principal do projeto
   Author :       Vlademir Manoel
   date：          20/09/2020
-------------------------------------------------
"""
__author__ = 'Vlademir Manoel'

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


"""
Agora que a gente tem todos os formulários da nossa página, vamos tentar
pegar mais informações sobre os formulários.

Vamos criar uma função para extrair informações importantes para ajudar a gente a submeter o formulário
"""


def form_infos(form):
    """
    Retorna todas as informações importantes em um formulário
    :param form: Formulário que queremos extrair informações
    :return: Lista com as informações extraidas do formulário
    :raises KeyError: Se atributo não existir
    """

    # Pegamos o endereço que os dados serão enviados quando submeter o formulário.
    # Pegamos qual verbo/método HTTP que a url alvo está esperando receber
    attributes_and_fields = {
        'action': form.attrs.get('action', '/').lower(),
        'http_method': form.attrs.get('method', 'get'),
        'fields': []
    }

    for field in form.find_all('input'):  # retorna uma lista com todos os campos
        field_name = field.attrs.get('name')
        field_type = field.attrs.get('type', 'text')  # Como não tem então eu sei que é text
        # colocamos dentro da nossa lista de campos para trabalhar posteriormente
        attributes_and_fields['fields'].append({"name": field_name, "type": field_type})

    return attributes_and_fields


"""
Já temos todas as informações necessárias para submeter um formulário HTML simples!
Vamos criar uma função para submeter o formulário.
"""


def submit(form_infos, url, value):
    """
    Submete formulários HTML dado as informações necessárias para tal.
    :param form_infos: Dicionário com informações necessárias para submeter um formulário
    :param url: Página que possui o formulario
    :param value: Será nosso Payload (código malicioso que executa uma ação destrutiva no alvo)
    :return: Resposta HTTP
    """
    # Precisamos formatar a URL alvo
    target_url = urljoin(url, form_infos['action'])
    # Precisamos dos campos para preencher(colocar valores/payload)
    fields = form_infos['fields']
    # Precisamos de uma estrutura de dados para fazer a requisição para url alvo
    data_structure = {}

    for field in fields:
        """ Precisamos adicionar o atributo value aos campos,
        porém existem campos HTML que não usam value por isso precisamos verificar
        """
        if field.get('type') == 'text' or field.get('type') == 'search':
            field['value'] = value
            data_structure[field.get('name')] = value # esse value é o parametro da função
    # Precisamos saber se tem dados na nossa estrutura para serem enviados
    if data_structure:
        # para simplificar, verificamos se é post ou get, se não for post então é get!
        data = {
            'txtName': value,
            'mtxMessage': value,
            'btnSign': 'ok'
        }
        cookies = {
            'PHPSESSID': '7vasai2mkrbk70qbs8611c5iq1',
            'security': 'low'
        }

        if form_infos.get('http_method') == 'post':
            requests.post('http://localhost/vulnerabilities/xss_s/', data=data, cookies=cookies)
        else:
            requests.get(target_url, params=data_structure)
        return requests.get('http://localhost/vulnerabilities/xss_s/')


"""
Agora vamos criar nossa função que será a cereja do bolo, ela que vai rodar o scanner em si.

Aqui está o que a função faz:
Dado um URL, ele pega todos os formulários HTML e, em seguida, imprime o número de formulários detectados.
Em seguida, itera todos os formulários e os envia com a inserção do valor de todos os campos de texto e de entrada de
pesquisa com um código Javascript. Se o código Javscript for injetado e executado com êxito,
isso é um sinal claro de que a página da web é vulnerável ao XSS.
"""


def scanner(forms, page):
    """
    Verifica se os formulários encontrados na página é vulnerável a XSS
    :param forms: Formulários encontrados na página
    :param page: Página alvo que possui formulários
    """
    # Vamos carregar nosso arquivo que possui nossos payloads e para cada payload vamos fazer o teste
    file_payloads = open("payloads.txt", "r")
    payloads = file_payloads.readlines()

    # para cada payload
    for payload in payloads:
        # para cada formulário
        for form in forms:
            infos = form_infos(form)  # informações do formulário
            # Tirar espaços/tabs/novas linhas (\n)
            js = ' '.join(payload.split())
            response = submit(infos, page, js)
            # enviamos as informações do formulário acrescentando nosso payload
            breakpoint()
            if payload in response.content.decode():
                print(f'[+] Vulnerável!!!')
                print(f'[*] Informações: ')
                print(infos)
    file_payloads.close()


def main():
    """ Função principal da aplicação """
    """
        A ideia é ver em uma página onde tem formulários para que a gente possa explorar eles, então
        vamos capturar todos os formulários em uma página.
        """
    page = input('Informe a página que deseja escanear: ')
    forms = BeautifulSoup(requests.get(page).content, 'html.parser').find_all('form')
    # html.parser define que desejo que seja feita analise como html
    # Classe bs4.element.ResultSet Um ResultSet é apenas uma lista que guarda o que extrai do html da página
    if forms:
        print(f'[+] Foram encontrados {len(forms)} formulários na página {page}')
        scanner(forms, page)
    else:
        print(f'A página {page} não possui formulário!')


if __name__ == '__main__':  # Se for executado diretamente
    main()
