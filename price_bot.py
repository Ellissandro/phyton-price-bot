import requests
from bs4 import BeautifulSoup
import telegram
import os
from dotenv import load_dotenv

load_dotenv()
async def send_telegram_message(chat_id, message):
    bot_token = os.getenv("BOT_TOKEN")
    bot = telegram.Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)

async def get_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    price_element = soup.find('p', attrs={'data-testid': 'price-value'})
    name_element = soup.find('h1', attrs={'data-testid': 'heading-product-title'})
    if price_element and name_element:
        price = price_element.get_text().strip()
        name = name_element.get_text().strip()
        return name, price
    else:
        return None, None

async def main():
    chat_id = os.getenv("CHAT_ID")
    url = os.getenv("URL")
    name, price = await get_product_details(url)

    if name and price:
        message = f"O produto {name} está com o preço {price}"
    else:
        message = "Não foi possível obter as informações do produto."

    await send_telegram_message(chat_id, message)

import asyncio
asyncio.run(main())
