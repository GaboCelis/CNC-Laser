from tkinter import *
from tkinter import messagebox, ttk, filedialog
from turtle import width
import serial, serial.tools.list_ports
from tkinter.messagebox import showinfo
import time

class CNCInt(Frame):

    fuente = '#121212'
    #serialArduino = serial.Serial("COM5", 115200)
    #print(serialArduino.name)
    
    def __init__(self, master=None):
        super().__init__(master,width=800, height=500)
        self.master = master
        self.pack()
        # self.ancho_ventana = ancho_ventana
        # self.alto_ventana = alto_ventana
        self.ValX = DoubleVar(value=0.0)
        self.ValY = DoubleVar(value=0.0)
        self.ValZ = DoubleVar(value=0.0)
        self.ValXa = DoubleVar(value=0.0)
        self.ValYa = DoubleVar(value=0.0)
        self.ValZa = DoubleVar(value=0.0)
        self.Avance = DoubleVar(value=1.0)
        self.EstaLaser = BooleanVar(value=False)
        self.port=[]
        self.Archivo=""
        self.ApProfundidad = IntVar()
        self.serialArduino = serial.Serial()
        self.feedrate = [20, 50, 100, 200, 300, 400, 500, 600, 700, 1000]
        self.LisBaudos = [2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400, 250000] 
        self.Profun = [-0.1, -0.2, -0.3, -0.4, 0.5, 0.6, 0.7, 0.8, 0.9, -1] 
        self.Ciclos = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
        self.Poten = [5, 10, 20, 20, 30, 40, 50, 60, 70, 80, 90, 100] 
        self.create_widgets()
        
        # Función para leer los puertos disponibles
    def get_ports(self):
        self.port=[]
        ports = serial.tools.list_ports.comports()
        try:
            for i in ports:
                self.port.append(i.device)
            self.Puertos["values"]=self.port
            self.Puertos.current(0)
            self.serialArduino.port = self.Puertos.get()
                        
        except:
            messagebox.showinfo(message="No hay puerto conectados", title="Sin puertos")
        if self.Puertos == None:
                pass
        else:
            self.Puerto.configure(background="#F1EB1E")
        # Función para realizar la conexion por el puerto seleccionado
    def fnConectar(self):
        if self.serialArduino.port == None:
            messagebox.showinfo(message="Actualiza los puertos y selecciona uno", title="Puerto no seleccionado")
            return
        if self.serialArduino.is_open:
            self.fnHome()

            self.EstaLaser = False
            self.FnEncLaser()

            self.Puerto.configure(background="#F1EB1E")
            self.LBaudios.configure(background="#E13D20")

            self.ConectArduino.configure(text="Conectar Arduino")
            self.serialArduino.close()
            if self.serialArduino.is_open:
                messagebox.showinfo(message="Desconexión no exitosa", title="Desconexion de Arduino")
            else:
                messagebox.showinfo(message="Desconexión exitosa", title="Desconexion de Arduino")
        else:
            self.serialArduino.baudrate = self.Baudios.get()
            self.serialArduino.timeout = None
            self.serialArduino.open()

            self.serialArduino.port = self.Puertos.get()
            self.serialArduino.baudrate = self.Baudios.get()
            self.Puerto.configure(background="#78E120")
            self.LBaudios.configure(background="#78E120")
            self.ConectArduino.configure(text="Desconectar Arduino")
            if self.serialArduino.is_open:
                isRun = True
                while isRun:
                    aux = self.serialArduino.readline().decode("ascii").strip()
                    if aux: 
                        isRun = False
                    # self.fnHome()
                    self.EstaLaser = False
                    self.FnEncLaser()
                messagebox.showinfo(message="Conexión exitosa", title="Desconexion de Arduino")
            else:
                messagebox.showinfo(message="Conexión no exitosa", title="Conexion de Arduino")
        # Función para seleccionar la distancia de avance
    def fnAvance(self, opc):
        aux = self.Avance.get()
        # aux = float(aux)
        if opc == 0:
            if aux <= 10:
                aux = aux*10
                self.Avance = DoubleVar(value=aux) 
            else:
                pass
        else:
            if aux >= 0.1:
                aux = aux/10
                self.Avance = DoubleVar(value=aux)
            else:
                pass
        self.ValAv.config(textvariable=self.Avance)
        # Función para desplegar las coordenadas a la se encuentra el láser
    def fnCoo(self, Eje):
        if Eje == 'X':
            aux = self.CooX.get()
            try:
                aux = float(aux)
                if self.ValX == aux:
                    pass
                elif aux <= 330.00 and aux >=0:
                    self.CooX.delete(0,'end')
                    self.ValX = DoubleVar(value=aux)
                    self.ValXa = DoubleVar(value=aux)
                    self.CooX.insert(0,str(aux))
                elif aux > 330:
                    self.CooX.delete(0,'end')
                    self.ValX = DoubleVar(value=330.0)
                    self.ValXa = DoubleVar(value=330.0)
                    self.CooX.insert(0,str(aux))
                    messagebox.showinfo(message="Las coordenadas deben ser de 0 a 330 mm", title="Error de valor de coordenada")
                else:
                    self.CooX.delete(0,'end')
                    self.ValX = DoubleVar(value=0.0)
                    self.ValXa = DoubleVar(value=0.0)
                    self.CooX.insert(0,str(aux))
                    messagebox.showinfo(message="Las coordenadas deben ser de 0 a 330 mm", title="Error de valor de coordenada")           
            except:
                aux = self.ValXa.get()
                aux = float(aux)
                self.CooX.delete(0,'end')
                self.ValX = DoubleVar(value=aux)
                self.CooX.insert(0, str(aux))
                messagebox.showinfo(message="Las coordenadas deben ser de 0 a 330 mm", title="Error de valor de coordenada")                
        elif Eje == 'Y':
            aux = self.CooY.get()
            try:
                aux = float(aux)
                if self.ValY == aux:
                    pass
                elif aux <= 330.00 and aux >=0:
                    self.CooY.delete(0,'end')
                    self.ValY = DoubleVar(value=aux)
                    self.ValYa = DoubleVar(value=aux)
                    self.CooY.insert(0,str(aux))
                elif aux > 330:
                    self.CooY.delete(0,'end')
                    self.ValY = DoubleVar(value=330.0)
                    self.ValYa = DoubleVar(value=330.0)
                    self.CooY.insert(0,str(aux))
                    messagebox.showinfo(message="Las coordenadas deben ser de 0 a 330 mm", title="Error de valor de coordenada")
                else:
                    self.CooY.delete(0,'end')
                    self.ValY = DoubleVar(value=0.0)
                    self.ValYa = DoubleVar(value=0.0)
                    self.CooY.insert(0,str(aux))
                    messagebox.showinfo(message="Las coordenadas deben ser de 0 a 330 mm", title="Error de valor de coordenada")                
            except:
                aux = self.ValYa.get()
                aux = float(aux)
                self.CooY.delete(0,'end')
                self.ValY = DoubleVar(value=aux)
                self.CooY.insert(0, str(aux))
                messagebox.showinfo(message="Las coordenadas deben ser de 0 a 330 mm", title="Error de valor de coordenada")
        elif Eje == 'Z':
            aux = self.CooZ.get()
            try:
                aux = float(aux)
                if self.ValZ == aux:
                    pass
                elif aux <= 100.00 and aux >=0:
                    self.CooZ.delete(0,'end')
                    self.ValZ = DoubleVar(value=aux)
                    self.ValZa = DoubleVar(value=aux)
                    self.CooZ.insert(0,str(aux))
                elif aux > 100:
                    self.CooZ.delete(0,'end')
                    self.ValZ = DoubleVar(value=100.0)
                    self.ValZa = DoubleVar(value=100.0)
                    self.CooZ.insert(0,str(aux))
                    messagebox.showinfo(message="Se ha alcanzado el limite de la mesa (0 a 100 mm)", title="Limite de coordenadas")
                else:
                    aux = self.ValZa.get()
                    aux = float()
                    self.CooZ.delete(0,'end')
                    self.ValZ = DoubleVar(value=aux)
                    self.ValZa = DoubleVar(0.0)
                    self.CooZ.insert(0,str(aux))
                    messagebox.showinfo(message="Se ha alcanzado el limite de la mesa (0 a 100 mm)", title="Limite de coordenadas")                
            except:
                aux = self.ValZa.get()
                aux = float(aux)
                self.CooZ.delete(0,'end')
                self.ValZ = DoubleVar(value=aux)
                self.CooZ.insert(0, str(aux))
                messagebox.showinfo(message="La coordenada debe ser un número de 0 a 100", title="Error de valor de coordenada")
        #Función que realiza el movimiento en cada uno de los ejes
    def fnMov(self, Eje, Dir, Par):
        aux3 = self.FeedRate.get()
        aux3 = float(aux3)
        if Eje == 'X':
            aux = self.ValX.get()
            aux = float(aux)
            aux2 = self.Avance.get()
            aux2= float(aux2)
            if Dir == 0:
                if aux > 0:
                    aux = round(aux - aux2, 2)
                    if aux < 0:
                        if Par == 0:
                            self.fnEnvMovS(Eje, aux+aux2, aux3)
                        aux = 0
                        messagebox.showinfo(message="Se ha alcanzado el limite de la mesa (0 a 330 mm)", title="Limite de coordenadas")
                    else:
                        if Par == 0:
                            self.fnEnvMovS(Eje, -aux2, aux3)
                    self.CooX.delete(0,'end')
                    self.ValX = DoubleVar(value=aux)
                    self.ValXa = DoubleVar(value=aux)

                    self.CooX.insert(0,aux)
                elif aux <= 0:
                    messagebox.showinfo(message="Se ha alcanzado el limite de la mesa (0 a 330 mm)", title="Limite de coordenadas")
            elif Dir == 1:
                if aux < 300:
                    aux = round(aux + aux2, 2)
                    if aux > 300:
                        if Par == 0:
                            self.fnEnvMovS(Eje, aux-300, aux2)
                        aux = 300
                        messagebox.showinfo(message="Se ha alcanzado el limite de la mesa (0 a 330 mm)", title="Limite de coordenadas")
                    else:
                        if Par == 0:
                            self.fnEnvMovS(Eje, aux2, aux3)
                    self.CooX.delete(0,'end')
                    self.ValX = DoubleVar(value=aux)
                    self.ValXa = DoubleVar(value=aux)
                    self.CooX.insert(0,aux)
                elif aux >= 300:
                    messagebox.showinfo(message="Se ha alcanzado el limite de la mesa (0 a 330 mm)", title="Limite de coordenadas")                
        elif Eje == 'Y':
            aux = self.ValY.get()
            aux = float(aux)
            aux2 = self.Avance.get()
            aux2 = float(aux2)

            if Dir == 0:
                if aux > 0:
                    aux = round(aux - aux2, 2)
                    if aux < 0:
                        if Par == 0:
                            self.fnEnvMovS(Eje, aux+aux2, aux3)
                        aux = 0
                        if Par == 0:
                            messagebox.showinfo(message="Se ha alcanzado el limite de la mesa (0 a 330 mm)", title="Limite de coordenadas")
                    else:
                        if Par == 0:
                            self.fnEnvMovS(Eje, -aux2, aux3)
                    self.CooY.delete(0,'end')
                    self.ValY = DoubleVar(value=aux)
                    self.ValYa = DoubleVar(value=aux)
                    self.CooY.insert(0,aux)
                elif aux <= 0:
                    if Par == 0:
                        messagebox.showinfo(message="Se ha alcanzado el limite de la mesa (0 a 330 mm)", title="Limite de coordenadas")
            elif Dir == 1:
                if aux < 300:
                    aux = round(aux + aux2, 2)
                    if aux > 300:
                        if Par == 0:
                            self.fnEnvMovS(Eje, aux-300, aux3)
                        aux = 300
                        if Par == 0:
                            messagebox.showinfo(message="Se ha alcanzado el limite de la mesa (0 a 330 mm)", title="Limite de coordenadas")
                    else:
                        if Par == 0:
                            self.fnEnvMovS(Eje, aux2, aux3)
                    self.CooY.delete(0,'end')
                    self.ValY = DoubleVar(value=aux)
                    self.ValYa = DoubleVar(value=aux)
                    self.CooY.insert(0,aux)
                elif aux >= 300:
                    if Par == 0:
                        messagebox.showinfo(message="Se ha alcanzado el limite de la mesa (0 a 330 mm)", title="Limite de coordenadas")
        elif Eje == 'Z':
            aux = self.ValZ.get()
            aux = float(aux)
            aux2 = self.Avance.get()
            aux2= float(aux2)
            if Dir == 0:
                if aux > -30:
                    aux = round(aux - aux2, 2)
                    if aux < -30:
                        if Par == 0:
                            self.fnEnvMovS(Eje, aux+30, aux3)
                        aux = -30
                        messagebox.showinfo(message="Se ha alcanzado el limite del eje Z (0 a 100 mm)", title="Limite de coordenadas")
                    else:
                        if Par == 0:
                            self.fnEnvMovS(Eje, -aux2, aux3)
                    self.CooZ.delete(0,'end')
                    self.ValZ = DoubleVar(value=aux)
                    self.ValZa = DoubleVar(value=aux)
                    self.CooZ.insert(0,aux)
                elif aux <= 0:
                    messagebox.showinfo(message="Se ha alcanzado el limite del eje Z (0 a -100 mm)", title="Limite de coordenadas")
            elif Dir == 1:
                if aux < 0:
                    aux = round(aux + aux2, 2)
                    if aux > 0:
                        self.fnEnvMovS(Eje, -aux+aux2, aux3)
                        aux = 0
                        messagebox.showinfo(message="Se ha alcanzado el limite del eje Z (0 a -100 mm)", title="Limite de coordenadas")
                    else:
                        self.fnEnvMovS(Eje, aux2, aux3)
                    self.CooZ.delete(0,'end')
                    self.ValZ = DoubleVar(value=aux)
                    self.ValZa = DoubleVar(value=aux)
                    self.CooZ.insert(0,aux)
                elif aux >= 0:
                    messagebox.showinfo(message="Se ha alcanzado el limite del eje Z (0 a -100 mm)", title="Limite de coordenadas")
        # Función para realizar el movimiento del eje X y Y al mismo tiempo
    def fnMovPar(self, Eje1, Dir1, Eje2, Dir2):
        aux = self.Avance.get()
        aux= float(aux)
        aux3 = self.FeedRate.get()
        aux3 = float(aux3)
        if Dir1 == 1 and Dir2 == 1:
            print("11")
            self.fnEnvMovPar(aux, aux, aux3)
        elif Dir1 == 0 and Dir2 == 1:
            print("01")
            self.fnEnvMovPar(-aux, aux, aux3)
        elif Dir1 == 1 and Dir2 == 0:
            print("10")
            self.fnEnvMovPar(aux, -aux, aux3)
        else:
            print("00")
            self.fnEnvMovPar(-aux, -aux, aux3)

        self.fnMov(Eje1, Dir1, 1)
        self.fnMov(Eje2, Dir2, 1)
        # Función para realizar el Home de todos los ejes ( Manda a 0 todas las coordenadas)
    def fnHome(self):
        auxX = self.ValX.get()
        auxX = float(auxX)
        auxY = self.ValY.get()
        auxY = float(auxY)
        auxZ = self.ValZ.get()
        auxZ = float(auxZ)

        
        self.fnEnvMovS("Z", -auxZ, 700)
        self.fnEnvMovS("X", -auxX, 700)
        self.fnEnvMovS("Y", -auxY, 700)

        self.CooX.delete(0,'end')
        self.ValX = DoubleVar(value=0)
        self.ValXa = DoubleVar(value=0)
        self.CooX.insert(0,0.0)
        self.CooY.delete(0,'end')
        self.ValY = DoubleVar(value=0)
        self.ValYa = DoubleVar(value=0)
        self.CooY.insert(0,0.0)
        self.CooZ.delete(0,'end')
        self.ValZ = DoubleVar(value=0)
        self.ValZa = DoubleVar(value=0)
        self.CooZ.insert(0,0.0)
        # Función para abrir ventana de busqueda del archivo a utilizar
    def browseFiles(self): 
        self.Archivo = filedialog.askopenfilename(initialdir = "/", title = "Seleccione un archivo", filetypes = (("Archivos gcode", "*.gcode"), ("all files", "*.*"))) 
        aux = self.Archivo.split("/")
        aux = aux[len(aux)-1]
        aux = aux.split(".")
        self.LArchivo.configure(text=aux[0])
        
        showinfo( title='Selected File', message = self.Archivo)
        self.Correr.configure(background="#F1EB1E")
        # Función para eecutar el programa seleccionado
    def fnCorrer(self):
        try:
            nciclos = self.Cicl.get()
            nciclos = int(nciclos)
            Acpro = self.ApProfundidad.get()
            Acpro = int(Acpro)
            pro = self.Prof.get()
            pro = str(pro)
            for i in range(nciclos):
                
                self.Correr.configure(background="#78E120")
                f = open(self.Archivo,'r')
                txt = "\r\n\r\n"
                self.serialArduino.write(txt.encode("ascii"))
                time.sleep(2)   # Wait for grbl to initialize 
                self.serialArduino.flushInput()  # Flush startup text in serial input
                if Acpro == 1:
                    l = "G0 Z" + pro # Strip all EOL characters for consistency
                    print ('Sending: ' + l)
                    txt2 = l + '\n'
                    self.serialArduino.write(txt2.encode("ascii")) # Send g-code block to grbl
                    grbl_out = self.serialArduino.readline().decode("ascii") # Wait for grbl response with carriage return
                    print (' : ' + grbl_out.strip())
                    # self.fnEnvMovS("Z", pro, 200)
                for line in f:
                        l = line.strip() # Strip all EOL characters for consistency
                        print ('Sending: ' + l)
                        txt2 = l + '\n'
                        self.serialArduino.write(txt2.encode("ascii")) # Send g-code block to grbl
                        grbl_out = self.serialArduino.readline().decode("ascii") # Wait for grbl response with carriage return
                        print (' : ' + grbl_out.strip())
                
                if i >= (nciclos-1) and Acpro == 1:
                    # pro = float(pro)
                    pro = nciclos*(-float(pro))
                    pro = str(pro)
                    # print(str(pro))
                    l = "S5 M5 G0 Z" + pro # Strip all EOL characters for consistency
                    print ('Sending: ' + l)
                    txt2 = l + '\n'
                    self.serialArduino.write(txt2.encode("ascii")) # Send g-code block to grbl
                    grbl_out = self.serialArduino.readline().decode("ascii") # Wait for grbl response with carriage return
                    print (' : ' + grbl_out.strip())
                    # self.fnEnvMovS("Z", pro, 200)

                f.close()
            
            

            self.EstaLaser = False
            self.FnEncLaser()
            self.Encender.configure(text="Encender Láser a " + self.Potencia.get() + "%")
            messagebox.showinfo(message="Fin de la ejecución del archivo", title="Ejecucion exitosa")  
        except:
            messagebox.showinfo(message="No se pudo ejecutar el archivo", title="Error de ejecucion")
        self.Correr.configure(background="#F1EB1E")
        # Función para enviar las instruccioines de los movimientos a cada eje
    def fnEnvMovS(self, Eje, aux, aux2):        
        l = "$J=G21G91" + str(Eje) + str(aux) + "F" + str(aux2)  # Strip all EOL characters for consistency
        print ('Sending: ' + l)
        txt2 = l + '\n'
        self.serialArduino.write(txt2.encode("ascii")) # Send g-code block to grbl
        grbl_out = self.serialArduino.readline().decode("ascii") # Wait for grbl response with carriage return
        print (' : ' + grbl_out.strip())
        # Función para enviar las instrucciones de los ejes X y Y al mismo tiempo    
    def fnEnvMovPar(self, aux1, aux2, aux3):
        l = "$J=G21G91X" + str(aux1) +"Y" + str(aux2) + "F"+str(aux3)  # Strip all EOL characters for consistency
        print ('Sending: ' + l)
        txt2 = l + '\n'
        self.serialArduino.write(txt2.encode("ascii")) # Send g-code block to grbl
        grbl_out = self.serialArduino.readline().decode("ascii") # Wait for grbl response with carriage return
        print (' : ' + grbl_out.strip())
        # Función para encender o apagar el láser
    def FnEncLaser(self):

        if self.EstaLaser:
            self.Encender.configure(text="Apagar Láser")
            self.EstaLaser = False
            aux = self.Potencia.get().strip()
            l = "M3 S" + str(aux) # Strip all EOL characters for consistency
            print ('Sending: ' + l)
            txt2 = l + '\n'
            self.serialArduino.write(txt2.encode("ascii")) # Send g-code block to grbl
            grbl_out = self.serialArduino.readline().decode("ascii") # Wait for grbl response with carriage return
            print ( grbl_out.strip())
            
        else:
            self.Encender.configure(text="Encender Láser a " + self.Potencia.get() + "%")
            self.EstaLaser = True
            l = "M5"# Strip all EOL characters for consistency
            print ('Sending: ' + l)
            txt2 = l + '\n'
            self.serialArduino.write(txt2.encode("ascii")) # Send g-code block to grbl
            grbl_out = self.serialArduino.readline().decode("ascii") # Wait for grbl response with carriage return
            print ( grbl_out.strip())

    def fnPrueba(self):
        text = "$$\n"
        self.serialArduino.write(text.encode("ascii"))
        prueba = self.serialArduino.readline().decode("ascii").strip()
        # self.fnArch()
        
        # prueba = self.serialArduino.read()
        # print(prueba.decode("ascii"))
        isRun =True
        while isRun:
            
            if prueba:
                # print(self.serialArduino.in_waiting)
                # prueba = self.serialArduino.readline()
                print(prueba)
                if prueba == "ok":
                    isRun = False
                else:
                    prueba = self.serialArduino.readline().decode("ascii").strip()
        # Función donde se crean todos los botenes de la ventana
    def create_widgets(self):
        
        #       FRAME de Inicio
        fIni = 'gray'
        #       FRAME de Ejes
        BLabelPos = '#A1D1D1'
        BLabelCoo = '#CDF7C8'
        BLabelDP1 = '#4CFF33'
        BLabelDP2 = '#FF6E33'
        BLabelDH = '#FCFF33'
        
        ##############################
        #       FRAME de Inicio
        ##############################
        FrameInicio = Frame(self)
        FrameInicio.place(relx=0.025,rely=0.05)
        ################
        self.Puerto=Label(FrameInicio, text="Puerto de lectura", fg = self.fuente, bg="#E13D20")
        self.Puerto.grid(column=0, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.Puertos = ttk.Combobox(FrameInicio, textvariable=self.port, justify=RIGHT, width=10)#, state="readonly"
        self.Puertos.grid(column=1, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.ActPuet=Button(FrameInicio, text="Actualizar puertos", fg = self.fuente, bg="#2098E1", command = self.get_ports)
        self.ActPuet.grid(column=3, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        ################
        self.LBaudios=Label(FrameInicio, text="Baoudios", fg = self.fuente, bg="#E13D20")
        self.LBaudios.grid(column=0, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.Baudios = ttk.Combobox(FrameInicio, values=self.LisBaudos, justify=RIGHT, width=10)
        self.Baudios.grid(column=1, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        self.Baudios.current(6)
        
        self.ConectArduino=Button(FrameInicio, text="Conectar Arduino", fg = self.fuente, bg="#2098E1", command = self.fnConectar)
        self.ConectArduino.grid(column=3, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        ################
        self.Archivo=Button(FrameInicio, text="Cargar Archivo", fg = self.fuente, bg="#2098E1", command = self.browseFiles)
        self.Archivo.grid(column=0, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.LArchivo = Label(FrameInicio, text=" ", fg = self.fuente , bg=fIni)
        self.LArchivo.grid(column=1, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.Correr=Button(FrameInicio, text="Correr archivo", fg = self.fuente, bg="#2098E1", command = self.fnCorrer)
        self.Correr.grid(column=3, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)

        ##############################
        #       FRAME de Ajuste Laser
        ##############################
        FrameAjuLaser = Frame(self)
        FrameAjuLaser.place(relx=0.025,rely=0.22)#relwidth=0.2, relheight=0.09

        Label(FrameAjuLaser, text="Parametros del Láser", fg = self.fuente, ).grid(columnspan=2, row=0, sticky=NSEW, padx=0, pady=0)
        
        Label(FrameAjuLaser, text="Profundidad", fg = self.fuente).grid(column=0, row=1, sticky=NSEW, padx=0, pady=0)
        
        self.Prof = ttk.Combobox(FrameAjuLaser, values=self.Profun, justify=RIGHT, width=5)
        self.Prof.grid(column=0, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        self.Prof.current(0)

        Label(FrameAjuLaser, text="mm", fg = self.fuente, ).grid(column=1, row=2, sticky=NSEW, padx=0, pady=0)
        
        # Label(FrameAjuLaser, text="Aplicar profundidad", fg = self.fuente, ).grid(columnspan=3, row=3, sticky=NSEW, padx=0, pady=0)
        
        ApliProfundidad = ttk.Checkbutton(FrameAjuLaser, text="Aplicar profundidad", variable=self.ApProfundidad, onvalue=1, offvalue=0)
        ApliProfundidad.grid(columnspan=3, row=3, sticky=NSEW, padx=0, pady=0)
         
        Label(FrameAjuLaser, text="Ciclos", fg = self.fuente).grid(column=0, row=4, sticky=NSEW, padx=0, pady=0)
        
        self.Cicl = ttk.Combobox(FrameAjuLaser, values=self.Ciclos, justify=RIGHT, width=5)
        self.Cicl.grid(column=0, row=5, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        self.Cicl.current(0)
        
        Label(FrameAjuLaser, text="Potencia (%)", fg = self.fuente).grid(column=0, row=6, sticky=NSEW, padx=0, pady=0)
        
        self.Potencia = ttk.Combobox(FrameAjuLaser, values=self.Poten, justify=RIGHT, width=5)
        self.Potencia.grid(column=0, row=7, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        self.Potencia.current(0)
        
        # Label(FrameAjuLaser, text="%", fg = self.fuente, ).grid(column=5, row=2, sticky=NSEW, padx=0, pady=0)
                        
        ##############################
        #       FRAME de Avance
        ##############################
        FrameAvance = Frame(self,bg="#A0FBFB")
        FrameAvance.place(relx=0.25,rely=0.35)#relwidth=0.2, relheight=0.09

        Label(FrameAvance, text="Avance", fg = self.fuente).grid(columnspan=4, row=0, sticky=NSEW, padx=0, pady=0)
        
        self.AvanP=Button(FrameAvance, text="A +", fg = self.fuente, command =lambda: self.fnAvance(0))
        self.AvanP.grid(column=0, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.AvanN=Button(FrameAvance, text="A -", fg = self.fuente, command =lambda: self.fnAvance(1))
        self.AvanN.grid(column=1, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.ValAv=Entry(FrameAvance, width=7, textvariable=self.Avance, justify=RIGHT, bg="#CDF7C8", fg = self.fuente)
        self.ValAv.grid(column=2, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        Label(FrameAvance, text="mm", fg = self.fuente, ).grid(column=3, row=1, sticky=NSEW, padx=0, pady=0)

        Label(FrameAvance, text="V. de Avance", fg = self.fuente).grid(columnspan=2, row=2, sticky=NSEW, padx=0, pady=0)
        
        self.FeedRate = ttk.Combobox(FrameAvance, values=self.feedrate, justify=RIGHT, width=4)
        self.FeedRate.grid(column = 2, columnspan=1, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        self.FeedRate.current(8)
        Label(FrameAvance, text="mm/min", fg = self.fuente, ).grid(column=3, row=2, sticky=NSEW, padx=0, pady=0)
            
        ##############################
        #       FRAME Encender Láser
        ##############################
        FrameEncLaser = Frame(self,bg="#A0FBFB")
        FrameEncLaser.place(relx=0.24,rely=0.23)#relwidth=0.2, relheight=0.09

        self.Encender=Button(FrameEncLaser, text="Encender Láser a 5%", fg = self.fuente, command = self.FnEncLaser)
        self.Encender.grid(column=0, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)

        # self.Apagar=Button(FrameEncLaser, text="Apagar Láser", fg = self.fuente, command = lambda: self.FnEncLaser(0))
        # self.Apagar.grid(column=0, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)

        ##############################
        #       FRAME de Coordenadas
        ##############################
        FrameCoo = Frame(self)
        FrameCoo.place(relx=0.25,rely=0.58)#,relwidth=0.2, relheight=0.15
        
        PosX = Button(FrameCoo, text="Coordena X", fg=self.fuente, bg=BLabelPos, command =lambda: self.fnCoo('X'))
        PosX.grid(column=0, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        PosY = Button(FrameCoo, text="Coordena Y", fg=self.fuente, bg=BLabelPos, command =lambda: self.fnCoo('Y'))
        PosY.grid(column=0, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        PosZ = Button(FrameCoo, text="Coordena Z", fg=self.fuente, bg=BLabelPos, command =lambda: self.fnCoo('Z'))
        PosZ.grid(column=0, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.CooX = Entry(FrameCoo, width=7, textvariable=self.ValX, justify=RIGHT, fg=self.fuente , bg=BLabelCoo)
        self.CooX.grid(column=1, row=0, sticky=NSEW, padx=0, pady=0)
        Label(FrameCoo, text="mm", fg = self.fuente).grid(column=3, row=0, sticky=NSEW, padx=0, pady=0)

        self.CooY = Entry(FrameCoo, width=4, textvariable=self.ValY, justify=RIGHT, fg=self.fuente , bg=BLabelCoo)
        self.CooY.grid(column=1, row=1, sticky=NSEW, padx=0, pady=0)
        Label(FrameCoo, text="mm", fg = self.fuente).grid(column=3, row=1, sticky=NSEW, padx=0, pady=0)
                
        self.CooZ = Entry(FrameCoo, width=7, textvariable=self.ValZ, justify=RIGHT, fg=self.fuente , bg=BLabelCoo)
        self.CooZ.grid(column=1, row=2, sticky=NSEW, padx=0, pady=0)
        Label(FrameCoo, text="mm", fg = self.fuente).grid(column=3, row=2, sticky=NSEW, padx=0, pady=0)

        ##############################
         #       FRAME de Ejes
        ##############################
        FrameEjes = Frame(self)
        FrameEjes.place(relx=0.025,rely=0.58)#,relwidth=0.22, relheight=0.15
        ################
        self.botonXnYp=Button(FrameEjes, text="X-Y+", fg = self.fuente, bg=BLabelDP2, command=lambda:self.fnMovPar('X', 0, 'Y', 1))
        self.botonXnYp.grid(column=0, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.botonYp=Button(FrameEjes, text="Y+", fg = self.fuente, bg=BLabelDP1, command=lambda:self.fnMov('Y', 1, 0))
        self.botonYp.grid(column=1, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.botonXpYp=Button(FrameEjes, text="X+Y+", fg = self.fuente, bg=BLabelDP2, command=lambda:self.fnMovPar('X', 1, 'Y', 1))
        self.botonXpYp.grid(column=2, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        ################
        self.botonXn=Button(FrameEjes, text="X-", fg = self.fuente, bg=BLabelDP1, command=lambda:self.fnMov('X', 0, 0))
        self.botonXn.grid(column=0, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.botonHome=Button(FrameEjes, text="Home", fg = self.fuente, bg=BLabelDH, command=self.fnHome)
        self.botonHome.grid(column=1, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.botonXp=Button(FrameEjes, text="X+", fg = self.fuente, bg=BLabelDP1, command=lambda:self.fnMov('X', 1, 0))
        self.botonXp.grid(column=2, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        ################
        self.botonXnYn=Button(FrameEjes, text="X-Y-", fg = self.fuente, bg=BLabelDP2, command=lambda:self.fnMovPar('X', 0, 'Y', 0))
        self.botonXnYn.grid(column=0, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)   
             
        self.botonYn=Button(FrameEjes, text="Y-", fg = self.fuente, bg=BLabelDP1, command=lambda:self.fnMov('Y', 0, 0))
        self.botonYn.grid(column=1, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.botonXpYn=Button(FrameEjes, text="X+Y-", fg = self.fuente, bg=BLabelDP2, command=lambda:self.fnMovPar('X', 1, 'Y', 0))
        self.botonXpYn.grid(column=2, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        ################        
        self.botonZp=Button(FrameEjes, text="Z+", fg = self.fuente, bg=BLabelDP1, command=lambda:self.fnMov('Z', 1, 0))
        self.botonZp.grid(column=3, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.botonZn=Button(FrameEjes, text="Z-", fg = self.fuente, bg=BLabelDP1, command=lambda:self.fnMov('Z', 0, 0))
        self.botonZn.grid(column=3, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        
         #       FRAME de Numero
        # FrameNum = Frame(self,bg="#D4FBA0" )
        # FrameNum.place(relx=0.6,rely=0.475,relwidth=0.15, relheight=0.208)
        
        # FrameNum.columnconfigure(0, weight=1)
        # FrameNum.columnconfigure(1, weight=1)
        # FrameNum.columnconfigure(2, weight=1)
                
        # self.boton1=Button(FrameNum, text="  1  ", fg = self.fuente, command=self.fnMov)
        # self.boton1.grid(column=0, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.boton2=Button(FrameNum, text="  2  ", fg = self.fuente, command=self.fnMov)
        # self.boton2.grid(column=1, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.boton3=Button(FrameNum, text="  3  ", fg = self.fuente, command=self.fnMov)
        # self.boton3.grid(column=2, row=0, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.boton4=Button(FrameNum, text="  4  ", fg = self.fuente, command=self.fnMov)
        # self.boton4.grid(column=0, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.boton5=Button(FrameNum, text="  5  ", fg = self.fuente, command=self.fnMov)
        # self.boton5.grid(column=1, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.boton6=Button(FrameNum, text="  6  ", fg = self.fuente, command=self.fnMov)
        # self.boton6.grid(column=2, row=1, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.boton7=Button(FrameNum, text="  7  ", fg = self.fuente, command=self.fnMov)
        # self.boton7.grid(column=0, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.boton8=Button(FrameNum, text="  8  ", fg = self.fuente, command=self.fnMov)
        # self.boton8.grid(column=1, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.boton9=Button(FrameNum, text="  9  ", fg = self.fuente, command=self.fnMov)
        # self.boton9.grid(column=2, row=2, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.botonBorrar=Button(FrameNum, text="  <- ", fg = self.fuente, command=self.fnMov)
        # self.botonBorrar.grid(column=0, row=3, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.boton0=Button(FrameNum, text="  0  ", fg = self.fuente, command=self.fnMov)
        # self.boton0.grid(column=1, row=3, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
        # self.botonEnter=Button(FrameNum, text="Enter", fg = self.fuente, command=self.fnMov)
        # self.botonEnter.grid(column=2, row=3, sticky=NSEW, padx=0, pady=0, ipadx=0, ipady=0)
 
ancho_ventana = 800
alto_ventana = 500
    
root = Tk()
x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
root.wm_title("CNC Láser ''PT''")
posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
root.geometry(posicion)
app = CNCInt(root) 
app.mainloop()