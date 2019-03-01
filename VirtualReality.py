import pandas as pd,numpy as np,matplotlib.pyplot as plt,math as m

"""

    Question1

"""

"Read/import"

data=pd.read_csv("IMUData.csv", delimiter=',')

time=data["time"].values

gyroX=np.deg2rad(data[" gyroscope.X"].values)
gyroY=np.deg2rad(data[" gyroscope.Y"].values)
gyroZ=np.deg2rad(data[" gyroscope.Z"].values)


acceX=data[" accelerometer.X"].values#[1:]
acceY=data[" accelerometer.Y"].values
acceZ=data[" accelerometer.Z"].values

magnX=data[" magnetometer.X"].values
magnY=data[" magnetometer.Y"].values
magnZ=data[" magnetometer.Z "].values

"Convert and normalize"
def magnitudeFinder(x,y,z):
    return np.sqrt((x * x) + (y * y) + (z * z))

acceM=magnitudeFinder(acceX,acceY,acceZ)

magnM=magnitudeFinder(magnX,magnY,magnZ)

acceNX=acceX/acceM#check divide by 0
acceNY=acceY/acceM
acceNZ=acceZ/acceM
magnNX=magnX/magnM
magnNY=magnY/magnM
magnNZ=magnZ/magnM

"i)"
"to euler angles"
eulerAngs=[]
for each in range(1,len(time)):#0
    t=time[each]-time[each-1]
    eulerAngs.append([t*gyroX[each],t*gyroY[each],t*gyroZ[each]])
    #phi,theta,psi



# plt.plot(time[1:],eulerAngs)
# plt.show()
"to quaternions"
def toQuaternions(vx,vy,vz,theta):
    m.cos(theta/2), vx*m.sin(theta/2), vy*m.sin(theta/2), vz*m.sin(theta/2)
    return [m.cos(theta/2), vx*m.sin(theta/2), vy*m.sin(theta/2), vz*m.sin(theta/2)]

quaternions=[]
for each in eulerAngs:
    theta=magnitudeFinder(each[0],each[1],each[2])
    quaternions.append(toQuaternions(each[0],each[1],each[2],theta))

# plt.plot(time[1:],quaternions)
# plt.show()
"ii)"
"back to Euler"
def toEuler(each):
    poles=each[1]*each[2] + each[3]*each[0]
    if poles != 0.5 and poles != -0.5:
        heading= m.atan2(2*each[2]*each[0]-2*each[1]*each[3] , 1 - 2*each[2]*each[2] - 2*each[3]*each[3])
        attitude = m.asin(2*poles)
        bank = m.atan2(2*each[1]*each[0]-2*each[2]*each[3] , 1 - 2*each[1]*each[1] - 2*each[3]*each[3])
    elif poles == 0.5:
        heading = 2*m.atan2(each[1],each[0])
        bank = 0
    elif poles == -0.5:
        heading = -2*m.atan2(each[1],each[0])
        bank = 0

    return [heading,attitude,bank]

toEu=[]
for each in quaternions:
    toEu.append(toEuler(each))

# plt.plot(time[1:],toEu)
# plt.show()

"iii)"
def conjQuot(each):
    return [each[0],-each[1],-each[2],-each[3]]

conjQ=[]
for each in quaternions:
    conjQ.append(conjQuot(each))

"iv)"

"quaternion product"
def qProd(q,r):#change?
    #https://uk.mathworks.com/help/aeroblks/quaternionmultiplication.html
    t0=r[0]*q[0]-r[1]*q[1]-r[2]*q[2]-r[3]*q[3]
    t1=r[0]*q[1]+r[1]*q[0]-r[2]*q[3]+r[3]*q[2]
    t2=r[0]*q[2]+r[1]*q[3]+r[2]*q[0]-r[3]*q[1]
    t3=r[0]*q[3]-r[1]*q[2]+r[2]*q[1]+r[3]*q[0]

    return [t0,t1,t2,t3]

"""

    Question2

"""
gyroM=magnitudeFinder(gyroX,gyroY,gyroZ)

