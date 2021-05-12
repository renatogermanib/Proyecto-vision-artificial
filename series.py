import cv2
import pytesseract
import csv
import os
import time
import pandas as pd
import xlsxwriter
from openpyxl import Workbook

def ocr(ruta_video):

	tiempo_inicial = time.time()

	l = [] #genera lista vacía

	l1, l2, l3, l4, l5, l6, l7 = [], [], [], [], [], [], [] #listas para almacenar cada columna de cada dato de la fuente

	with open('/home/viruta/Desktop/Archivos/PROGRAMA/fuente.csv') as archivo: #abre el csv como "archivo"
		lector = csv.reader(archivo) #creación de objeto encargado de leer el csv
		for fila in lector: 
			l.append(fila) #creación de lista con todos los datos del documento csv

	tamagno = len(l) #longitud de las columnas, se utilizará para recorrer las columnas completas

	for x in range(1,tamagno): #comienza desde la primera para no tomar en cuenta la cabecera
		l1.append((l[x][0])) #recorre las filas especificando solo una columna a la vez, para luego añadir estos datos a las listas creadas
		l2.append((l[x][1]))
		l3.append((l[x][2]))
		l4.append((l[x][3]))
		l5.append((l[x][4]))
		l6.append((l[x][5]))
		l7.append((l[x][6]))
	
	#ELIMINAR DATOS VACÍOS EN LISTAS:
	l_proveedores = list(filter(bool, l1)) #se crean nuevas listas sin datos vacíos
	l_modelos = list(filter(bool, l2))
	l_categorias = list(filter(bool, l3))
	l_calidades = list(filter(bool, l4))
	l_agnos = list(filter(bool, l5))
	l_temporadas = list(filter(bool, l6))
	l_episodios = list(filter(bool, l7))

	aux2, aux3, aux4, aux5, aux6, aux7, aux8, aux9 = ('', '', '', '', '', '', '', '') #variables auxiliar
	
	index = 0 #contador para referenciar el número de frame de la ejecución

	video = cv2.VideoCapture(ruta_video) #abre video

	while (video.isOpened()): #mientras el video este abierto
		ret, frame = video.read() #leer video, ret= True o False. frame=imagen en si misma
		index += 1 #incrementa contador para hacer referencia al número de frame

		if not ret: #si ret es False
			print('no hay imagen, terminando programa...')
			break #se detiene la ejecución en caso de no recibir más imagen

		if (index % 20 == 0): #acelera la ejecución, ya que solo tomará en cuenta los frames que cumplan esta condición
		
			print('analysis on process (', os.getpid(), ') -Frame -> ', index) #printea indicador de frame e ID de proceso

			gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convierte a escala de grises
			
			#print(ret) #printea valor booleano para saber si el video efectivamente se está leyendo

			#cv2.imshow('video', frame) #muestra los frames, es decir, el video
			#cv2.moveWindow('video',0,0) #desplaza ventana hacia la esquina
			
			if (index == 140): #analiza el frame 140

				_,binary1 = cv2.threshold(gris, 90, 255, cv2.THRESH_BINARY) #convierte a imagen binaria para extraer el dato título

				#EXTRACCIÓN TITULO:
				x1, y1, h1, w1 = 145, 138, 36, 450
				ROI1 = binary1[y1:y1+h1, x1:x1+w1]
				#cv2.imshow('roi1', ROI1)
				#cv2.moveWindow('roi1',200,200)
				titulo = pytesseract.image_to_string(ROI1).strip() #extraemos el titulo
				#print(titulo)
				
				for x in range(1, 256): #recorre cada uno de los umbrales

					_,binary2 = cv2.threshold(gris, x, 255, cv2.THRESH_BINARY) #crea imagen binaria dinamica

					#EXTRACCIÓN CATEGORIA:
					x4, y4, h4, w4 = 150, 177, 20, 300
					ROI4 = binary2[y4:y4+h4, x4:x4+w4]
					#cv2.imshow('roi4', ROI4)
					#cv2.moveWindow('roi4',400,400)
					aux4 = pytesseract.image_to_string(ROI4, lang='spa').strip() #extrae el dato categoria, especificación idioma español para que detecte tildes
					if (len(aux4) < 3): #si se cumpĺe esta condición se asignará un distractor a la variable de extracción, con el fin de evitar una comparación ambigua con la fuente, provocando que diversos valores sean válidos
						aux4 = '@@@'
					#print('categoria: ', aux4)

					#EXTRACCIÓN CALIDAD:
					x5, y5, h5, w5 = 145, 203, 28, 34
					ROI5 = binary2[y5:y5+h5, x5:x5+w5] 
					#cv2.imshow('roi5', ROI5)
					#cv2.moveWindow('roi5',400,400)
					aux5 = pytesseract.image_to_string(ROI5).strip() #extrae el dato calidad
					if (aux5 == ''):
						aux5 = '@@@'
					#print('calidad: ', aux5)

					#EXTRACCIÓN AGNO:
					x6, y6, h6, w6 = 305, 205, 22, 55
					ROI6 = binary2[y6:y6+h6, x6:x6+w6] 
					#cv2.imshow('roi6', ROI6)
					#cv2.moveWindow('roi6',600,600)
					aux6 = pytesseract.image_to_string(ROI6).strip() #extrae el dato agno
					if (len(aux6) < 4):
						aux6 = '@@@'
					#print('agno: ', aux4)

					#BÚSQUEDA DE DATOS:
					#modelo de negocio:
					if (len(aux3) == 0): #si modelo de negocio esta vacio se asume que es gratiuito
						modelo = 'Gratis'

					#categorias:
					for dato1 in l_categorias: #recorre la fuente de información
						if (aux4 == dato1):
							categoria = dato1.title()
							break
						elif (aux4 in dato1):
							categoria = dato1.title()
							#print(categoria)
						elif (dato1 in aux4):
							categoria = dato1.title()
							#print(categoria)

					#calidades:
					for dato2 in l_calidades:
						if (aux5 == dato2):
							calidad = dato2
							break
						elif (aux5 in dato2):
							calidad = dato2
						elif (dato2 in aux5):
							calidad = dato2

					#agnos:
					for dato3 in l_agnos:
						if (aux6 == dato3):
							agno = dato3
							break
						elif (aux6 in dato3):
							agno = dato3
						elif (dato3 in aux6):
							agno = dato3
							#print(agno)
			
			if (index == 440): #analiza el frame 440
				
				for z in range(1, 256): #recorre cada uno de los umbrales

					_,binary3 = cv2.threshold(gris, z, 255, cv2.THRESH_BINARY) #crea imagen binaria dinamica

					#EXTRACCIÓN TEMPORADAS:
					x7, y7, h7, w7 = 375, 238, 28, 107
					ROI7 = binary3[y7:y7+h7, x7:x7+w7] 
					#cv2.imshow('roi7', ROI7)
					#cv2.moveWindow('roi7',600,600)
					aux7 = pytesseract.image_to_string(ROI7).strip() #extrae el dato temporadas
					if (len(aux7) < 9):
						aux7 = '@@@'
					#print('temporadas: ', aux7)

					#EXTRACCIÓN EPISODIOS:
					x8, y8, h8, w8 = 725, 170, 50, 110
					ROI8 = binary3[y8:y8+h8, x8:x8+w8] 
					#cv2.imshow('roi8', ROI8)
					#cv2.moveWindow('roi8',600,600)
					aux8 = pytesseract.image_to_string(ROI8).strip() #extrae el dato episodios
					if (aux8 == ''):
						aux8 = '@@@'
					#print('episodios: ', aux8)

					#BÚSQUEDA DE DATOS:
					#temporadas:
					for dato4 in l_temporadas: #recorre la fuente de información
						if (aux7 == dato4):
							temporadas = dato4
							break
						elif (aux7 in dato4):
							temporadas = dato4
						elif (dato4 in aux7):
							temporadas = dato4

					#episodios:
					for dato5 in l_episodios:	
						if (aux8 == dato5):
							episodios = dato5
							break
						elif (aux8 in dato5):
							episodios = dato5
						elif (dato5 in aux8):
							episodios = dato5
				
		if (cv2.waitKey(10) & 0xFF == ord('s')): #especificado en documentacion de opencv->necesario para procesadores de 64bits
			print('se ha detenido la ejecucion')
			break #si se presiona la letra S se detendra el programa
	

	#ESCRITURA EN DOCUMENTO EXCEL:
	extraccion = {'TÍTULO':[titulo], 'PROVEEDOR':[aux2], 'MODELO DE NEGOCIO':[modelo], 'CATEGORÍA':[categoria], 'CALIDAD':[calidad], 'AGNO':[agno], 'TEMPORADAS':[temporadas], 'EPISODIOS':[episodios]} #creación de diccionario con los datos extraídos
	df_extraccion = pd.DataFrame(extraccion) #creación de dataframe con el diccionario de extracción

	old_PyD = pd.read_excel('data.xlsx', sheet_name='peliculas o documentales') #lee la hoja de películas o documentales, retorna un df
	old_Series = pd.read_excel('data.xlsx', sheet_name='series') #lee la planilla de series, retorna un df

	new_Series = old_Series.append(df_extraccion, ignore_index=True) #genera un nuevo df, sumando el df de extracción a el viejo df

	dfs = {'peliculas o documentales': old_PyD, 'series': new_Series} #diccionario de dfs, las keys son los nombres de las hojas

	writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter') #objeto de escritura para documentos excel

	for hoja in dfs.keys(): #recorre las keys del diccionario de dfs
		dfs[hoja].to_excel(writer, sheet_name=hoja, index=False) #sobreescribe df y el nombre correspondiente de la hoja

	workbook = writer.book #creación de objeto
	worksheet1 = writer.sheets['peliculas o documentales'] #para la primera hoja
	worksheet2 = writer.sheets['series'] #para la segunda hoja
	formato = workbook.add_format({'num_format': '@'}) #declaración de formato string mediante @

	worksheet1.set_column('A:L', 20, formato) #establece formato -> columna A hasta la L, con un ancho de 20 por casilla
	worksheet2.set_column('A:L', 20, formato)
	writer.save() #guarda

	#CÁLCULO TIEMPO FINAL:
	tiempo_final = (time.time()) #asignamos tiempo final
	print('\ntiempo de ejecución series: ', ("{0:.2f}".format(tiempo_final - tiempo_inicial)), 'seg.') #calculamos y printiamos el tiempo total de ejecucion

	video.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':

	None #variable nula para evitar unexpected EOF
	#ocr('/home/viruta/Desktop/Archivos/PROGRAMA/Series/MyBrilliantFriend_Video.mp4')
	#ocr('/home/viruta/Desktop/Archivos/PROGRAMA/Series/TheOutsider_Video.mp4')
	#ocr('/home/viruta/Desktop/Archivos/PROGRAMA/Series/Chernobyl_Video.mp4')
	