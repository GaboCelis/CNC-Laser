import math
#comentario agregado

def Tor_Motor(d_carga, L_theta, D_total, f_0, t_acel, t_total, Masa_t, mu_superficie, F_externa, F_gravedad, J_total):
	
	# Resolución de la posición de la carga
	Theta_paso = (d_carga / i) / L_theta

	# Determine el perfil del movimiento
	P_total = (D_total / (d_carga / i)) * Theta_paso
	print("Total de pulsos = ", P_total)
	f_trape = (P_total - (f_0 * t_acel)) /  (t_total - t_acel)
	V_eje = f_trape * (60 / 200)	# RPM
	print("Total de RPM = ", V_eje)

	#	Torque necesario para mover la carga
	T_acel = J_total * (f_trape / t_acel) * 2 * math.pi / 60

	F_friccion = mu_superficie * Masa_t * math.cos(Theta) * 9.81
	F_total = F_externa + F_friccion + F_gravedad

	T_resis = (F_total / (2 * math.pi * (1000 / d_carga))) / 2

	T_movimiento = T_acel + T_resis

	return T_movimiento, f_trape, t_acel, T_resis
	# 	Seleccione y confirme el sistema del motor/accionamiento

def Tor_Mot_Fin(T_movimiento, J_total, f_trape, t_acel, T_resis, J_motor):
	# Resolución de la posición de la carga

	T_acel = (J_total + J_motor) * (f_trape / t_acel) * 2 * math.pi / 60

	T_movimiento = T_acel + T_resis

	return T_movimiento

Theta = 0	# Grados
F_externa = 0	# Newtons
F_gravedad = 0	# Newtons

L_theta_xy = 0.03	# Resolución deseada  [mm/paso]
L_theta_z = 0.05
dZ_carga = 2 # mm/rev
dXY_carga = 50.26
i = 1	# Relacion del reductor de engranaje
D_total = 120 	# Movimiento [mm]	


mu_superficie = 0.05 
t_total = 2	# Tiempo del moviemiento [seg]
t_acel = t_total / 4	# Tiempo de aceleracion (25% del tiempo total)
f_0 = 40	# Frecuencia inicial de partida

# EJe Z
					  	#[m]			  #[m]
e_Z = 0.9
Tornillo_Z = {'Diametro': 0.0080, 'Longitud': 0.14, 'Densidad': 7700, 'e': 0.9}
M_tornillo_Z = Tornillo_Z['Diametro'] * math.pi * Tornillo_Z['Longitud'] * Tornillo_Z['Densidad']
Motor_Z = {'Masa': 0.115, 'J' :0.00003283}
Soport_Z = {'Masa': 0.404, 'J':0.0001502}
Laser = {'Masa': 0.477, 'J':0.000798}

Masa_Z = Motor_Z['Masa'] + Soport_Z['Masa'] + Laser['Masa']

J_WX = (Masa_Z / e_Z) * pow((1 / (2 * math.pi * (1000 / dZ_carga))),2)
J_tornillo = (math.pi * Tornillo_Z['Longitud'] * Tornillo_Z['Densidad'] * pow(Tornillo_Z['Diametro']/2,4)) / 2
JZ_total = (J_tornillo + J_WX) / pow(i,2)


# Eje Y

e_Y = 0.9
Soport_Y = {'Masa': 1.562, 'J':0.006}
Componentes_Z = {'Masa': Masa_Z, 'J':JZ_total}
Motor_Y = {'Masa': 0.644, 'J':0.0003278}

Masa_Y = Motor_Y['Masa'] + Soport_Y['Masa'] + Componentes_Z['Masa']

J_WY = (Masa_Z / e_Y) * pow((1 / (2 * math.pi * (1000 / dXY_carga))),2)
JY_total = (J_WY) / pow(i,2)

# Eje X

e_X = 0.9
Soport_X = {'Masa': 0.619, 'J':0.005}
Componentes_Y = {'Masa': 2.206, 'J':0.013}
Eje_X = {'Masa': 0.81, 'J':0.004}
Motor_X = {'Masa': 0.644, 'J' :0.0003278}

Masa_X =  (2 * Motor_X['Masa']) + Soport_X['Masa'] + Componentes_Y['Masa'] # + M_tornillo_X

J_WX = (Masa_X / e_X) * pow((1 / (2 * math.pi * (1000 / dXY_carga))),2)
JX_total = (J_WX) / pow(i,2)

Tor_Motor_Z, f_trape_Z, t_acel_Z, T_resis_Z = Tor_Motor(dZ_carga, L_theta_z, D_total, f_0, t_acel, t_total, Masa_Z, mu_superficie, F_externa, F_gravedad, JZ_total)
print("Torque inicial eje Z = ", Tor_Motor_Z, "N-m")

Tor_Motor_Y, f_trape_Y, t_acel_Y, T_resis_Y = Tor_Motor(dXY_carga, L_theta_xy, D_total, f_0, t_acel, t_total, Masa_Y,mu_superficie, F_externa, F_gravedad, JY_total)
print("Torque inicial eje Y = ", Tor_Motor_Y, "N-m")

Tor_Motor_X, f_trape_X, t_acel_X, T_resis_X = Tor_Motor(dXY_carga, L_theta_xy, D_total, f_0, t_acel, t_total, Masa_Z,mu_superficie, F_externa, F_gravedad, JX_total)
print("Torque inicial eje X = ", Tor_Motor_X, "N-m")


#		Motor STP-MTR-17048
print("Torque con motor seleccionado eje Z =", Tor_Mot_Fin(Tor_Motor_Z, JZ_total, f_trape_Z, t_acel_Z, T_resis_Z, 0.0000068), "N-m")

#		Motor STP-MTR-23055
print("Torque con motor seleccionado eje X =", Tor_Mot_Fin(Tor_Motor_Y, JY_total, f_trape_Y, t_acel_Y, T_resis_Y, 0.000027), "N-m")

#		Motor STP-MTR-23055
# DAdo que el eje Y se repartira en dos motores seria un Tor_Motor/2 
print("Torque con motor seleccionado eje Y =", Tor_Mot_Fin(Tor_Motor_X/2, JX_total, f_trape_X, t_acel_X, T_resis_X, 0.000027), "N-m")