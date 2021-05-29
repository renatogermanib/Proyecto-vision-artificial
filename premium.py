import cv2
import pytesseract
import csv
import os
import time
import pandas as pd
import xlsxwriter
import sys
import io
from openpyxl import Workbook

def ocr1(ruta_video, conexion1, conexion2): #ruta - pipe1 emisor de imágenes - pipe3 emisor de output

	salida_std = sys.stdout #creación de objeto con salida standard principal (backup para su posterior recuperación)

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
		
		if (index % 20 == 0): #acelera la ejecución, ya que solo tomará en cuenta los frames que cumplan esta condición
		
			im = video.read()[1] #lectura de imagen con [1] para su uso con tkinter
			conexion1.send(im) #traspaso de arrays por tubería

			sys.stdout = io.StringIO() #inicio captura de output
			print('analysis on process (', os.getpid(), ') -Frame -> ', index) #printea indicador de frame e ID de proceso
			out = sys.stdout.getvalue() #asignación variable con los datos output
			conexion2.send(out) #envío de output hacia proceso Main
			sys.stdout.close() #finalización de captura de output

			if (im is None): #si el arreglo contiene valor nulo
				sys.stdout = io.StringIO() #inicio captura de output
				print('traspaso de imágenes a GUI finalizado')
				out = sys.stdout.getvalue() #asignación variable con los datos output
				conexion2.send(out) #último envío de output antes de la interrupción del ciclo
				sys.stdout.close() #finalización de captura de output
				conexion1.close() #cierre de pipe emisor de imagen

			if not ret: #si ret es false
				sys.stdout = io.StringIO() #inicio captura de output
				print('no hay imagen, terminando programa... \n')
				out = sys.stdout.getvalue() #asignación variable con los datos output
				conexion2.send(out) #último envío de output antes de la interrupción del ciclo
				conexion2.send(None)
				sys.stdout.close() #cirre antes de envío
				conexion2.close() #cierre de pipe emisor de output
				break #se detiene la ejecucion en caso de no recibir mas imagen

			gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convierte a escala de grises para poder convertir a imagen binaria
			_,binary1 = cv2.threshold(gris, 80, 255, cv2.THRESH_BINARY) #binariza una imagen únicamente para extraer el dato título
			
			#print(ret) #printea valor booleano para saber si el video efectivamente se está leyendo

			#cv2.imshow('video', frame) #muestra los frames, es decir, la imagen
			#cv2.moveWindow('video', 0, 0) #desplaza ventana hacia la esquina
			
			if (index == 40): #analiza el frame 40
				
				for z in range(1, 256): #recorre cada una de las umbralizaciones utilizando la imagen binary2

					_,binary2 = cv2.threshold(gris, z, 255, cv2.THRESH_BINARY) #crea una binarización dinámica

					#EXTRACCIÓN MODELO DE NEGOCIO:
					x3, y3, h3, w3 = 150, 155, 23, 600
					ROI3 = binary2[y3:y3+h3, x3:x3+w3] #hace uso de binary2
					#cv2.imshow('roi3', ROI3)
					#cv2.moveWindow('roi3',600,600)
					aux3 = pytesseract.image_to_string(ROI3).strip() #extrae el dato modelo de negocio
					if (len(aux3) < 4): #si se cumpĺe esta condición se asignará un distractor a la variable de extracción, con el fin de evitar una comparación ambigua con la fuente, provocando que diversos valores sean válidos
						aux3 = '@@@'
					#print('modelo de negocio: ', aux3)

					#BÚSQUEDA DE DATOS:
					#modelo de negocio:
					for dato1 in l_modelos: #recorre la fuente de información
						if (aux3 == dato1): #¿la extracción es igual a algún dato de la fuente?
							modelo = dato1
							break
						elif (aux3 in dato1): #¿el dato está en la fuente? 
							modelo = dato1
						elif (dato1 in aux3): #¿la fuente está en el dato?
							modelo = dato1

			if (index == 160): #analiza el frame 160
				
				#EXTRACCIÓN TITULO: (el titulo debe estar fuera del recorrido de umbralizaciones, ya que es un dato exacto. No existe una fuente de información con todos los títulos posibles
				x1, y1, h1, w1 = 110, 110, 68, 310 #coordenadas
				ROI1 = binary1[y1:y1+h1, x1:x1+w1] #parte de eje Y + el alto(hacia abajo), sigue el eje X más el ancho (hacia la derecha). Hace uso de binary1
				#cv2.imshow('roi1', ROI1) #despliega el recorte seleccionado
				#cv2.moveWindow('roi1',200,200)
				titulo = pytesseract.image_to_string(ROI1, lang='spa').strip() #extrae el dato titulo, especificación en lenguaje español para que detecte las tildes
				#print(titulo)
				
				for x in range(1, 256): #recorre cada uno de los umbrales utilizando la imagen binary3

					_,binary3 = cv2.threshold(gris, x, 255, cv2.THRESH_BINARY) #binariza una imagen para extraer los datos proveedor, categoria, calidad y agno

					#EXTRACCIÓN PROVEEDOR:
					x2, y2, h2, w2 = 967, 135, 31, 60
					ROI2 = binary3[y2:y2+h2, x2:x2+w2] #hace uso de binary3
					#cv2.imshow('roi2', ROI2)
					#cv2.moveWindow('roi2',600,600)
					aux2 = pytesseract.image_to_string(ROI2).strip() #extrae el dato proveedor
					if (len(aux2) < 3): #define esta condición para que no tome en cuenta cadenas muy pequeñas y provoque una confusión en la búsqueda de datos
						aux2 = '@@@'
					#print('proveedor: ', aux2)
					
					#SEPARACIÓN DE DATOS:
					var = ''.join(aux2) #genera un string en base a la lista que extrae la herramienta
					separacion_p = aux2.split() #generamos otra lista con los elementos separados del string. Esos elementos se compararán con la fuente
					#print('proveedor: ', separacion_p)

					#EXTRACCIÓN CATEGORIA:
					x4, y4, h4, w4 = 150, 177, 20, 113
					ROI4 = binary3[y4:y4+h4, x4:x4+w4]
					#cv2.imshow('roi4', ROI4)
					#cv2.moveWindow('roi4',400,400)
					aux4 = pytesseract.image_to_string(ROI4).strip() #extrae el dato categoria
					if (len(aux4)  < 3): #define esta condición para que no tome en cuenta cadenas muy pequeñas y provoque una confusión en la búsqueda de datos
						aux4 = '@@@'
					#print('categoria: ', aux4)

					#EXTRACCIÓN CALIDAD:
					x5, y5, h5, w5 = 145, 203, 28, 34
					ROI5 = binary3[y5:y5+h5, x5:x5+w5] 
					#cv2.imshow('roi5', ROI5)
					#cv2.moveWindow('roi5',400,400)
					aux5 = pytesseract.image_to_string(ROI5).strip() #extrae el dato calidad
					if (aux5 == ''): #si se cumple, se asigna distracción para que no genere elementos vacíos
						aux5 = '@@@'
					#print('calidad: ', aux5)

					#EXTRACCIÓN AGNO:
					x6, y6, h6, w6 = 305, 205, 22, 41
					ROI6 = binary3[y6:y6+h6, x6:x6+w6] 
					#cv2.imshow('roi6', ROI6)
					#cv2.moveWindow('roi6',600,600)
					aux6 = pytesseract.image_to_string(ROI6).strip() #extrae el dato agno
					if (len(aux6) < 4): #condición para que solo considere años que tengan cuatro dígitos de longitud
						aux6 = '@@@'
					#print('agno: ', aux6)

					#BÚSQUEDA DE DATOS:
					#proveedores:
					for dato2 in l_proveedores: #recorre la fuente de información (lista con la columna proveedores)
						for p in separacion_p:
							if (len(p) > 4 and p == dato2): #se añade condición > 4 para que no considere datos pequeños. Para cada uno de los strings de la lista creada en "SEPARACIÓN DE DATOS"
								proveedor = dato2
								#print(True, 'condicion 1: dato valido -> ', p)
								break
							elif (len(p) > 4 and p in dato2):
								proveedor = dato2
								#print(True, 'condicion 2: dato valido -> ', p)
							elif (len(p) > 4 and dato2 in p):
								proveedor = dato2
								#print(True, 'condicion 3: dato valido -> ', p)
					

					#categorias:
					for dato3 in l_categorias: #recorre la fuente de información (lista con la columna categorías)
						if (aux4 == dato3):
							categoria = dato3.title() #title() provoca que la primera letra sea mayúscula y las demás minúsculas
							break
						elif (aux4 in dato3):
							categoria = dato3.title()
						elif (dato3 in aux4):
							categoria = dato3.title()

					#calidades:
					for dato4 in l_calidades:
						if (aux5 == dato4):
							calidad = dato4
							break
						elif (aux5 in dato4):
							calidad = dato4
						elif (dato4 in aux5):
							calidad = dato4

					#agnos:
					for dato5 in l_agnos:	
						if (aux6 == dato5):
							agno = dato5
							break
						if (aux6 in dato5):
							agno = dato5
						if (dato5 in aux6):
							agno = dato5
				
		if (cv2.waitKey(10) & 0xFF == ord('s')): #especificado en documentacion de opencv->necesario para procesadores de 64bits
			print('se ha detenido la ejecucion')
			break #si se presiona la letra S se detendra el programa

	'''
	#ESCRITURA EN DOCUMENTO EXCEL:
	extraccion = {'TÍTULO':[titulo], 'PROVEEDOR':[proveedor], 'MODELO DE NEGOCIO':[modelo], 'CATEGORÍA':[categoria], 'CALIDAD':[calidad], 'AGNO':[agno], 'PRECIO':[aux9]} #creación de diccionario con los datos extraídos
	df_extraccion = pd.DataFrame(extraccion) #creación de dataframe con el diccionario de extracción

	old_PyD = pd.read_excel('data.xlsx', sheet_name='peliculas o documentales') #lee la hoja de películas o documentales, retorna un df
	old_Series = pd.read_excel('data.xlsx', sheet_name='series') #lee la planilla de series, retorna un df

	new_PyD = old_PyD.append(df_extraccion, ignore_index=True) #genera un nuevo df, sumando el df de extracción a el viejo df

	dfs = {'peliculas o documentales': new_PyD, 'series': old_Series} #diccionario de dfs, las keys son los nombres de las hojas

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
	'''
	sys.stdout = salida_std #recuperación de salida standard principal

	print(titulo, proveedor, modelo, categoria, calidad, agno, aux9) #printeo temporal para evitar la escritura constante en excel

	#CÁLCULO TIEMPO FINAL:
	tiempo_final = (time.time()) #asignamos tiempo final
	print('\ntiempo de ejecución premium: ', ("{0:.2f}".format(tiempo_final - tiempo_inicial)), 'seg.') #calcula y printea el tiempo total de ejecucion

	video.release()#cierre de video
	cv2.destroyAllWindows() #cierre de todas las ventanas OpenCV que hayan podido quedar abiertas

if __name__ == '__main__':

	None #variable nula para evitar unexpected EOF 
	#ocr('/home/viruta/Desktop/Archivos/PROGRAMA/Premium/ThisIsUs_Video.mp4')
	#ocr('/home/viruta/Desktop/Archivos/PROGRAMA/Premium/PlanetaHostil_Video.mp4')
	#ocr('/home/viruta/Desktop/Archivos/PROGRAMA/Premium/GuerrillaDelOro_Video.mp4')
	