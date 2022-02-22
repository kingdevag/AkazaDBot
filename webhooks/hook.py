#Imports
import os
#From-Import
from dhooks import Webhook, Embed
from dotenv import load_dotenv

load_dotenv()

hook = Webhook(os.environ['hook'])

embed = Embed(
    description='Hola Soy El Web Hook de Akaza',
    color=0x5CDBF0,
    timestamp='now'
    )

image1 = 'https://imgur.com/o2pEUWY.png'
image2 = 'https://imgur.com/3mDvF2r.png'

author = input("Introduce el Autor: ")
data = input("Introduce el Mensaje: ")

embed.set_author(name='Akaza', icon_url=image1)
embed.add_field(name=f'{author} Dice:', value=data)
embed.add_field(name='', value='@everyone')
embed.set_footer(text='Agregame a tu servidor :)', icon_url=image1)

embed.set_timestamp()
embed.set_image(image2)

hook.send(embed=embed)