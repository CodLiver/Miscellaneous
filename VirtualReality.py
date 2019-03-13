import pandas as pd,numpy as np,matplotlib.pyplot as plt,math as m,time as tt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation


"""
    Question1
"""

def readData(name):
    "reads CSV file which was delimited with ,"
    return pd.read_csv(name, delimiter=',')

def degToRad(data):
    "inputs the numpy array with degree values, converts to radians"
    return np.deg2rad(data)

def magnitudeFinder(x,y,z):
    "Find the magnitude of x,y,z components"
    return np.sqrt((x * x) + (y * y) + (z * z))

def normalizer(comp,magn):
    "returns the normalized version in numpy arrays, checks NaN's"
    norm=[]
    for each in range(len(comp)):
        if magn[each]!=0:
            norm.append(comp[each]/magn[each])
        else:
            norm.append(0)
    # without checking nan:
    # return comp/magn
    return norm

"Question 1)i)"
def toQuaternions(vx,vy,vz,theta):
    "According to [1], the implementation of quaternion convertion. Inputs x,y,z component and theta, returns [w,x,y,z]"
    m.cos(theta/2), vx*m.sin(theta/2), vy*m.sin(theta/2), vz*m.sin(theta/2)
    return [m.cos(theta/2), vx*m.sin(theta/2), vy*m.sin(theta/2), vz*m.sin(theta/2)]

"Question 1)ii)"
def toEuler(each):
    "Inputs each quaternion list [w,x,y,z], and returns their [psi,theta,phi] euler convertion. According to www."
    poles=each[1]*each[2] + each[3]*each[0]
    if poles <= 0.5 and poles >= -0.5:
        heading= m.atan2(2*each[2]*each[0]-2*each[1]*each[3] , 1 - 2*each[2]*each[2] - 2*each[3]*each[3])
        attitude = m.asin(2*poles)
        bank = m.atan2(2*each[1]*each[0]-2*each[2]*each[3] , 1 - 2*each[1]*each[1] - 2*each[3]*each[3])
    elif poles > 0.5:
        heading = 2*m.atan2(each[1],each[0])
        attitude = m.asin(poles)#ereasable
        bank = 0
    elif poles < -0.5:
        heading = -2*m.atan2(each[1],each[0])
        attitude = m.asin(poles)#ereasable
        bank = 0

    return [heading,attitude,bank]

"Question 1)iii)"
def conjQuot(each):
    "Converts quaternion to its conjugate [q,x,y,z] -> [q,-x,-y,-z]"
    return [each[0],-each[1],-each[2],-each[3]]

"Question 1)iv)"
def qProd(q,r):
    "Inputs Quaternion Q and Quaternion R, quaternion multiplies q*r"
    #https://uk.mathworks.com/help/aeroblks/quaternionmultiplication.html
    t0=r[0]*q[0]-r[1]*q[1]-r[2]*q[2]-r[3]*q[3]
    t1=r[0]*q[1]+r[1]*q[0]-r[2]*q[3]+r[3]*q[2]
    t2=r[0]*q[2]+r[1]*q[3]+r[2]*q[0]-r[3]*q[1]
    t3=r[0]*q[3]-r[1]*q[2]+r[2]*q[1]+r[3]*q[0]
    return [t0,t1,t2,t3]

def question1():
    "Question 1)i)"
    "finds euler angle"
    eulerAngs=[]
    for each in range(1,len(time)):#0
        t=time[each]-time[each-1]
        eulerAngs.append([t*gyroX[each],t*gyroY[each],t*gyroZ[each]])

    "converts euler angles to quaternions"
    quaternions=[]
    for each in eulerAngs:
        theta=magnitudeFinder(each[0],each[1],each[2])
        quaternions.append(toQuaternions(each[0],each[1],each[2],theta))

    "Question 1)ii)"
    "converts quaternions back to euler angles"
    toEu=[]
    for each in quaternions:
        toEu.append(toEuler(each))

    "Question 1)iii)"
    "converts quaternions to their conjugates"
    conjQ=[]
    for each in quaternions:
        conjQ.append(conjQuot(each))

    "Question 1)iv) can seen in qProd(q,r) func"


"""
    Question2
"""

