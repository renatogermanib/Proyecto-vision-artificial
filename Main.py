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
#FUNCIONES:
from premium import ocr1
#from series import ocr2
#from alquiler import ocr3

def ingresar_premium():
	print('proceso ingreso premium -> ', os.getpid()) #printeo para la identificación del proceso actual
	global pipe1, pipe1 #declaración cglobal para la utilización de variables declaradas en el Main
	global labelInfo2
	ruta_video = filedialog.askopenfilename(initialdir='/home/viruta/Desktop/Archivos/PROGRAMA/Premium', filetypes=[("all video format", '.mp4')])
	if len(ruta_video) > 0: #si el objeto de askopenfilename tiene un nombre y una ruta, es decir, si escogimos un archivo
		p1 = multiprocessing.Process(target=ocr1, args=(ruta_video, pipe1))
		p1.start()
		visualizar(pipe2)
	else:
		labelInfo2.configure(text='se ha cancelado la selección') #en caso de haber cancelado la elección de video

def ingresar_series():
	ruta_video = filedialog.askopenfilename(initialdir='/home/viruta/Desktop/Archivos/PROGRAMA/Series', filetypes=[('all video format','.mp4')])
	if len(ruta_video) > 0:
		series.ocr(ruta_video)
	else:
		labelInfo2.configure(text='se ha cancelado la selección')

def ingresar_alquiler():
	ruta_video = filedialog.askopenfilename(initialdir='/home/viruta/Desktop/Archivos/PROGRAMA/Alquiler', filetypes=[('all video format','.mp4')])
	if len(ruta_video) > 0:
		alquiler.ocr(ruta_video)
	else:
		labelInfo2.configure(text='se ha cancelado la selección')

def visualizar(conexion):
	print('proceso visualizar -> ', os.getpid())
	global labelVideo #declaración global para la utilización de variables declaradas en el Main
	global root
	while (True): #loop infinito
		im = conexion.recv()
		if (im is None):
			root.update()
			break
		else:
			im = imutils.resize(im, width=720) #redimensionamiento de imagen
			im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB) #converción de bgr a rgb, opencv lee en bgr y PIL muestra el rgb
			im = Image.fromarray(im) #conversión de imagen rgb a arreglo
			im = ImageTk.PhotoImage(im) #conversión de arreglo a un objeto de imagen PIL
			labelVideo['image'] = im #asignación de video al label
			root.update()

if __name__ == '__main__':
	pipe1, pipe2 = multiprocessing.Pipe() #pipe1: emisor - pipe2: receptor

	root = Tk() #creación de ventana principal
	root.title('ANÁLISIS VOD') #asignación de título a la ventana
	w, h = root.winfo_screenwidth(), root.winfo_screenheight() #calcula el ancho y alto máximo de la pantalla
	root.geometry('%dx%d+0+0' % (w, h)) #maximiza la ventana principal a su tamaño máximo

	#creación de fuentes a utilizar
	fuenteTitulos = font.Font(family='Ubuntu Condensed', size=40, weight='bold')
	fuentePrincipal = font.Font(family='Ubuntu Condensed', size=40)

	#LABELS:
	labelInfo1 = Label(root, text='Análisis -')
	labelInfo1.grid(column=0, row=1, padx=5, pady=5)
	labelInfo1['font'] = fuenteTitulos

	labelInfo2 = Label(root, text='aún no se ha ingresado material')
	labelInfo2.grid(column=1, row=1, padx=5, pady=5)
	labelInfo2['font'] = fuentePrincipal

	labelInfo3 = Label(root, text='VIDEO')
	labelInfo3.grid(column=1, row=2)

	labelVideo = Label(root, bg='black') #label donde se reproducirá el video
	labelVideo.grid(column=1, row=3)

	#f1 = LabelFrame(root, bg='red')
	#f1.pack()
	#l1 = Label(f1, bg='yellow')
	#l1.pack()

	#BOTÓN PREMIUM:
	btnVisualizarPremium = Button(root, text='Premium', width=10, command=ingresar_premium, bg='#0052cc', fg='#ffffff') #creación de botón, columnspan permite centrar el botón entre dos columnas, el número especifica la cantidad de columnas
	btnVisualizarPremium.grid(column=10, row=10, padx=5, pady=5) #pad x e y especifica la separación que tendrá frente a los widgets
	btnVisualizarPremium['font'] = fuentePrincipal

	#BOTÓN SERIES:
	btnVisualizarSeries = Button(root, text='Series', width=10, command=ingresar_series, bg='#0052cc', fg='#ffffff')
	btnVisualizarSeries.grid(column=10, row=20, padx=5, pady=5)
	btnVisualizarSeries['font'] = fuentePrincipal

	#BOTÓN ALQUILER:
	btnVisualizarAlquiler = Button(root, text='Alquiler', width=10, command=ingresar_alquiler, bg='#0052cc', fg='#ffffff')
	btnVisualizarAlquiler.grid(column=10, row=30, padx=5, pady=5)
	btnVisualizarAlquiler['font'] = fuentePrincipal

	root.mainloop() #loop que mantiene abierta la ventana durante la ejecución del aplicativo
