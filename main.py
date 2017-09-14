import requests
from bs4 import BeautifulSoup
import json

process_number = '0714317-35.2017.8.02.0001'

url = "https://www2.tjal.jus.br/cpopg/open.do"
search_url = "https://www2.tjal.jus.br/cpopg/search.do?conversationId=&dadosConsulta.localPesquisa.cdLocal=-1&cbPesquisa=NUMPROC&dadosConsulta.tipoNuProcesso=SAJ&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.valorConsultaNuUnificado=&dadosConsulta.valorConsulta=" + process_number + "&uuidCaptcha="

session = requests.session()
session.get(url)
response = session.get(search_url)
print(response)
soup = BeautifulSoup(response.content, "html.parser")

def get_data(name):
    tr_list = soup.select("table.secaoFormBody tr")
    for tr in tr_list:
        td = tr.find('td')
        if td.text.strip() == name:
            return td.find_next_sibling('td').text.strip()

process = get_data('Processo:')
classe = get_data('Classe:')
subject = get_data('Assunto:')
distribuition = get_data('Distribuição:')
control = get_data('Controle:')
judge = get_data('Juiz:')
action_value = get_data('Valor da ação:')

process_data = {}
process_data['processo'] = process
process_data['classe'] = classe
process_data['assunto'] = subject
process_data['distribuicao'] = distribuition
process_data['controle'] = control
process_data['juiz'] = judge
process_data['valor_acao'] = action_value

moviments = []
movements_elements = soup.select("table#tabelaUltimasMovimentacoes tr")
for element in movements_elements:
    td = element.select('td')
    moviment = {}
    moviment['data'] = td[0].text.strip()
    moviment['information'] = td[2].text.strip()
    moviments.append(moviment)

data = {}
data['dados_processo'] = process_data
data['movimentacoes'] = moviments

file_name = process_number + '.json'
with open(file_name, 'w') as f:
    f.write(json.dumps(data, indent=4,
                       sort_keys=True,
                       ensure_ascii=False))
