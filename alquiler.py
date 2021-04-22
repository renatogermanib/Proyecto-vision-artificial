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
	
	#VACIAR DATOS VACÍOS EN LISTA
	l_proveedores = list(filter(bool, l1))
	l_modelos = list(filter(bool, l2))
	l_categorias = list(filter(bool, l3))
	l_calidades = list(filter(bool, l4))
	l_agnos = list(filter(bool, l5))
	l_temporadas = list(filter(bool, l6))
	l_episodios = list(filter(bool, l7))

	aux2, aux3, aux4, aux5, aux6, aux7, aux8, aux9 = ('', '', '', '', '', '', '', '') #variables auxiliar

	index = 0 #creamos contador

	video = cv2.VideoCapture(ruta_video)

	while (video.isOpened()): #mientras el video este abierto
		ret, frame = video.read() #leemos video
		index += 1 #sumamos contador

		if not ret: #si no se recibe imagen
			print('no hay imagen, terminando programa...')
			break #se detiene la ejecucion

		if (index % 20 == 0): #analizamos los frames que unicamente cumplan esta condicion
			
			print('analysis on process (', os.getpid(), ')' , index) #printiamos indicador e ID de proceso

			#print(index) #printiamos contador para saber en que momento de la ejecucion nos encontramos

			#cv2.imshow('video', frame) #mostramos el video
			#cv2.moveWindow('video',0,0) #movemos la ventana
			
			if (index == 60): #analiza el frame 60

				gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convertimos a escala de grises, creamos la variable aqui para que no se deba crear en cada frame%20==0

				for x in range(1, 256): #recorremos cada una de las umbralizaciones

					_,binary1 = cv2.threshold(gris, x, 255, cv2.THRESH_BINARY) #creamos imagen binaria dinamica

					#MODELO DE NEGOCIO:
					x3, y3, h3, w3 = 570, 155, 23, 650
					ROI3 = binary1[y3:y3+h3, x3:x3+w3] #hacemos uso de binary1
					#cv2.imshow('roi3', ROI3)
					#cv2.moveWindow('roi3',600,600)
					aux3 = pytesseract.image_to_string(ROI3).strip() #extraemos el dato modelo de negocio
					if (aux3 == ''):
						aux3 = '@@@'
					print('modelo de negocio: ', aux3)
					
					#BÚSQUEDA DE DATOS:
					#modelo de negocio:
					for dato1 in l_modelos: #recorre la fuente de información
						if(aux3 == dato1): #si encuentra el dato idéntico, entonces detener ciclo y asignar valor
							modelo = dato1
							break
						elif (aux3 in dato1): #si el dato contiene la palabra presente en la fuente
							modelo = dato1
						elif (dato1 in aux3): #si no se cumple, entonces verifica si la contiene alguna palabra que tenga el dato
							modelo = dato1
							
			if (index == 260): #analizamos el frame 260

				gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convertimos a escala de grises, creamos la variable aqui para que no se deba crear en cada frame%20==0
				_,binary2 = cv2.threshold(gris, 140, 255, cv2.THRESH_BINARY) #creamos imagen binaria para la extraccion del dato titulo

				#TITULO:
				x1, y1, h1, w1 = 142, 135, 40, 450
				ROI1 = binary2[y1:y1+h1, x1:x1+w1] #hacemos uso de binary2
				#cv2.imshow('roi1', ROI1)
				#cv2.moveWindow('roi1',200,200)
				titulo = pytesseract.image_to_string(ROI1).strip() #extraemos el dato titulo
				#print(titulo)

				#PRECIO:
				x9, y9, h9, w9 = 325, 240, 45, 120
				ROI9 = binary2[y9:y9+h9, x9:x9+w9]
				#cv2.imshow('roi9', ROI9)
				#cv2.moveWindow('roi9',300,300)
				precio = pytesseract.image_to_string(ROI9).strip() #extraemos el dato precio
				#print(precio)
				
				for z in range (1, 256): #recorremos cada una de las umbralizaciones

					_,binary3 = cv2.threshold(gris, z, 255, cv2.THRESH_BINARY) #creamos una imagen binaria dinamica

					#CATEGORIA:
					x4, y4, h4, w4 = 150, 177, 20, 75
					ROI4 = binary3[y4:y4+h4, x4:x4+w4] #hacemos uso de binary3
					#cv2.imshow('roi4', ROI4)
					#cv2.moveWindow('roi4',400,400)
					aux4 = pytesseract.image_to_string(ROI4, lang='spa').strip() #extraemos el dato categoria, especificamos espagnol para que detecte tildes
					if (aux4 == ''):
						aux4 = '@@@' #cuando la extracción sea un string vacío, se asignará este valor como "distracción", para que el string vacío no cumpla todas las condicinoes en la búsqueda de datos
					print('categoria: ', aux4)

					#CALIDAD:
					x5, y5, h5, w5 = 145, 203, 28, 34
					ROI5 = binary3[y5:y5+h5, x5:x5+w5] 
					#cv2.imshow('roi5', ROI5)
					#cv2.moveWindow('roi5',700,700)
					aux5 = pytesseract.image_to_string(ROI5).strip() #extraemos el dato calidad
					if (aux5 == ''):
						aux5 = '@@@'
					print('calidad: ', aux5)

					#AGNO:
					x6, y6, h6, w6 = 315, 205, 22, 55
					ROI6 = binary3[y6:y6+h6, x6:x6+w6] 
					#cv2.imshow('roi6', ROI6)
					#cv2.moveWindow('roi6',600,600)
					aux6 = pytesseract.image_to_string(ROI6).strip() #extraemos el dato agno
					if (aux6 == ''):
						aux6 = '@@@'
					print('agno: ', aux4)

					#BÚSQUEDA DE DATOS:
					#categorias:
					for dato2 in l_categorias: #recorre la fuente de información
						if (aux4 == dato2):
							categoria = dato2
							break
						elif (aux4 in dato2):
							categoria = dato2
						elif (dato2 in aux4):
							categoria = dato2
							
					#calidades:
					for dato3 in l_calidades:
						if (aux5 == dato3):
							calidad = dato3
							break
						elif (aux5 in dato3):
							calidad = dato3
						elif (dato3 in aux5):
							calidad = dato3

					#agnos:
					for dato4 in l_agnos:
						if (aux6 == dato4):
							agno = dato4
							break
						elif (aux6 in dato4):
							agno = dato4
						elif (dato4 in aux6):
							agno = dato4
				
				
		if (cv2.waitKey(10) & 0xFF == ord('s')): #especificado en documentacion de opencv->necesario para procesadores de 64bits
			print('se ha detenido la ejecucion')
			break #si se presiona la letra S se detendra el programa
	
	with open('titulos.csv', mode='a', newline='') as Escritura_Datos:
		writer = csv.writer(Escritura_Datos)
		writer.writerow([titulo, aux2, modelo, categoria.title(), calidad, agno, precio])

	#tiempo_final = (time.time()) #asignamos tiempo final
	#print('\ntiempo de ejecución alquiler: ', ("{0:.2f}".format(tiempo_final - tiempo_inicial)), 'seg.') #calculamos y printiamos el tiempo total de ejecucion

	video.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':

	ocr('/home/viruta/Desktop/Archivos/PROGRAMA/Alquiler/ElCuboNegro_Video.mp4')
