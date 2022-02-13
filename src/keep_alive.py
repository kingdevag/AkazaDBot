from colorama import Fore
from colorama import Style
from flask import Flask
from threading import Thread
 
app = Flask('')
 
@app.route('/')
def main():
    return "Bot Xd"
  
def run():
  app.run(host="0.0.0.0", port=8101)
 
def keep_alive():
    server = Thread(target=run)
    server.start()
    print(Fore.GREEN + "--------------- ONLINE ---------------" + Style.RESET_ALL)