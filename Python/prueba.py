import math

def Tor_Motor(d_carga, L_theta, D_total, f_0, t_acel, t_total, M_soporte, e, Longitud, Densidad, Diametro, mu_superficie, F_externa, F_gravedad):
	# Resolución de la posición de la carga

	Theta_paso = (d_carga / i) / L_theta

	# Determine el perfil del movimiento

	P_total = (D_total / (d_carga / i)) * Theta_paso
	#print("Total de pulsos = ", P_total)
	f_trape = (P_total - (f_0 * t_acel)) /  (t_total - t_acel)
	V_eje = f_trape * (60 / 200)	# RPM

	#	Torque necesario para mover la carga

	J_W = (M_soporte / e) * pow((1 / (2 * math.pi * (1000 / d_carga))),2)
	J_tornillo = (math.pi * Longitud * Densidad * pow(Diametro/2,4)) / 2
	J_total = (J_tornillo + J_W) / pow(i,2)

	T_acel = J_total * (f_trape / t_acel) * 2 * math.pi / 60

	F_friccion = mu_superficie * M_soporte* math.cos(Theta) * 9.81
	F_total = F_externa + F_friccion + F_gravedad

	T_resis = (F_total / (2 * math.pi * (1000 / d_carga))) / 2

	T_movimiento = T_acel + T_resis

	return T_movimiento,  J_total, f_trape, t_acel, T_resis
	# 	Seleccione y confirme el sistema del motor/accionamiento

def Tor_Mot_Fin(T_movimiento, J_total, f_trape, t_acel, T_resis, J_motor):
	# Resolución de la posición de la carga

	T_acel = (J_total + J_motor) * (f_trape / t_acel) * 2 * math.pi / 60

	T_movimiento = T_acel + T_resis

	return T_movimiento

Theta = 0	# Grados
F_externa = 0	# Newtons
F_gravedad = 0	# Newtons

# EJe Z
					  	#[m]			  #[m]
Tornillo_Z = {'Diametro': 0.020, 'Longitud': 0.4, 'Densidad': 7700, 'e': 0.9}
Motor_Z = {'Masa': 0.362, 'J' :0.0002157  + 0.0004127 + 0.0004127}
Soport_Z = {'Masa': 0.48, 'J':0.002 + 0.002 + 0.003}
Laser = {'Masa': 4, 'J':0.003 + 0.027 + 0.027}

M_tornillo_Z = Tornillo_Z['Diametro'] * math.pi * Tornillo_Z['Longitud'] * Tornillo_Z['Densidad']

Masa_Z = M_tornillo_Z + Motor_Z['Masa'] + Soport_Z['Masa'] + Laser['Masa']
J_eje_Z = Motor_Z['J'] + Soport_Z['J'] + Laser['J']

# Eje X

Tornillo_X = {'Diametro': 0.020, 'Longitud': 1.2, 'Densidad': 7700, 'e': 0.9}
Soport_X = {'Masa': 0.48, 'J':0.002 + 0.002 + 0.003}
Motor_X = {'Masa': 0.362, 'J' :0.0002157  + 0.0004127 + 0.0004127}

M_tornillo_X = Tornillo_X['Diametro'] * math.pi * Tornillo_X['Longitud'] * Tornillo_X['Densidad'] 

Masa_X = M_tornillo_X + Motor_X['Masa'] + Soport_X['Masa'] + Masa_Z
J_eje_X = Motor_X['J'] + Soport_X['J'] + J_eje_Z

Banda_X = {'Masa': 0.362, 'J' :0.0002157  + 0.0004127 + 0.0004127}
Larguero_X = {'Masa': 6.887, 'J':0.005 + 1.292 + 1.296}

# Eje Y

Tornillo_Y = {'Diametro': 0.020, 'Longitud': 2.4, 'Densidad': 7700, 'e': 0.9}
Soport_Y = {'Masa': 1.09, 'J':0.004 + 0.004 + 0.007}
Motor_Y = {'Masa': 0.362, 'J':0.0002157 + 0.0004127 + 0.0004127}

M_tornillo_Y = Tornillo_Y['Diametro'] * math.pi * Tornillo_Y['Longitud'] * Tornillo_Y['Densidad'] 

Masa_Y = M_tornillo_Y + Motor_Y['Masa'] + Soport_Y['Masa'] + Masa_X
J_eje_Y = Motor_Y['J'] + Soport_Y['J'] + J_eje_X

L_theta_xy = 0.0254	# Resolución deseada  [mm/paso]
L_theta_z = 0.1

i = 1	# Relacion del reductor de engranaje
D_total = 120 	# Movimiento [mm]	

d_carga = 16 # mm/rev (pitch = 0,0625 rev/mm o 62,5 rev/m)
mu_superficie = 0.05 
t_total = 1.7	# Tiempo del moviemiento [seg]
t_acel = t_total / 4	# Tiempo de aceleracion (25% del tiempo total)
f_0 = 40	# Frecuencia inicial de partida

Tor_Motor_Z, J_total_Z, f_trape_Z, t_acel_Z, T_resis_Z = Tor_Motor(d_carga, L_theta_z, D_total, f_0, t_acel, t_total, Soport_Z['Masa'], Tornillo_Z['e'], Tornillo_Z['Longitud'], Tornillo_Z['Densidad'], Tornillo_Z['Diametro'], mu_superficie, F_externa, F_gravedad)
print("Torque inicial eje Z = ", Tor_Motor_Z)

Tor_Motor_X, J_total_X, f_trape_X, t_acel_X, T_resis_X = Tor_Motor(d_carga, L_theta_xy, D_total, f_0, t_acel, t_total, Soport_X['Masa'], Tornillo_X['e'], Tornillo_X['Longitud'], Tornillo_X['Densidad'], Tornillo_X['Diametro'], mu_superficie, F_externa, F_gravedad)
print("Torque inicial eje X = ", Tor_Motor_X)

Tor_Motor_Y, J_total_Y, f_trape_Y, t_acel_Y, T_resis_Y = Tor_Motor(d_carga, L_theta_xy, D_total, f_0, t_acel, t_total, Soport_Y['Masa'], Tornillo_Y['e'], Tornillo_Y['Longitud'], Tornillo_Y['Densidad'], Tornillo_Y['Diametro'], mu_superficie, F_externa, F_gravedad)
print("Torque inicial eje Y = ", Tor_Motor_Y/2)


#		Motor STP-MTR-23055
print("Torque con motor seleccionado eje Z =", Tor_Mot_Fin(Tor_Motor_Z, J_total_Z, f_trape_Z, t_acel_Z, T_resis_Z, 0.000027), "N-m")

#		Motor STP-MTR-23079
print("Torque con motor seleccionado eje X =", Tor_Mot_Fin(Tor_Motor_X, J_total_X, f_trape_X, t_acel_X, T_resis_X, 0.000047), "N-m")

#		Motor STP-MTR-34066
# DAdo que el eje Y se repartira en dos motores seria un Tor_Motor/2 
print("Torque con motor seleccionado eje Y =", Tor_Mot_Fin(Tor_Motor_Y/2, J_total_Y, f_trape_Y, t_acel_Y, T_resis_Y, 0.00014), "N-m")