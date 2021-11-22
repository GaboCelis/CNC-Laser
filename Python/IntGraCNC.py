import tkinter

ventana = tkinter.Tk()
ventana.geometry("400x300")

cajaTexto = tkinter.Entry(ventana)
cajaTexto.pack()

def textoDeCaja():
	cajaTextImp = cajaTexto.get()
	print(cajaTextImp)

boton1 = tkinter.Button(ventana, text = "click", command = textoDeCaja)
boton1.pack()

ventana.mainloop()