import numpy as np
import matplotlib.pyplot as plt

#initialization
nx = 100
# ny = 1
nt = 200
v0 = 0.01 # initial velocity
delta_x = 1
delta_t = 0.3
gamma = 1.4
U = np.zeros((nx, 3))
F = np.zeros((nx, 3))
F_half = np.zeros((nx, 3))
U_der = np.zeros((nx, 3))

# initialization of U
for i in range(nx):
    if i < nx / 2:
        rho_L = 1
        P_L = 0.8
        U[i, 0:3] = np.array([rho_L, rho_L*v0, P_L])
    else:
        rho_R = 0.1
        P_R = 0.1
        U[i, 0:3] = np.array([rho_R, rho_R*v0, P_R])

def find_f(U):
    v = U[:, 1] / U[:,  0]
    P = (gamma-1)*U[:,0]*(U[:,2]/U[:,0]-0.5*v**2)
    e = P/((gamma-1)*U[:,0])
    F[:,0] = U[:,1]
    F[:,1] = U[:,1]*v + P
    F[:,2] = (U[:,0]*(e+0.5*v**2)+P)*v
    return F

def find_f_half(U,F):
    v = U[:,1]/U[:,0]
    P = (gamma-1)*U[:,0]*(U[:,2]/U[:,0]-0.5*v**2)
    c_s = np.sqrt(P*gamma/U[:,0])
    lambda_p = v + c_s
    lambda_m = v - c_s
    # print(lambda_m[1,0]*U[1,0,1])
    alpha = np.zeros((nx,6)) #first three rows alpha plus, second three alpha minus
    for i in range(nx-1):
        for k in range(3):
            alpha[i,k] = max(0, lambda_p[i]*U[i,k], lambda_p[i+1]*U[i+1,k])
            alpha[i,k+3] = max(0, -lambda_m[i]*U[i,k], -lambda_m[i+1]*U[i+1,k])
    # print(alpha)
    F_half = (alpha[:nx-1,0:3]*F[:nx-1,:]+alpha[:nx-1,3:6]*F[1:,:]-alpha[:nx-1,0:3]*\
              alpha[:nx-1,3:6]*(U[1:,:]-U[:nx-1,:]))/(alpha[:nx-1,0:3]+alpha[:nx-1,3:6])
    return F_half

def find_u_der(F_half, delta_x):
    U_der = -(F_half[1:,:]-F_half[:-1,:])/delta_x
    U_der = np.append(U_der,[np.array([0,0,0])], axis=0)
    U_der = np.vstack([np.array([0,0,0]),U_der])
    # print(U_der)
    return U_der

def find_u(U, U_der,delta_t,ii):
    # print(U)
    # U_histor[i] = U[:nx-2,:,:]
    if ii % 10 == 0:
        plt.plot(range(nx), U[:,1]/U[:,0])
    U[:,:]= U[:,:] + delta_t*U_der
    # print(U)
    return U

for i in range(nt):
    F = find_f(U)
    F_half = find_f_half(U,F)
    U_der = find_u_der(F_half,delta_x)
    U = find_u(U,U_der,delta_t,i)

plt.show()