def deadReckoningFilter():
    "Dead Reckoning filter uses gyrometer reading to estimate position, returns estimate in quaternion"

    "gyroscope normalization"
    gyroM=magnitudeFinder(gyroX,gyroY,gyroZ)

    gyroNX=(gyroX/gyroM)[1:]
    gyroNY=(gyroY/gyroM)[1:]
    gyroNZ=(gyroZ/gyroM)[1:]

    "get the theta to convert to quaternion"
    theta=[]
    for each in range(1,len(time)):#0
        t=time[each]-time[each-1]
        calc=t*gyroM[each]
        theta.append(calc)

    estimate=[[1,0,0,0]]

    "implement drf estimation with init quaternion."
    for each in range(len(time)-1):#0
        qvt=toQuaternions(gyroNX[each],gyroNZ[each],-gyroNY[each],theta[each])#x,z,y
        estimate.append(qProd(estimate[each],qvt))

    "drawing dead reckoning filter results"
    resxx=[]
    resyx=[]
    reszx=[]

    for each in estimate:
        resxx.append(toEuler(each)[2])
        resyx.append(-toEuler(each)[1])
        reszx.append(toEuler(each)[0])

    resDRF=[resxx,resyx,reszx]

    # plt.plot(time,np.rad2deg(resxx),label="phiq2",color="black")
    # plt.plot(time,np.rad2deg(resyx),label="thetaq2",color="blue")
    # plt.plot(time,np.rad2deg(reszx),label="psiq2",color="gray")
    # plt.legend()
    # plt.show()

    "returns drf estimate result"
    return estimate,gyroM,resDRF

"""
    Question3
"""

def tiltCorrection(estimate,alpha,acceM,gyroM):
    "tilt correction with accelerometer as part of question 3"

    "to find the conjugate of drf estimation for fusing"
    newconjQ=[]
    for each in estimate:
        newconjQ.append(conjQuot(each))


    "to convert the accelerometer data to global frame"
    acceM=acceM[1:]
    globalA=[]
    for each in range(len(acceM)):
        t=time[each+1]-time[each]
        calc=t*gyroM[each]#may change?
        avt=toQuaternions(acceX[each+1],acceY[each+1],acceZ[each+1],calc)
        globalA.append(qProd(qProd(newconjQ[each],avt),estimate[each]))

    "convert global data to euler forma again"
    toEuAcce=[]
    for each in globalA:
        toEuAcce.append(toEuler(each))

    "calculate tilt axis"
    project=[]
    tiltax=[]
    for each in toEuAcce:
        project.append(np.asarray([each[0],0,each[2]]))
        tiltax.append(np.asarray([each[2],0,-each[0]]))

    "phi angle"
    phi=[]
    phivec=np.asarray([0,1,0])
    for each in toEuAcce:
        normEach=magnitudeFinder(each[0],each[1],each[2])
        phi.append(m.acos(np.dot(each,phivec) / normEach))

    "complimentary filter for accelerometer correction"
    alpha=0.001
    goodestimate=[]
    for each in range(len(time)-1):
        qvt=toQuaternions(tiltax[each][0],0,tiltax[each][2],-alpha*phi[each])#x
        goodestimate.append(qProd(qvt,estimate[each]))


    "draw the tilt correction plot"
    resx=[]
    resy=[]
    resz=[]

    "acce res"
    for each in goodestimate:
        resx.append(toEuler(each)[2])
        resy.append(-toEuler(each)[1])
        resz.append(toEuler(each)[0])
    #
    # plt.plot(time[1:],np.rad2deg(resx),label="phiq3",color="cyan")
    # plt.plot(time[1:],np.rad2deg(resy),label="thetaq3",color="orange")
    # plt.plot(time[1:],np.rad2deg(resz),label="psiq3",color="magenta")
    # plt.legend()
    # plt.show()

    resTilt=[resx,resy,resz]
    return goodestimate,resTilt


"""
    Question4
"""

def yawCorrection(goodestimate,alpha,magnM):
    newMconjQ=[]
    for each in goodestimate:
        newMconjQ.append(conjQuot(each))

    "get magnetometer ref estimation calculation"
    mest=[]
    mdist=[]
    magnM=magnM[1:]
    mref=qProd(qProd(newMconjQ[0],toQuaternions(magnX[0],magnY[0],magnZ[0],time[1]*gyroM[0])),goodestimate[0])
    for each in range(len(magnM)):
        mest.append(qProd(qProd(newMconjQ[each],toQuaternions(magnX[each],magnY[each],magnZ[each],([each+1]-time[each])*gyroM[each])),goodestimate[each]))
        mEuRef=toEuler(mref)
        mEuEst=toEuler(mest[each])
        mdist.append(magnitudeFinder(mEuRef[0],mEuRef[1],mEuRef[2])-magnitudeFinder(mEuEst[0],mEuEst[1],mEuEst[2]))

    "get reference magnetometer, and do yaw correction"
    yawCfilt=[]
    thr=m.atan2(mref[1],mref[3])
    for each in range(len(time)-1):#0
        th=m.atan2(mest[each][1],mest[each][3])#x,z
        qvt=toQuaternions(0,1,0,-alpha*(th-thr))
        yawCfilt.append(qProd(qvt,goodestimate[each]))

    "yaw corrected result plotting"
    ressx=[]
    ressy=[]
    ressz=[]

    for each in yawCfilt:
        ressx.append(toEuler(each)[2])
        ressy.append(-toEuler(each)[1])
        ressz.append(toEuler(each)[0])

    # plt.plot(time[1:],np.rad2deg(ressx),label="phiq4",color="red")
    # plt.plot(time[1:],np.rad2deg(ressy),label="thetaq4",color="green")
    # plt.plot(time[1:],np.rad2deg(ressz),label="psiq4",color="purple")
    # plt.legend()
    # plt.show()

    resYaw=[ressx,ressy,ressz]

    return yawCfilt,resYaw


