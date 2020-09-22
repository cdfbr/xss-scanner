# -*- coding: utf-8 -*-

__author__ = 'Vlademir Manoel'

from requests import get
from bs4 import BeautifulSoup
import scanner


def main():
    """ Função principal da aplicação """
    """A ideia é ver em uma página onde tem formulários para que a gente possa explorar eles, então
    vamos capturar todos os formulários em uma página."""
    url = input(f'Informe a URL que deseja escanear: ')
    auth = input(f'Precisa de autênticação (y/n): ')
    cookies = {}

    if auth == 'y':
        cookies['PHPSESSID'] = input('PHPSESSID: ') # Informe a URL que deseja escanear: 7vasai2mkrbk70qbs8611c5iq1
        cookies['security'] = 'low'

    forms = BeautifulSoup(get(url, cookies=cookies).content, 'html.parser').find_all('form')
    # Forms é uma lista com todos os formulários da url
    if forms:
        scanner.run(forms, url, cookies)
    else:
        print(f'Em {url} não possui formulário!')


if __name__ == '__main__':  # Se for executado diretamente
    main()
