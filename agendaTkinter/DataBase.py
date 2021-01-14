import sqlite3

def insertValues(v):
	return  'NULL' if v==None else '?'
class DataBase():
	"""docstring for DataBase"""
	def __init__(self, ruta='',tabla=''):
		self.ruta = ruta
		self.tabla = tabla
		self.conexion = sqlite3.connect(ruta)
		self.cursor = self.conexion.cursor()
	def setTabla(self,tabla):
		self.tabla = tabla
	def crear(self,datos):
		values = list(map(lambda e: insertValues(e),datos))
		datos = list(filter((lambda e: e!=None),datos))
		values = ','.join(values)
		print(datos)
		self.cursor.execute("INSERT INTO {} VALUES({})".format(self.tabla,values),datos)
		self.conexion.commit()
	def cargar(self,id=None):
		if id:
			return self.cursor.execute("SELECT * FROM {} WHERE id={}".format(self.tabla,id)).fetchall()
		else:
			return self.cursor.execute("SELECT * FROM {}".format(self.tabla)).fetchall()
	def actualizar(self,id,columna,dato):
		self.cursor.execute("UPDATE {} SET {}='{}' WHERE id={}".format(self.tabla,columna,dato,id))
		self.conexion.commit()
	def eliminar(self,id,columna='id'):
		self.cursor.execute("DELETE FROM {} WHERE {}={}".format(self.tabla,columna,id))
		self.conexion.commit()
	def confirmar(self):
		self.conexion.commit()
	def cerrar(self):
		self.conexion.close()
	