gyroNX=(gyroX/gyroM)[1:]
gyroNY=(gyroY/gyroM)[1:]
gyroNZ=(gyroZ/gyroM)[1:]

theta=[]
for each in range(1,len(time)):#0
    t=time[each]-time[each-1]
    calc=t*gyroM[each]
    theta.append(calc)

# plt.plot(time[1:],theta)
# plt.show()

estimate=[[1,0,0,0]]

"X,Z,-Y"
for each in range(len(time)-1):#0
    qvt=toQuaternions(gyroNX[each],gyroNZ[each],-gyroNY[each],theta[each])#x,z,y
    estimate.append(qProd(estimate[each],qvt))


#xyz
#xzy---
#yzx
#yxz
#zyx
#zxy-

resxx=[]
resyx=[]
reszx=[]
# for each in estimate:
#     ress.append(toEuler(each))

"Phi"
for each in estimate:
    resxx.append(toEuler(each)[2])#
    resyx.append(-toEuler(each)[1])#- is important
    reszx.append(toEuler(each)[0])#

plt.plot(time,np.rad2deg(resxx),label="phiq2",color="black")#wrong spikes
plt.plot(time,np.rad2deg(resyx),label="thetaq2",color="blue")#semi
plt.plot(time,np.rad2deg(reszx),label="psiq2",color="yellow")#correct
plt.legend()
# plt.show()

"""

    Question3

    general remarks: recheck after all axis of gyro is correct

"""

"to global"
# def conjVquat(conj,v,quat):
#     return np.float64(conj)*v*np.float64(quat)

acceM=acceM[1:]

newconjQ=[]
for each in estimate:
    newconjQ.append(conjQuot(each))

globalA=[]
for each in range(len(acceM)):
    t=time[each+1]-time[each]
    calc=t*gyroM[each]#may change?
    avt=toQuaternions(acceX[each+1],acceY[each+1],acceZ[each+1],calc)#theta[each]
    # globalA.append(conjVquat(conjQ[each],acceM[each],quaternions[each]))#
    # last-globalA.append(qProd(qProd(conjQ[each],avt),quaternions[each]))#conjVquat(conjQ[each],acceM[each],quaternions[each]))#
    globalA.append(qProd(qProd(newconjQ[each],avt),estimate[each]))
"new theta? new phi,thet,psi check all again"
"check acceM shuld be q?"
"clarification needed to continue"

toEuAcce=[]
for each in globalA:
    toEuAcce.append(toEuler(each))

"calc tilt axis"
project=[]
# for each in globalA:
#     project.append(np.asarray([each[1],0,each[3]]))
for each in toEuAcce:
    project.append(np.asarray([each[0],0,each[2]]))
    "currently x,0,z  old: t=each[3],0,-each[1]  z,0,-x"
    "X,Z,-Y to Y,-Z,X"
    "hence might be 3,0,1?"



"phi angle"
phi=[]
phivec=np.asarray([0,1,0])
for each in toEuAcce:
    normEach=magnitudeFinder(each[0],each[1],each[2])
    phi.append(m.acos(np.dot(each,phivec) / normEach))
"dont forget the axis conversion again"
# print(phi)

"comp filter for acce correction"
alpha=0.01#0.0001
goodestimate=[]
for each in range(len(time)-1):#0
    qvt=toQuaternions(project[each][2],0,-project[each][0],-alpha*phi[each])#x
    goodestimate.append(qProd(qvt,estimate[each]))

resx=[]
resy=[]
resz=[]
# for each in estimate:
#     ress.append(toEuler(each))

"acce res"
for each in goodestimate:
    resx.append(toEuler(each)[2])#
    resy.append(-toEuler(each)[1])#- is important
    resz.append(toEuler(each)[0])#

plt.plot(time[1:],np.rad2deg(resx),label="phiq3",color="red")#wrong spikes
plt.plot(time[1:],np.rad2deg(resy),label="thetaq3",color="green")#semi
plt.plot(time[1:],np.rad2deg(resz),label="psiq3",color="purple")#correct
plt.legend()
plt.show()