"""
    Question5
"""

def plotter(in1,in2,in3,divisor,alls):
    "plots the axis in real time"
    ends=len(in1)
    fig = plt.figure()

    ax11 = fig.add_subplot(3, 3, 1)
    ax11.plot(alls[0],np.rad2deg(alls[4][0]),label="gyroX",color="red")
    ax11.plot(alls[0],np.rad2deg(alls[4][1]),label="gyroY",color="green")
    ax11.plot(alls[0],np.rad2deg(alls[4][2]),label="gyroZ",color="purple")
    ax11.set_title('Gyroscope')
    plt.legend()
    ax12 = fig.add_subplot(3, 3, 2)
    ax12.plot(alls[0],alls[5][0],label="acceX",color="red")
    ax12.plot(alls[0],alls[5][1],label="acceY",color="green")
    ax12.plot(alls[0],alls[5][2],label="acceZ",color="purple")
    ax12.set_title('Accelerometer')
    plt.legend()
    ax13 = fig.add_subplot(3, 3, 3)
    ax13.plot(alls[0],alls[6][0],label="magnX",color="red")
    ax13.plot(alls[0],alls[6][1],label="magnY",color="green")
    ax13.plot(alls[0],alls[6][2],label="magnZ",color="purple")
    ax13.set_title('Magnetometer')
    plt.legend()
    ax11 = fig.add_subplot(3, 3, 4)
    ax11.plot(alls[0],np.rad2deg(alls[1][0]),label="phiQ2",color="red")
    ax11.plot(alls[0],np.rad2deg(alls[1][1]),label="thetaQ2",color="green")
    ax11.plot(alls[0],np.rad2deg(alls[1][2]),label="psiQ2",color="purple")
    ax11.set_title('Dead Reckoning Filter')
    plt.legend()
    ax12 = fig.add_subplot(3, 3, 5)
    ax12.plot(alls[0][1:],np.rad2deg(alls[2][0]),label="phiQ3",color="red")
    ax12.plot(alls[0][1:],np.rad2deg(alls[2][1]),label="thetaQ3",color="green")
    ax12.plot(alls[0][1:],np.rad2deg(alls[2][2]),label="psiQ3",color="purple")
    ax12.set_title('Tilt Correction')
    plt.legend()
    ax13 = fig.add_subplot(3, 3, 6)
    ax13.plot(alls[0][1:],np.rad2deg(alls[3][0]),label="phiQ4",color="red")
    ax13.plot(alls[0][1:],np.rad2deg(alls[3][1]),label="thetaQ4",color="green")
    ax13.plot(alls[0][1:],np.rad2deg(alls[3][2]),label="psiQ4",color="purple")
    ax13.set_title('Yaw Correction')
    plt.legend()

    ax1 = fig.add_subplot(3, 3, 7, projection='3d')
    ax2 = fig.add_subplot(3, 3, 8, projection='3d')
    ax3 = fig.add_subplot(3, 3, 9, projection='3d')

    finalT=int(alls[0][-1])

    x1=[0,0,0,1,0,0]
    y1=[0,0,0,0,1,0]
    z1=[0,0,0,0,0,1]
    x2=[0,0,0,1,0,0]
    y2=[0,0,0,0,1,0]
    z2=[0,0,0,0,0,1]
    x3=[0,0,0,1,0,0]
    y3=[0,0,0,0,1,0]
    z3=[0,0,0,0,0,1]

    ins=[in1,in2,in3]
    xs=[x1,x2,x3]
    ys=[y1,y2,y3]
    zs=[z1,z2,z3]
    axs=[ax1,ax2,ax3]

    def animate(i,ax,x,y,z):
        i=round(6959*((tt.time()-startingTime)/finalT)/divisor)
        if i<6959:
            for eachInd in range(3):
                wData=ins[eachInd][i][0]
                xData=ins[eachInd][i][1]
                yData=ins[eachInd][i][2]
                zData=ins[eachInd][i][3]

                x[eachInd][3]=1-2*yData*yData-2*zData*zData
                x[eachInd][4]=2*xData*yData+2*wData*zData
                x[eachInd][5]=2*xData*zData-2*wData*yData

                y[eachInd][3]=2*xData*yData-2*wData*zData
                y[eachInd][4]=1-2*xData*xData-2*zData*zData
                y[eachInd][5]=2*yData*zData+2*wData*xData

                z[eachInd][3]=2*xData*zData+2*wData*yData
                z[eachInd][4]=2*yData*zData-2*wData*xData
                z[eachInd][5]=1-2*xData*xData-2*yData*yData

                ax[eachInd].cla()
                ax[eachInd].quiver(0,0,0,x[eachInd][3],x[eachInd][4],x[eachInd][5],color="green")
                ax[eachInd].quiver(0,0,0,y[eachInd][3],y[eachInd][4],y[eachInd][5],color="red")
                ax[eachInd].quiver(0,0,0,z[eachInd][3],z[eachInd][4],z[eachInd][5],color="purple")

                ax[eachInd].set_xlim3d([-1.0, 1.0])
                ax[eachInd].set_xlabel('X')
                ax[eachInd].set_ylim3d([-1.0, 1.0])
                ax[eachInd].set_ylabel('Y')
                ax[eachInd].set_zlim3d([-1.0, 1.0])
                ax[eachInd].set_zlabel('Z')

                if eachInd==0:
                    ax[eachInd].set_title('gyro')
                elif eachInd==1:
                    ax[eachInd].set_title('gyro+acce')
                else:
                    ax[eachInd].set_title('gyro+acce+magn')

            return x,y,z
        else:
            plt.close()

    startingTime=tt.time()
    line_ani = animation.FuncAnimation(fig,animate,fargs=(axs,xs,ys,zs), interval=0, blit=False, repeat = False)
    manager = plt.get_current_fig_manager()
    manager.window.showMaximized()
    plt.show()

