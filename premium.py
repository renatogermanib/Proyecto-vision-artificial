import cv2
import pytesseract
import csv
import os
import time

def ocr(ruta_video):

	#tiempo_inicial = time.time()

	l = [] #genera lista vacía

	l1, l2, l3, l4, l5, l6, l7 = [], [], [], [], [], [], [] #listas para almacenar las columnas de cada dato

	with open('/home/viruta/Desktop/Archivos/PROGRAMA/fuente.csv') as archivo: #abre el csv como "archivo"
		lector = csv.reader(archivo) #creación de objeto encargado de leer el csv
		for fila in lector: 
			l.append(fila) #creación de lista con todos los datos del documento csv

	tamagno = len(l) #longitud de las columnas, se utilizará para recorrer las columnas completas

	for x in range(1,tamagno): #comienza desde la primera para no tomar en cuenta la cabecera
		l1.append((l[x][0])) #recorre las filas con x especificando solo una columna, añadiendo estos datos a las listas creadas anteriormente
		l2.append((l[x][1]))
		l3.append((l[x][2]))
		l4.append((l[x][3]))
		l5.append((l[x][4]))
		l6.append((l[x][5]))
		l7.append((l[x][6]))
	
	#ELIMINAR DATOS VACÍOS EN LISTA
	l_proveedores = list(filter(bool, l1))
	l_modelos = list(filter(bool, l2))
	l_categorias = list(filter(bool, l3))
	l_calidades = list(filter(bool, l4))
	l_agnos = list(filter(bool, l5))
	l_temporadas = list(filter(bool, l6))
	l_episodios = list(filter(bool, l7))

	aux2, aux3, aux4, aux5, aux6, aux7, aux8, aux9 = ('', '', '', '', '', '', '', '') #variables auxiliar
	
	index = 0 #creamos un contador

	video = cv2.VideoCapture(ruta_video)

	while (video.isOpened()): #mientras el video este abierto
		ret, frame = video.read() #leemos el video mientras este abierto. Nos devuelve los valores ret y frame, ret=True si se lee la imagen, ret=False cuando no se lee. frame es la imagen en si misma
		index += 1 #sumamos el contador para saber en que momento de la ejecucion nos encontramos

		if not ret: #si ret es false
			print('no hay imagen, terminando programa... \n')
			break #se detiene la ejecucion en caso de no recibir mas imagen
		
		if (index % 20 == 0): #con esta condicion aceleramos el programa, ya que solo tomara en cuenta los frames que cumplan esta condicion

			print('analysis on process (', os.getpid(), ')' , index) #printiamos indicador e ID de proceso

			gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convertimos a escala de grises para poder convertir a imagen binaria
			_,binary1 = cv2.threshold(gris, 80, 255, cv2.THRESH_BINARY) #binarizamos una imagen para extraer solamente el dato titulo
			
			#print(ret) #printiamos el valor booleano que nos indica si se esta leyendo la imagen o no
			#print(index) #printiamos el valor referencial para saber en que parte de la ejecucion vamos

			#cv2.imshow('video', frame) #mostramos los frames
			#cv2.moveWindow('video', 0, 0) #movemos ventana
			
			if (index == 40): #analizamos el frame 40
				
				for z in range(1, 256): #recorremos cada una de las umbralizaciones utilizando la imagen binary2

					_,binary2 = cv2.threshold(gris, z, 255, cv2.THRESH_BINARY) #creamos una binarización dinámica

					#MODELO DE NEGOCIO:
					x3, y3, h3, w3 = 150, 155, 23, 600
					ROI3 = binary2[y3:y3+h3, x3:x3+w3] #hacemos uso de binary2
					#cv2.imshow('roi3', ROI3)
					#cv2.moveWindow('roi3',600,600)
					aux3 = pytesseract.image_to_string(ROI3).strip() #extraemos el dato modelo de negocio
					if (aux3 == ''):
						aux3 = '@@@'
					print('modelo de negocio: ', aux3)

					#BÚSQUEDA DE DATOS:
					#modelo de negocio:
					for dato1 in l_modelos: #recorre la fuente de información
						if (aux3 == dato1):
							modelo = dato1
							break
						elif (aux3 in dato1):
							modelo = dato1
						elif (dato1 in aux3):
							modelo = dato1

			if (index == 160): #analizamos el frame 160
				
				#TITULO: (el titulo debe estar fuera del recorrido de umbralizaciones, ya que debe ser un dato exacto, debido a que que no tenemos una fuente de conocimiento para comparar los datos)
				x1, y1, h1, w1 = 110, 110, 68, 310 #coordenadas
				ROI1 = binary1[y1:y1+h1, x1:x1+w1] #parte de eje Y + el alto(hacia abajo), sigue el eje X más el ancho (hacia la derecha). Hacemos uso de binary1
				#cv2.imshow('roi1', ROI1) #mostramos el recorte seleccionado
				#cv2.moveWindow('roi1',200,200)
				titulo = pytesseract.image_to_string(ROI1, lang='spa').strip() #extraemos el dato titulo, especificamos lenguaje espagnol para que detecte las tildes
				#print(titulo)

				'''
				x2, y2, h2, w2 = 145, 203, 28, 34
				ROI2 = binary1[y2:y2+h2, x2:x2+w2] #hacemos uso de binary2
				cv2.imshow('roi2', ROI2)
				cv2.moveWindow('roi2',600,600)
				aux2 = pytesseract.image_to_string(ROI2, lang='spa').strip()
				print(aux2)
				'''
				
				for x in range(1, 256): #recorremos cada uno de los umbrales utilizando la imagen binary3

					_,binary3 = cv2.threshold(gris, x, 255, cv2.THRESH_BINARY) #binarizamos una imagen para extraer proveedor, categoria, calidad y agno

					#PROVEEDOR:
					x2, y2, h2, w2 = 967, 135, 31, 60
					ROI2 = binary3[y2:y2+h2, x2:x2+w2] #hacemos uso de binary3
					#cv2.imshow('roi2', ROI2)
					#cv2.moveWindow('roi2',600,600)
					aux2 = pytesseract.image_to_string(ROI2).strip() #extraemos el dato proveedor
					if (len(aux2) < 4):
						aux2 = '@@@'
					#print('proveedor: ', aux2)
					
					#SEPARACIÓN DE DATOS:
					var = ''.join(aux2) #genera un string en base a la lista que extrae la herramienta
					separacion_p = var.split() #generamos otra lista con elementos separados, esos elementos se compararán con la fuente
					

					#CATEGORIA:
					x4, y4, h4, w4 = 150, 177, 20, 113
					ROI4 = binary3[y4:y4+h4, x4:x4+w4]
					#cv2.imshow('roi4', ROI4)
					#cv2.moveWindow('roi4',400,400)
					aux4 = pytesseract.image_to_string(ROI4).strip() #extraemos el dato categoria
					if (aux4 == ''):
						aux4 = '@@@'
					#print('categoria: ', aux4)

					#CALIDAD:
					x5, y5, h5, w5 = 145, 203, 28, 34
					ROI5 = binary3[y5:y5+h5, x5:x5+w5] 
					#cv2.imshow('roi5', ROI5)
					#cv2.moveWindow('roi5',400,400)
					aux5 = pytesseract.image_to_string(ROI5).strip() #extraemos el dato calidad
					if (aux5 == ''):
						aux5 = '@@@'
					#print('calidad: ', aux5)

					#AGNO:
					x6, y6, h6, w6 = 305, 205, 22, 41
					ROI6 = binary3[y6:y6+h6, x6:x6+w6] 
					#cv2.imshow('roi6', ROI6)
					#cv2.moveWindow('roi6',600,600)
					aux6 = pytesseract.image_to_string(ROI6).strip() #extraemos el dato agno
					if (aux6 == ''):
						aux6 = '@@@'
					#print('agno: ', aux6)

					#BÚSQUEDA DE DATOS:
					#proveedores:
					for dato2 in l_proveedores: #recorre la fuente de información
						if (separacion_p[0] == dato2):
							proveedor = dato2
							print(True, 'condicion 1')
							break
						elif (separacion_p[0] in dato2):
							proveedor = dato2
							print(True, 'condicion 2')
						elif (dato2 in separacion_p[0]):
							proveedor = dato2
							print(True, 'condicion 3')
					

					#categorias:
					for dato3 in l_categorias:
						if (aux4 == dato3):
							categoria = dato3
							break
						elif (aux4 in dato3):
							categoria = dato3
						elif (dato3 in aux4):
							categoria = dato3

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
	
	with open('titulos.csv', mode='a', newline='') as Escritura_Datos:
		writer = csv.writer(Escritura_Datos)
		writer.writerow([titulo, proveedor, modelo, categoria, calidad, agno, aux9])

	#tiempo_final = (time.time()) #asignamos tiempo final
	#print('\ntiempo de ejecución premium: ', ("{0:.2f}".format(tiempo_final - tiempo_inicial)), 'seg.') #calculamos y printiamos el tiempo total de ejecucion

	video.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':

	ocr('/home/viruta/Desktop/Archivos/PROGRAMA/Premium/GuerrillaDelOro_Video.mp4')
	'''
	'/home/viruta/Desktop/Archivos/PROGRAMA/Premium/ThisIsUs_Video.mp4'
	'/home/viruta/Desktop/Archivos/PROGRAMA/Premium/PlanetaHostil_Video.mp4'
	'/home/viruta/Desktop/Archivos/PROGRAMA/Premium/GuerrillaDelOro_Video.mp4'
	'''