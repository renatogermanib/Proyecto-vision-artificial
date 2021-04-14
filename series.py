import cv2
import pytesseract
import csv
import os
import time

def ocr(ruta_video):

	#tiempo_inicial = time.time()

	aux2, aux3, aux4, aux5, aux6, aux7, aux8, aux9 = ('', '', '', '', '', '', '', '') #variables auxiliar
	
	index = 0

	video = cv2.VideoCapture(ruta_video)

	while (video.isOpened()): #mientras el video este abierto
		ret, frame = video.read() #leer video, ret= True o False. frame=imagen en si misma
		index += 1 #sumamos contador para saber en que parte de la ejecucion nos encontramos

		if not ret: #si ret es False
			print('no hay imagen, terminando programa...')
			break #se detiene el programa cuando no hay lectura de imagen

		if (index % 20 == 0): #aceleramos el programa al analizar solo los frames que cumplan esta condicion
		
			print('analysis on process (', os.getpid(), ')' , index) #printiamos indicador e ID de proceso

			gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convertimos a escala de grises
			
			#print(index) #printiamos el indice para saber en que momento de la ejecucion nos encontramos
			#cv2.imshow('video', frame) #mostramos los frames, es decir, el video
			#cv2.moveWindow('video',0,0) #movemos ventana hacia la esquina
			
			if (index == 140): #analizamos el frame 140

				_,binary1 = cv2.threshold(gris, 90, 255, cv2.THRESH_BINARY) #convertimos a imagen binaria para extraer el título

				#TITULO:
				x1, y1, h1, w1 = 145, 138, 36, 450
				ROI1 = binary1[y1:y1+h1, x1:x1+w1]
				#cv2.imshow('roi1', ROI1)
				#cv2.moveWindow('roi1',200,200)
				titulo = pytesseract.image_to_string(ROI1).strip() #extraemos el titulo
				#print(titulo)
				
				for x in range(1, 256): #recorremos cada uno de los umbrales

					_,binary2 = cv2.threshold(gris, x, 255, cv2.THRESH_BINARY) #creamos imagen binaria dinamica

					#CATEGORIA:
					x4, y4, h4, w4 = 150, 177, 20, 300
					ROI4 = binary2[y4:y4+h4, x4:x4+w4]
					#cv2.imshow('roi4', ROI4)
					#cv2.moveWindow('roi4',400,400)
					aux4 = pytesseract.image_to_string(ROI4, lang='spa').strip() #extraemos el dato categoria, especificamos espagnol para que detecte tildes
					#print('categoria: ', aux4)

					#CALIDAD:
					x5, y5, h5, w5 = 145, 203, 28, 34
					ROI5 = binary2[y5:y5+h5, x5:x5+w5] 
					#cv2.imshow('roi5', ROI5)
					#cv2.moveWindow('roi5',400,400)
					aux5 = pytesseract.image_to_string(ROI5).strip() #extraemos el dato calidad
					#print('calidad: ', aux5)

					#AGNO:
					x6, y6, h6, w6 = 305, 205, 22, 55
					ROI6 = binary2[y6:y6+h6, x6:x6+w6] 
					#cv2.imshow('roi6', ROI6)
					#cv2.moveWindow('roi6',600,600)
					aux6 = pytesseract.image_to_string(ROI6).strip() #extraemos el dato agno
					#print('agno: ', aux4)

					#CORRECCION DE DATOS:
					#proveedores:
					if (len(aux2) == 0): #si el dato proveedor se encuentra vacio quiere decir que VOD no ha especificado ningun proveedor en especifico
						proveedor = 'Independiente'

					#tipo:
					if (len(aux3) == 0): #si modelo de negocio esta vacio se asume que es gratiuito
						modelo = 'Gratis'

					#categorias:
					if ('DRAMA' == aux4): #usamos == para que esta condicion se pueda diferenciar de la siguiente
						categoria = 'Drama'
						#print(categoria)
					if ('ACCIÓN' == aux4):
						categoria = 'Acción'
						#print(categoria)

					#calidades:
					if ('HD' in aux5):
						calidad = 'HD'
						#print(calidad)

					#agnos:
					if ('2019' in aux6):
						agno = '2019'
						#print(agno)
					if ('2020' in aux6):
						agno = '2020'
						#print(agno)
			
			if (index == 440): #analizamos el frame 440
				
				for z in range(1, 256): #recorremos cada uno de los umbrales

					_,binary3 = cv2.threshold(gris, z, 255, cv2.THRESH_BINARY) #creamos imagen binaria dinamica

					#TEMPORADAS:
					x7, y7, h7, w7 = 375, 238, 28, 107
					ROI7 = binary3[y7:y7+h7, x7:x7+w7] 
					#cv2.imshow('roi7', ROI7)
					#cv2.moveWindow('roi7',600,600)
					aux7 = pytesseract.image_to_string(ROI7).strip() #extraemos el dato temporadas
					#print('temporadas: ', aux7)

					#EPISODIOS:
					x8, y8, h8, w8 = 725, 170, 50, 110
					ROI8 = binary3[y8:y8+h8, x8:x8+w8] 
					#cv2.imshow('roi8', ROI8)
					#cv2.moveWindow('roi8',600,600)
					aux8 = pytesseract.image_to_string(ROI8).strip() #extraemos el dato episodios
					#print('episodios: ', aux8)

					#CORRECCION DE DATOS:
					#temporadas:
					if ('Temporada 01' == aux7):
						temporadas = '1ra'
					if ('Temporada 02' == aux7):
						temporadas = '2da'

					#episodios: (utilizamos la condicion == para que la primera y tercera condicion no se cumplan simultaneamente)
					if ('Episodios 1' in aux8):
						episodios = '1'
					if ('Episodios 10' == aux8):
						episodios = '10'
					if ('Episodios 5' == aux8):
						episodios = '5'
				
		if (cv2.waitKey(10) & 0xFF == ord('s')): #especificado en documentacion de opencv->necesario para procesadores de 64bits
			print('se ha detenido la ejecucion')
			break #si se presiona la letra S se detendra el programa

	with open('Datos.csv', mode='a', newline='') as Escritura_Datos:
		writer = csv.writer(Escritura_Datos)
		writer.writerow([titulo, aux2, modelo, categoria, calidad, agno, aux9])

	#tiempo_final = (time.time()) #asignamos tiempo final
	#print('\ntiempo de ejecución series: ', ("{0:.2f}".format(tiempo_final - tiempo_inicial)), 'seg.') #calculamos y printiamos el tiempo total de ejecucion

	video.release()
	cv2.destroyAllWindows()
