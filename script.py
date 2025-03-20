import asyncio
import os
from bs4 import BeautifulSoup
import requests
from telegram import Bot
from telegram.constants import ParseMode
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = '7803564666:AAEIeVRn_zzdiumVg89RB12xGczBv1mksaU' 
GROUP_ID = '-1002630091079' 
bot = Bot(token=TOKEN)
group_id = GROUP_ID  

async def enviar_vaga():
    url = "https://www.fiotec.fiocruz.br/vagas-projetos/todas"
    response = requests.get(url, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        hoje = "2025-02-20"
        tr_elements = soup.find_all(class_="col-md-6 col-xs-12")

        vagas_filtradas = []  
        for tr in tr_elements:
            titulo_vaga = tr.get_text(" ", strip=True).split("Publicado:")[0].strip()

            published_times = tr.find_all("time")
            
            for time in published_times:
                data_publicacao = time.get("datetime", "")[:10]  
                
                if data_publicacao == hoje:
                    vaga_info = f"Título: {titulo_vaga} - Data de Publicação: {time.text.strip()}"
                    
                    
                    if group_id:
                        try:
                            await bot.send_message(chat_id=GROUP_ID, text=vaga_info, parse_mode=ParseMode.MARKDOWN)
                            print(f'Mensagem enviada com sucesso para o grupo!')
                        except Exception as e:
                            print(f'Erro ao enviar mensagem: {e}')
                    else:
                        print("GROUP_ID não encontrado no ambiente.")
                    
                    vagas_filtradas.append(vaga_info)
                        
        return vagas_filtradas

vagas = asyncio.run(enviar_vaga())
print(vagas)
