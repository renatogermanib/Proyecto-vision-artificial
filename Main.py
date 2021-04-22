from multiprocessing import Process
import time

import premium
import series
import alquiler

if __name__ == '__main__':

	#tiempo_inicial = time.time()
 
	#PROCESOS PARA PREMIUM:
	#p1 = Process(target=premium.ocr, args=('/home/viruta/Desktop/Archivos/PROGRAMA/Premium/PlanetaHostil_Video.mp4', ))
	#p2 = Process(target=premium.ocr, args=('/home/viruta/Desktop/Archivos/PROGRAMA/Premium/ThisIsUs_Video.mp4', ))
	#p3 = Process(target=premium.ocr, args=('/home/viruta/Desktop/Archivos/PROGRAMA/Premium/GuerrillaDelOro_Video.mp4', ))

	#PROCESOS PARA SERIES:
	#p4 = Process(target=series.ocr, args=('/home/viruta/Desktop/Archivos/PROGRAMA/Series/MyBrilliantFriend_Video.mp4', ))
	#p5 = Process(target=series.ocr, args=('/home/viruta/Desktop/Archivos/PROGRAMA/Series/TheOutsider_Video.mp4', ))
	#p6 = Process(target=series.ocr, args=('/home/viruta/Desktop/Archivos/PROGRAMA/Series/Chernobyl_Video.mp4', ))
	
	#PROCESOS PARA ALQUILER:
	#p7 = Process(target=alquiler.ocr, args=('/home/viruta/Desktop/Archivos/PROGRAMA/Alquiler/Sumergidos_Video.mp4', ))
	#p8 = Process(target=alquiler.ocr, args=('/home/viruta/Desktop/Archivos/PROGRAMA/Alquiler/UnLocoFuneral_Video.mp4', ))
	#p9 = Process(target=alquiler.ocr, args=('/home/viruta/Desktop/Archivos/PROGRAMA/Alquiler/ElCuboNegro_Video.mp4', ))

	#EJECUCIONES
	#p1.start()
	#time.sleep(5)
	#p2.start()
	#time.sleep(5)
	#p3.start()
	#time.sleep(5)

	#p4.start()
	#time.sleep(5)
	#p5.start()
	#time.sleep(5)
	#p6.start()
	#time.sleep(5)

	#p7.start()
	#time.sleep(9)
	#p8.start()
	#time.sleep(9)
	#p9.start()

	#CIERRES
	#p1.join()
	#p2.join()
	#p3.join()

	#p4.join()
	#p5.join()
	#p6.join()

	#p7.join()
	#p8.join()
	#p9.join()

	#tiempo_final = time.time()
	#print('\ntiempo de ejecución: ', ("{0:.2f}".format(tiempo_final - tiempo_inicial)), 'seg.') #calculamos y printeamos el tiempo de ejecución total