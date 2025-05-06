"""
Práctica 3: Sistema Cardiovascular

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Mariana Rivera Peñuelas
Número de control: 22210427
Correo institucional: l22210427@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
#!pip install control
#!pip install slycot
import control as ctrl

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import matplotlib.pyplot as plt
import math

x0, t0, tF, dt, w, h = 0,0,10,1E-3,10,5
N = round((tF-t0)/dt)+1
t = np.linspace(t0, tF, N)
u = np.sin(2*math.pi*95/60*t) + 0.8

Signal = ["Sistema_cardiovascular","Hipertenso","Hipotenso"]
def cardio (Z, C, R, L):
    num =[L*R, R*Z]
    den = [C*L*R*Z, L*R+L*Z, R*Z]
    sys = ctrl.tf(num, den)
    return sys

#Funcion de transferencia: individuo hipotenso(caso)
Z, C, R, L =  0.020, 0.250, 0.600, 0.005
sysT = cardio (Z, C, R, L)
print ('INDIVIDUO HIPOTENSO[CASO]:')
print (sysT)

#Funcion de transferencia: individuo normotenso(caso)
Z, C, R, L = 0.033, 1.500, 0.950, 0.010
sysN = cardio (Z, C, R, L)
print ('INDIVIDUO NORMOTENSO[CONTROL]:')
print (sysN)

#Funcion de transferencia: individuo hipertenso(caso)
Z, C, R, L = 0.050, 2.500, 1.400, 0.020
sysH = cardio (Z, C, R, L)
print ('INDIVIDUO HIPERTENSO[CASO]:')
print (sysH)  

#Sistema cardiovascular
def senales(u,sysT,sysN,sysH,Signal):
    fig=plt.figure()
    
    if Signal=="Sistema_cardiovascular":
        ts,Vs=ctrl.forced_response(sysT,t,u,x0)
        plt.plot(ts,Vs, '--', color =  [252/255, 199/255, 55/255], label = '$P_p(t): Hipotenso$')
        ts,Ve=ctrl.forced_response(sysN,t,u,x0)
        plt.plot(ts,Ve, '-', color =  [242/255, 107/255, 15/255], label = '$P_p(t): Normotenso$')
        ts,Vd=ctrl.forced_response(sysH,t,u,x0)
        plt.plot(ts,Vd, ':', color= [126/255, 24/255, 145/255], label = '$P_p(t): Hipertenso$')
        
    elif Signal=="Hipotenso":
        ts,Ve=ctrl.forced_response(sysT,t,u,x0)
        plt.plot(ts,Ve, '-', color =  [252/255, 199/255, 55/255], label = '$P_p(t): Control$')
        ts,Vd=ctrl.forced_response(sysN,t,u,x0)
        plt.plot(ts,Vd, ':', color= [126/255, 24/255, 145/255], label = '$P_p(t): Hipotenso$')
        ts,pid=ctrl.forced_response(sysH,t,u,x0)
        plt.plot(ts,pid, ':',linewidth=3, color =  [242/255, 107/255, 15/255], label = '$Pa(t): Tratamiento$')
        
    elif Signal=="Hipertenso":
        ts,Ve=ctrl.forced_response(sysT,t,u,x0)
        plt.plot(ts,Ve, '-', color =  [252/255, 199/255, 55/255], label = '$P_p(t): Control$')
        ts,Vd=ctrl.forced_response(sysN,t,u,x0)
        plt.plot(ts,Vd, ':', color= [126/255, 24/255, 145/255], label = '$P_p(t): Hipertenso$')
        ts,pid=ctrl.forced_response(sysH,t,u,x0)
        plt.plot(ts,pid, ':',linewidth=3, color =  [242/255, 107/255, 15/255], label = '$Pa(t): Tratamiento$')

    plt.grid(False)
    plt.xlim(0,10)
    plt.ylim(-0.5,2)
    plt.xticks(np.arange(0,10,1))
    plt.yticks(np.arange(-0.5,2,.5))
    plt.xlabel('$t$ [s]',fontsize=11)
    plt.ylabel('$Pp(t)$ [V]',fontsize=11)
    plt.legend(bbox_to_anchor=(0.5,-0.3),loc='center',ncol=4, fontsize=8,frameon=False)
    plt.show()
    fig.set_size_inches(20,5)
    fig.tight_layout()
    namepng='Python_'+Signal+ '.png'
    namepdf='Python_'+Signal+ '.pdf'
    fig.savefig(namepng,dpi=600,bbox_inches='tight')
    fig.savefig(namepdf,bbox_inches='tight')
    fig.savefig('.pdf',bbox_inches='tight')

def tratamiento (sys): 
        Cr=10E-6
        Ki=1302.6562045662
        Kp=9.10544741022521e-05
        Re=1/(Ki*Cr)
        Rr=Kp*Re
        numPI=[Rr*Cr,1]
        denPI=[Re*Cr,0]
        PID=ctrl.tf(numPI,denPI)
        X = ctrl.series(PID,sysN)
        sys=ctrl.feedback(X,1,sign=-1)
        return sys
    
#Sistema de control en lazo cerrado
sysPID=tratamiento(sysH)
senales(u,sysT,sysN,sysH,"Sistema_cardiovascular")
senales(u,sysN,sysT,sysPID,"Hipotenso")
senales(u,sysN,sysH,sysPID,"Hipertenso")

