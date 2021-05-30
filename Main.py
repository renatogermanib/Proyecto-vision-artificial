#BIBLIOTECAS:
import multiprocessing
import time
from tkinter import *
from tkinter import filedialog
import tkinter.font as font
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import os
#MÓDULOS Y SUS FUNCIONES:
from premium import ocr1
from series import ocr2
from alquiler import ocr3

#FUNCIONES:
def ingresar_premium():
	print('Ingreso premium -> Process (', os.getpid(), ')') #printeo identificación de proceso actual
	global pipe1, pipe2, pipe3 #declaración global para la utilización de variables declaradas en el Main
	global labelInfo2
	ruta_video = filedialog.askopenfilename(initialdir='/home/viruta/Desktop/Archivos/PROGRAMA/Premium', filetypes=[("all video format", '.mp4')])
	if len(ruta_video) > 0: #si el objeto de askopenfilename tiene un nombre y una ruta, es decir, si se escoge un archivo
		p1 = multiprocessing.Process(target=ocr1, args=(ruta_video, pipe1, pipe3)) #creación de proceso para el análisis premium
		p1.start()
		visualizar(pipe2) #llamada a la función visualizar, envío de pipe receptor
	else:
		labelInfo2.configure(text='se ha cancelado la selección') #en caso de haber cancelado la elección de video

def ingresar_series():
	print('Ingreso series -> Process (', os.getpid(), ')')
	global pipe1, pipe2, pipe3
	global labelInfo2
	ruta_video = filedialog.askopenfilename(initialdir='/home/viruta/Desktop/Archivos/PROGRAMA/Series', filetypes=[('all video format','.mp4')])
	if len(ruta_video) > 0:
		p2 = multiprocessing.Process(target=ocr2, args=(ruta_video, pipe1, pipe3)) #creación de proceso para el análisis series
		p2.start()
		visualizar(pipe2) #llamada a la función visualizar, envío de pipe receptor
	else:
		labelInfo2.configure(text='se ha cancelado la selección')

def ingresar_alquiler():
	print('Ingreso alquiler -> Process (', os.getpid(), ')')
	global pipe1, pipe2, pipe3
	global labelInfo2
	ruta_video = filedialog.askopenfilename(initialdir='/home/viruta/Desktop/Archivos/PROGRAMA/Alquiler', filetypes=[('all video format','.mp4')])
	if len(ruta_video) > 0:
		p3 = multiprocessing.Process(target=ocr3, args=(ruta_video, pipe1, pipe3)) #creación de proceso para el análisis alquiler
		p3.start()
		visualizar(pipe2) #llamada a la función visualizar, envío de pipe receptor
	else:
		labelInfo2.configure(text='se ha cancelado la selección')

def visualizar(conexion): #toma como parámetro el pipe receptor
	print('Visualización de análisis -> Process (', os.getpid(), ')')
	global labelVideo #declaración global para la utilización de la variable declarada en el Main
	global root
	global pipe4
	p4 = multiprocessing.Process(target=salidas, args=[pipe4, ]) #llamada a la función salidas, envío de pipe receptor
	p4.start()
	while (True): #loop infinito
		im = conexion.recv() #creación de variable con los datos recibidos por el pipe
		if (im is None):
			root.update() #ejecución de un último update antes del break, con el propósito de eliminar el último frame de reproducción
			break
		else:
			im = imutils.resize(im, width=1100) #redimensionamiento de imagen
			im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB) #converción de bgr a rgb, opencv lee en bgr y PIL muestra el rgb
			im = Image.fromarray(im) #conversión de imagen rgb a arreglo
			im = ImageTk.PhotoImage(im) #conversión de arreglo a un objeto de imagen PIL
			labelVideo['image'] = im #asignación de imágenes al label de video
			labelVideo.pack() #método pack, se ejecuta dentro de la función con el propósito de que el frame se visualice en el tamaño definido en el Main
			root.update() #actualización de ventana principal

def salidas(conexion):
	print('Captura de salidas -> Process', os.getpid(), '\n')
	while (True): #loop infinito
		salida = conexion.recv() #recibe output de fucionalidad de análisis
		if (salida is None):
			print('output vacío')
			break
		else:
			print(salida.strip()) #printeo output proceso de análisis
			print('display of output in process -> (', os.getpid(), ') \n')

if __name__ == '__main__':
	print('Main -> Process (', os.getpid(), ')')
	pipe1, pipe2 = multiprocessing.Pipe() #pipe1: emisor - pipe2: receptor (imágenes de análisis)
	pipe3, pipe4 = multiprocessing.Pipe() #pipe3: emisor - pipe4: receptor (stdout procesos de análisis)

	root = Tk() #creación de ventana principal
	root.title('ANÁLISIS VOD') #asignación de título a la ventana
	w, h = root.winfo_screenwidth(), root.winfo_screenheight() #calcula el ancho y alto máximo de la pantalla
	root.geometry('%dx%d+0+0' % (w, h)) #maximiza la ventana principal a su tamaño máximo

	#creación de fuentes a utilizar
	fuenteTitulos = font.Font(family='Ubuntu Condensed', size=40, weight='bold')
	fuentePrincipal = font.Font(family='Ubuntu Condensed', size=40)

	borde = Frame(root, bg='lightblue', bd=10) #creación de frame contenedor, su objetivo es generar un efecto de borde en el label
	borde.place(relx=0.04, rely=0.05) #utilización de posicionamiento relativo (posicionamiento dinámico)

	ContenedorVideo = Frame(borde, bg='gray', width=1100, height=618) #ancho y alto correspondiente al tamaño asignado por imutils.resize
	ContenedorVideo.pack()

	labelVideo = Label(ContenedorVideo, bg='gray') #label donde se reproducirá el video, su método pack() se encuentra en la función visualizar, con el propósito de no distorcionar el tamaño asignado en el frame contenedor de video.

	#BOTONES:
	btnVisualizarPremium = Button(root, text='Premium', width=10, command=ingresar_premium, bg='#0052cc', fg='#ffffff') #creación de botón, columnspan permite centrar el botón entre dos columnas, el número especifica la cantidad de columnas
	btnVisualizarPremium.place(relx=0.7, rely=0.1) #pad x e y especifica la separación que tendrá frente a los widgets
	btnVisualizarPremium['font'] = fuentePrincipal
	
	btnVisualizarSeries = Button(root, text='Series', width=10, command=ingresar_series, bg='#0052cc', fg='#ffffff')
	btnVisualizarSeries.place(relx=0.7, rely=0.24)
	btnVisualizarSeries['font'] = fuentePrincipal
	
	btnVisualizarAlquiler = Button(root, text='Alquiler', width=10, command=ingresar_alquiler, bg='#0052cc', fg='#ffffff')
	btnVisualizarAlquiler.place(relx=0.7, rely=0.38)
	btnVisualizarAlquiler['font'] = fuentePrincipal

	#consola = Frame(root, bg='brown', width=600, height=200)
	#consola.place(relx=0.1, rely=0.73)

	#tfield = Text(root)
	#tfield.place(relx=0.1, rely=0.73)
	#for line in os.popen("run_command", 'r'):
		#tfield.insert("end", line)

	#wid = consola.winfo_id()
	#os.system('xterm -into %d -geometry 100x20 -sb &' % wid)
	
	root.mainloop() #loop que mantiene abierta la ventana durante la ejecución del aplicativo
