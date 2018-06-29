#IMPORTACOES

#importa biblioteca para acessar a API do google spreadsheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#importa bibliteca para imprimir dados de forma mais organizada
import pprint
#importa biblioteca para obter horario atual
from datetime import datetime
#importa a biblioteca para tratar a serial da Raspberry, neste caso o Bluetooth
import serial
import numpy as np
#importa a biblioteca para usar o sleep
import time

ser = serial.Serial('/dev/rfcomm0', 9600)
print ("Waiting for data...")

#what is a scope ?
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#credencial
creds = ServiceAccountCredentials.from_json_keyfile_name('entradaSecret.json',scope)

client = gspread.authorize(creds)

sheet = client.open('Controle Entrada FEGRobotica').sheet1

pp = pprint.PrettyPrinter()

def convert(s):
	
	#initialization of the string to ""
	new = ""
	
	#transform into string
	for x in s:
		new+=x
		
	#return string
	return new
	

while(True):
	
	membro = ['','','','','','','','','','','']
	nome = ""
	charEnviado = ''
	#Verifica se a serial esta pronta para receber um dado
	if(ser.inWaiting() > 0):
		#Faz laco para ler a palavra inteira
		for i in range(0,11):
			membro[i] = ser.read()
		if convert(membro) == "17 B7 EC 94":
			nome = "Paulinha"
			charEnviado = 'a'
		elif convert(membro) == "23 65 F9 25":
			nome = "Silas"
			charEnviado = 'a'
		elif convert(membro) == "FD B9 4B 73":
			nome = "Noemi"
			charEnviado = 'a'
		elif convert(membro) == "31 D2 DA 0E":
			nome =  "Leticia"
			charEnviado = 'a'
		else:
			nome = "Nao Autorizado"
			charEnviado = 'b'
			
		row = [str(datetime.now()),nome]
		sheet.insert_row(row,2)
		time.sleep(2)
		ser.write(charEnviado)
		ser.write(charEnviado)
		ser.write(charEnviado)
		ser.write(charEnviado)
		ser.write(charEnviado)
		

#CODIGO

#pega uma linha desejada
#entrada = sheet.row_values(6)

#pega uma coluna desejada 
#entradas = sheet.col_values(2)

#pega uma celula desejada
#entradas = sheet.cell(2,2).value

#alterar um valor
#sheet.update_cell(2,2,'Silas')

#entradas = sheet.cell(2,2).value

#pp.pprint(entradas)

#adicionando uma linha nova
#row = [str(datetime.now()),"Rod"]
#index = 8
#sheet.insert_row(row,sheet.row_count)

#sheet.delete_row(3)

#print(datetime.now())