if __name__ == "__main__":

    print("pre-processing..")
    "stores the IMUdata to a variable."
    data=readData("IMUData.csv")

    "reads the gyroscope data which is in degrees, converts to radians."
    gyroX=degToRad(data[" gyroscope.X"].values)
    gyroY=degToRad(data[" gyroscope.Y"].values)
    gyroZ=degToRad(data[" gyroscope.Z"].values)

    "reads time, accelerometer and magnetometer data and stores them."
    time=data["time"].values

    acceX=data[" accelerometer.X"].values
    acceY=data[" accelerometer.Y"].values
    acceZ=data[" accelerometer.Z"].values

    magnX=data[" magnetometer.X"].values
    magnY=data[" magnetometer.Y"].values
    magnZ=data[" magnetometer.Z "].values


    "finds the magnitude of accelerometer and magnetometer data"
    acceM=magnitudeFinder(acceX,acceY,acceZ)
    magnM=magnitudeFinder(magnX,magnY,magnZ)

    "normalizes accelerometer and magnetometer data, taking special care of NaN divisions"
    acceNX=normalizer(acceX,acceM)
    acceNY=normalizer(acceY,acceM)
    acceNZ=normalizer(acceZ,acceM)
    magnNX=normalizer(magnX,magnM)
    magnNY=normalizer(magnY,magnM)
    magnNZ=normalizer(magnZ,magnM)

    print("Question 1..")
    question1()

    print("Question 2-Dead Reckoning Filter..")
    estimate,gyroM,resDRF=deadReckoningFilter()
    print("Question 3-Tilt Correction..")
    goodestimate,resTilt=tiltCorrection(estimate,0.01,acceM,gyroM)
    print("Question 4-Yaw Correction..")
    yawCfilt,resYaw=yawCorrection(goodestimate,0.01,magnM)

    print("Question 5:")
    "to plot figures for Question 5"
    alls=[time,resDRF,resTilt,resYaw,[gyroX,gyroY,gyroZ],[acceX,acceY,acceZ],[magnX,magnY,magnZ]]
    print("Creating 3D visualizer in normal speed..")
    plotter(estimate,goodestimate,yawCfilt,1,alls)
    print("Creating 3D visualizer in 2x slower speed..")
    plotter(estimate,goodestimate,yawCfilt,2,alls)

    print("Done!")
