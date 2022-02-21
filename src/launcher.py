#Imports
import os

#From-Import
from colorama import Fore
from colorama import Style

rute = os.getcwd()

def printconsole():
    print(f"{Fore.BLUE} Trabajando desde: {rute} {Style.RESET_ALL}")

def modules_py():
    for file in os.listdir('src/modules'):
        if file.endswith('.py'):
            print(f"{Fore.WHITE} {file} {Style.RESET_ALL} {Fore.GREEN} Successfully Uploaded {Style.RESET_ALL}")
            
            
printconsole()
modules_py()
