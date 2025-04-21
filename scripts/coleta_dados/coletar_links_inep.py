# scripts/coleta_dados/coletar_links_inep.py
# Este script coleta os links dos microdados do Censo da Educação Superior do site do INEP (1995-2023).

import requests
from bs4 import BeautifulSoup

def coletar_links_inep(url_base, palavra_chave):
    """
    Coleta os links dos microdados do Censo da Educação Superior do INEP.
    
    :param url_base: URL da página do INEP com os dados.
    :param palavra_chave: Palavra-chave que identifica os links desejados.
    :return: Dicionário com os anos e os links dos microdados.
    """
    resposta = requests.get(url_base)
    if resposta.status_code != 200:
        raise Exception(f"Erro ao acessar {url_base}: {resposta.status_code}")

    soup = BeautifulSoup(resposta.content, 'html.parser')
    links = soup.find_all('a', href=True)
    
    urls = {}
    for link in links:
        href = link['href']
        if palavra_chave in href:
            # Extrai o ano do link e cria a entrada no dicionário
            for ano in range(1995, 2024):
                if str(ano) in href:
                    urls[f"INEP_{ano}-MICRODADOS-CENSO"] = href
                    break
    return urls

def salvar_links_em_arquivo(urls, caminho_arquivo):
    """
    Salva os links em um arquivo de texto no formato especificado.
    
    :param urls: Dicionário com os links e descrições.
    :param caminho_arquivo: Caminho do arquivo onde os links serão salvos.
    """
    with open(caminho_arquivo, 'w') as arquivo:
        for chave, url in urls.items():
            arquivo.write(f"{chave}: {url}\n")
    print(f"Links salvos em {caminho_arquivo}")

def main():
    url_base = "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior"
    palavra_chave = "microdados_censo_da_educacao_superior"
    caminho_arquivo = "./dados/bruto/lista-links.txt"

    print("Coletando links do INEP...")
    urls = coletar_links_inep(url_base, palavra_chave)
    salvar_links_em_arquivo(urls, caminho_arquivo)
    print("Processo concluído.")

if __name__ == '__main__':
    main()