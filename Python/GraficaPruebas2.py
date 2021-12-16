from tkinter import Tk, Label, Button, Entry

ValX = 0
ValY = 0
ValZ = 0
Avance = 0.01

vent = Tk()
vent.title("CNC Láser ''PT''")
vent.geometry("800x500")

def fnAvance(Avan, opc):
    if opc == 1:
        if Avan <= 100:
            Avance=Avan*10 
        else:
            Avance=Avan
    else:
        if Avan >= 0.01:
            Avance = Avan/10
        else:
            Avance=Avan

def fnMov():
    n1 = txt1.get()
    n2 = txt2.get()
    r = float(n1) + float(n2)
    txt3.delete(0,'end')
    txt3.insert(0,r)

AvanP=Button(vent, text="A+", command = fnAvance(Avance, 0))
AvanN=Button(vent, text="A-", command = fnAvance(Avance, 1))
AvanP.place(relx=0.1, rely=0.4, relwidth=0.05, relheight=0.05)
AvanN.place(relx=0.15, rely=0.4, relwidth=0.05, relheight=0.05)

ValAv = Label(vent, text = Avance, bg="#CDF7C8")
ValAv.place(relx=0.2, rely=0.4, relwidth=0.1, relheight=0.05)

PosX = Label(vent, text="Coordena X", bg="#CDF7C8")
PosY = Label(vent, text="Coordena Y", bg="#CDF7C8")
PosZ = Label(vent, text="Coordena Z", bg="#CDF7C8")
PosX.place(relx=0.35, rely=0.5, relwidth=0.1, relheight=0.05)
PosY.place(relx=0.35, rely=0.55, relwidth=0.1, relheight=0.05)
PosZ.place(relx=0.35, rely=0.6, relwidth=0.1, relheight=0.05)

CooX = Label(vent, text=ValX , bg="#C8EBF7")
CooY = Label(vent, text=ValY , bg="#C8EBF7")
CooZ = Label(vent, text=ValZ , bg="#C8EBF7")
CooX.place(relx=0.45, rely=0.5, relwidth=0.05, relheight=0.05)
CooY.place(relx=0.45, rely=0.55, relwidth=0.05, relheight=0.05)
CooZ.place(relx=0.45, rely=0.6, relwidth=0.05, relheight=0.05)

txt1 = Entry(vent, bg="pink")
txt2 = Entry(vent, bg="pink")
txt3 = Entry(vent, bg="pink")
txt1.place(relx=0.3, rely=0.04, relwidth=0.22, relheight=0.05)
txt2.place(relx=0.3, rely=0.17, relwidth=0.22, relheight=0.05)
txt3.place(relx=0.3, rely=0.35, relwidth=0.22, relheight=0.05)

botonXp=Button(vent, text="X+", command=fnMov)
botonXn=Button(vent, text="X-", command=fnMov)
botonYp=Button(vent, text="Y+", command=fnMov)
botonYn=Button(vent, text="Y-", command=fnMov)
botonXpYp=Button(vent, text="X+Y+", command=fnMov)
botonXnYp=Button(vent, text="X-Y+", command=fnMov)
botonXnYn=Button(vent, text="X-Y-", command=fnMov)
botonXpYn=Button(vent, text="X+Y-", command=fnMov)
botonZp=Button(vent, text="Z+", command=fnMov)
botonZn=Button(vent, text="Z-", command=fnMov)
botonXp.place(relx=0.15, rely=0.55, relwidth=0.05, relheight=0.05)
botonXn.place(relx=0.05, rely=0.55, relwidth=0.05, relheight=0.05)
botonYp.place(relx=0.10, rely=0.5, relwidth=0.05, relheight=0.05)
botonYn.place(relx=0.10, rely=0.6, relwidth=0.05, relheight=0.05)
botonXpYp.place(relx=0.15, rely=0.5, relwidth=0.05, relheight=0.05)
botonXnYp.place(relx=0.05, rely=0.5, relwidth=0.05, relheight=0.05)
botonXnYn.place(relx=0.05, rely=0.6, relwidth=0.05, relheight=0.05)
botonXpYn.place(relx=0.15, rely=0.6, relwidth=0.05, relheight=0.05)
botonZp.place(relx=0.25, rely=0.5, relwidth=0.05, relheight=0.05)
botonZn.place(relx=0.25, rely=0.6, relwidth=0.05, relheight=0.05)


vent.mainloop()