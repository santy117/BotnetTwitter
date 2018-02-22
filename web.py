""" web py : accede X veces a una web"""

import urllib2


cadena= "http://www.faitic.uvigo.es/"
f = open ('datos.txt','w')
for contador in range(1,11):
	print 'Realizando conexion a '+cadena+' numero: '+str(contador)
	f.write("acceso a la red.\n")
	response = urllib2.urlopen(str(cadena))

f.close()
