
from tkinter import *
from DataBase import DataBase
from random import choice
from functools import partial

def aleatorio(l):
	valores = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
	return ''.join([choice(valores) for i in range(l)])

class Root():
	"""docstring for Root"""
	def __init__(self):
		self.correoLista = DataBase('database.db')
		self.default = 'correos'
		self.correoLista.setTabla(self.default)
		self.root = Tk()
		self.root.resizable(height = 0, width = 0)
		self.root.title("Agenda de correos")  
		self.menu()
		self.main = Frame(self.root, width=150, height=100).grid(row=0, column=0)
		self.cargarFrame()
		self.root.mainloop()
	def menu(self):
		self.menubar = Menu(self.root)
		self.root.config(menu=self.menubar) 
		self.mainMenu = Menu(self.menubar,tearoff=0)
		self.mainMenu.add_command(label='Nuevo',command=self.guardarFrame)
		self.mainMenu.add_command(label='Mostrar lista',command=self.cargarFrame)
		self.mainMenu.add_command(label='Editar',command=self.editarFrame)
		self.mainMenu.add_separator()
		self.mainMenu.add_command(label='Salir', command=self.root.quit)
		self.menubar.add_cascade(label="Menu", menu=self.mainMenu)
	def listaPaginas(self):
		self.correoLista.setTabla('paginas')
		paginas=self.correoLista.cargar()
		self.correoLista.setTabla(self.default)	
		return paginas
	def guardarFrame(self,frame=None,datos=None):
		if frame:
			self.frame = Frame(frame)
			self.frame.grid(row=0,column=0,columnspan=12)
		else:
			try:
				self.frame.destroy()
			except AttributeError as e:
				pass
			finally:
				self.frame = Frame(self.main)
				self.frame.grid(row=0,column=0,columnspan=12)
		self.pagina=StringVar(frame)
		self.email =  StringVar(frame)
		self.password = StringVar(frame)
		opciones= [pagina[1] for pagina in self.listaPaginas()]
		self.pagina.set(opciones[0])
		id = None
		if datos:
			self.pagina.set(datos['pagina'])
			self.email.set(datos['email'])
			self.password.set(datos['password'])
			id = datos['id']
		Label(self.frame,text='Email').grid(pady=10,row = 2,column=0,columnspan=12)
		Entry(self.frame,textvariable=self.email,bg="white").grid(padx=(0,20),row = 3,column=0, columnspan=9)
		Button(self.frame,text='Aleatorio',command=(lambda: self.email.set(aleatorio(6)+'@gmail.com'))).grid(padx=20,row = 3,column=9,columnspan=3)
		Label(self.frame,text='Contraseña').grid(pady=10,row = 4,column=0,columnspan=12)
		Entry(self.frame,textvariable=self.password,bg="white").grid(padx=(0,20),row = 5,column=0, columnspan=9)
		Button(self.frame,text='Aleatorio',command=(lambda: self.password.set(aleatorio(10)))).grid(padx=20,row = 5,column=9,columnspan=3)

		Label(self.frame,text='Sitio').grid(pady=10,row = 6,column=0,columnspan=12)
		opcion = OptionMenu(self.frame,self.pagina,*opciones)
		opcion.config(width=20)
		opcion.grid(padx=(20,0),row=7,column=0)
		if not frame:
			Button(self.frame, text='Nuevo',command=self.ventanaNuevaPagina).grid(padx=20,row=7,column=9,columnspan=3)
		textoBoton = 'Guardar' if not frame else 'Actualizar'
		Button(self.frame,text=textoBoton,command=partial(self.guardar,id)).grid(pady=10,row = 8,column=0,columnspan=12)
	def cargarFrame(self):
		try:
			self.frame.destroy()
		except AttributeError as e:
			pass
		finally:
			self.frame = Frame(self.main)
			self.frame.grid(row=0,column=0,columnspan=12)
		paginas = self.listaPaginas()
		texto = Text(self.frame,font=('Calibri',12),width=35)
		texto.grid(row=0,columns=2)
		correos = self.correoLista.cargar()
		for c in correos:
			pagina= list(filter(lambda e: e[0]==c[3],paginas))[0][1]
			contenido ="{}\nnombre:{} \ncontraseña:{}\n\n".format(pagina,c[1],c[2])
			texto.insert('insert', contenido)
	def editarFrame(self):
		try:
			self.frame.destroy()
		except AttributeError as e:
			pass
		finally:
			self.frame = Frame(self.main)
			self.frame.grid(row=0,columns=12)
		row = 0
		correos = self.correoLista.cargar()
		paginas = self.listaPaginas()
		for correo in correos:
			try:
				pagina= list(filter(lambda e: e[0]==correo[3],paginas))
				texto = "{}: {}".format(pagina[0][1],correo[1])
			except IndexError as e:
				pass
			Label(self.frame,text=texto,anchor='w').grid(row=(0+row),column=0,columnspan=4)
			Button(self.frame,text='Editar',command=partial(self.ventanaEditar,correo[0])).grid(row=(0+row),column=4,columnspan=4)
			Button(self.frame,text='Borrar',command=lambda: self.correoLista.eliminar(correo[0])).grid(row=(0+row),column=8,columnspan=4)
			row = row+1	
	def ventanaNuevaPagina(self):
		self.ventana = Tk()
		self.ventana.title("Nuevo sitio")  
		self.ventana.resizable(width=0,height=0)
		self.pagina = StringVar(self.ventana)
		self.botones = []
		Label(self.ventana,text='Paginas',font=('Roman',18)).pack()
		for pagina in self.listaPaginas():
			var = IntVar(self.ventana)
			Checkbutton(self.ventana, text=pagina[1],variable=var,onvalue=pagina[0], offvalue=0).pack(anchor=W)
			self.botones.append(var)
			#var.set('0')
		Button(self.ventana,text=('Borrar seleccionados'),command=self.borrarPag).pack(anchor='s')
		form = Frame(self.ventana,bg="#0f0")
		form.pack(ipady=10,fill=X,side=TOP)
		Entry(form,width=25,textvariable=self.pagina,bg="white").pack(padx=20,side=LEFT)
		Button(form,text='Nuevo',command=self.nuevo).pack(padx=(0,20),side=LEFT)
	def ventanaEditar(self,id):
		self.ventana = Tk()
		self.ventana.title('Editar')
		self.ventana.resizable(width=0,height=0)
		editar = Frame(self.ventana,bg="#ff0")
		editar.grid(row=0,column=0)
		datosTupla = self.correoLista.cargar(id)[0]
		paginas = self.listaPaginas()
		pagina= list(filter(lambda e: e[0]==datosTupla[3],paginas))[0][1]

		datos = {'pagina':pagina,
				'email':datosTupla[1], 
				'password':datosTupla[2],
				'id':datosTupla[0]}
		self.guardarFrame(editar,datos)
	def guardar(self,Upgrade=None):
		paginas = self.listaPaginas()
		id= list(filter(lambda e: e[1]==self.pagina.get(),paginas))[0][0]
		if self.email.get().find("@") != -1:
			datos = [None,self.email.get(),self.password.get(),id]
			if Upgrade:
				self.correoLista.actualizar(Upgrade,'correo',datos[1]),
				self.correoLista.actualizar(Upgrade,'contrasena',datos[2]),
				self.correoLista.actualizar(Upgrade,'id_pagina',datos[3])
				self.ventana.destroy()
				self.cargarFrame()
			else:	
				self.correoLista.crear(datos)
		else:
			print('Error no se introdujo una direccion valida')
	def nuevo(self):
		pagina = self.pagina.get()
		if len(pagina)>0:
			self.correoLista.setTabla("paginas")
			self.correoLista.crear([None,pagina])
			self.correoLista.setTabla(self.default)
			self.ventana.destroy()
			self.guardarFrame()
		else:
			Label(self.ventana,text='Error',font=('Roman',16)).pack(side=BOTTOM)
	def borrarPag(self):
		check = [x.get()for x in self.botones]
		checkFiltrado = list(filter(lambda e: e,check))
		for e in checkFiltrado:
			if e != 1:
				self.correoLista.eliminar(e,'id_pagina')
				self.correoLista.setTabla('paginas')
				self.correoLista.eliminar(e)
				self.correoLista.setTabla(self.default)
		self.ventana.destroy()
Root()
