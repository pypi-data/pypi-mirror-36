import numpy as np
from scipy.linalg import block_diag, expm

''' Model Predictive Control '''
class MPC:
    def __init__(self, A, B, C, D=0, dist=0, Np=10, Nc=4, umax=1, umin=0, dumax=1, dumin=0, T=0.001, discretize=True, **kwargs):
        #### System State-Space ####
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.dist = dist
        self.T = T

        #### Discretization ####
        if discretize:
            self.A = expm(self.A.dot(self.T))
            self.B = np.linalg.inv(A).dot((self.A - np.eye(self.A.shape[0]))).dot(self.B)
        
        #### Augmented State-Space ####
        self.Aa = np.r_[np.c_[self.A, np.zeros((self.A.shape[0],self.C.shape[0]))], np.c_[self.C.dot(self.A), np.eye(self.C.shape[0])]]
        self.Ba = np.r_[self.B, self.C.dot(self.B)]
        self.Ca = np.c_[self.C, np.eye(self.C.shape[0])]
        
        #### Model Predictive Controller ####
        self.__Np = Np         # Prediction horizon
        self.__Nc = Nc         # Control Horizon
        self.F = self.get_F()
        self.P = self.get_P()
        self.u = np.zeros((self.B.shape[1],self.__Nc), dtype=np.float)
        self.x = np.zeros((self.A.shape[0],self.__Np), dtype=np.float)
        self.__Rs = np.zeros((self.F.shape[0],self.B.shape[1]))                       # Setpoint (reference, init as 0)
        self.H = self.get_H()        
        self.iH = np.linalg.inv(self.H)
        
        #### Optimization Restrictions ####
        self.M = np.tril(np.ones((self.__Nc, self.__Nc), dtype=np.float))
        self.M = np.r_[np.r_[np.r_[np.eye(self.__Nc), self.M], -np.eye(self.__Nc)], -np.eye(self.M.shape[0])*self.M]
        # Saturation limits must be numpy arrays!
        self.umax, self.dumax = umax, dumax
        self.umin, self.dumin = umin, dumin
        self.gamma = np.ones((1,self.__Nc*4), dtype=np.float).T

        #### Other parameters ####
        self.t = np.array([0,0], dtype=np.float)  # Time vector

    def get_F(self):
        F = self.Ca.dot(self.Aa)
        for i in range(1,self.__Np):
            F = np.vstack((F, self.Ca.dot(np.linalg.matrix_power(self.Aa,i+1))))
        return F
                
    def get_P(self):
        P = np.zeros((self.Ca.shape[0], self.__Nc*self.Ca.shape[0]))
        P[:,0:self.Ca.shape[0]] = self.Ca.dot(self.Ba)
        for i in range(1,self.__Np):
            row = np.roll(P[-self.Ca.shape[0]:,:],1)
            row[:,0:self.Ca.shape[0]] = (self.Ca.dot(np.linalg.matrix_power(self.Aa,i))).dot(self.Ba)
            P = np.r_[P, row]
        return P

    # Is this correct? For every input, make a diagonal augmented matrix
    def get_H(self):
        H = self.P.T.dot(self.P) + self.__Rs[0,0]*np.eye(self.P.T.dot(self.P).shape[0])
        for i in range(1,self.B.shape[1]):
            mtx = self.P.T.dot(self.P) + self.__Rs[0,i]*np.eye(self.P.T.dot(self.P).shape[0])
            H = block_diag(H, mtx)
        return H

    def get_predict_horizon(self):
        return self.__Np
    
    def get_control_horizon(self):
        return self.__Nc

    def set_model(self, A, B, C, D=0, dist=0):
        ref = self.get_reference()
        Np = self.get_predict_horizon()
        Nc = self.get_control_horizon()

        # Reinitialize
        self.__init__(A,B,C,D,dist)
        self.set_predict_horizon(Np)
        self.set_control_horizon(Nc)
        self.set_reference(ref)

    def set_predict_horizon(self, Np):
        self.__Np = Np
        self.F = self.get_F()
        self.P = self.get_P()
        self.H = self.get_H()
        self.iH = np.linalg.inv(self.H)
        ref = self.__Rs[0,:]
        self.__Rs = ref[0]*np.ones((self.F.shape[0],1))
        for i in range(1,self.B.shape[1]):
            self.__Rs = np.c_[self.__Rs, ref[i]*np.ones((self.F.shape[0]))]
        self.x = np.zeros((self.A.shape[0],self.__Np), dtype=np.float)
    
    def set_control_horizon(self, Nc):
        self.__Nc = Nc
        self.P = self.get_P()
        self.H = self.get_H()
        self.iH = np.linalg.inv(self.H)
        self.M = np.tril(np.ones((self.__Nc, self.__Nc), dtype=np.float))
        self.M = np.r_[np.r_[np.r_[np.eye(self.__Nc), self.M], -np.eye(self.__Nc)], -np.eye(self.M.shape[0])*self.M]
        self.gamma = np.ones((1,self.__Nc*4), dtype=np.float).T
        self.u = np.zeros((self.B.shape[1],self.__Nc), dtype=np.float)

    def get_reference(self):
        return self.__Rs[0,:]

    def set_reference(self, ref):
        # Reference is a list
        for i in range(self.B.shape[1]):
            self.__Rs[:,i] = (ref[i]*np.ones((self.__Rs.shape[0],1)))[:,0]
        self.H = self.get_H()
        self.iH = np.linalg.inv(self.H)

    def optimize(self, iH):
        # QPhild, from Liuping Wang's book
        #
        #  Minimizes the quadratic cost function
        #
        #       J = 0.5 x'Hx + x'f
        #       subject to:  M x < b
        #
        #  where iH = inv(H)
        
        n1 = self.M.shape[0]

        xa = np.array([], dtype=np.float)
        for i in range(self.x.shape[0]):
            xa = np.r_[xa, self.x[i,-1]-self.x[i,-2]]
        xa = np.r_[xa, self.x[0,-1]]
        f = self.F.dot(xa)
        f = f.reshape((f.shape[0],1))
        f = -(self.__Rs-f).T.dot(self.P).T

        # Unconstrained optimal solution is -H/f
        eta = -iH.dot(f)

        # Test if this solution satisfies all restrictions M
        kk = 0
        for i in range(n1):
            if (self.M[i,:].dot(eta) > self.gamma[i] ):
                kk += 1
        if (kk == 0):
            return eta  # If all restrictions are satisfied, we are done!
        
        # If not, we proceed with Hildreth's algorithm
        P = self.M.dot(iH.dot(self.M.T))
        d = (self.M.dot(iH.dot(f)) + self.gamma)
        n = d.shape[0]
        x_ini = np.zeros(d.shape)
        lamb = np.copy(x_ini)
        for _ in range(38):
            lamb_p = np.copy(lamb)
            for i in range(n):
                w = P[i,:].dot(lamb) - P[i,i]*lamb[i,0]
                w += d[i,0]
                la = -w/P[i,i]
                lamb[i,0] = max(0,la)
            
            al = (lamb-lamb_p).T.dot(lamb-lamb_p)
            if (al < 10e-8):
                break
            
        eta -= iH.dot(self.M.T).dot(lamb)
        return eta

    def run(self):
        # Redefine restrictions based on last input
        self.gamma = np.ones((self.B.shape[1],self.__Nc))*self.dumax.reshape((max(self.dumax.shape),1))
        self.gamma = np.c_[self.gamma, np.ones((self.B.shape[1],self.__Nc))*(self.umax.reshape((max(self.umax.shape),1))-self.u[:,-1].reshape((self.u.shape[0],1)))]
        self.gamma = np.c_[self.gamma, np.ones((self.B.shape[1],self.__Nc))*(-self.dumin.reshape((max(self.dumax.shape),1)))]
        self.gamma = np.c_[self.gamma, np.ones((self.B.shape[1],self.__Nc))*(-self.umin.reshape((max(self.umax.shape),1))+self.u[:,-1].reshape((self.u.shape[0],1)))]
        self.gamma = self.gamma.T

        # Quadratic optimization (returns best solution given restrictions M)
        du = self.optimize(self.iH)

        # New control output (u is bound by control horizon, to avoid memory issues)
        self.u = np.roll(self.u[-self.u.shape[0]:,:],-1)
        self.u[:,-1] = du[0,:] + self.u[:,-2]

''' Economic Model Predictive Control
    Inherits from MPC class, with the only modification being the minimization function ''' 
class EMPC(MPC):
    def __init__(self, A, B, C, D, minFun, dist=0, **kwargs):
        MPC.__init__(self, A, B, C, D, dist, **kwargs)
        self.minFun = minFun

    def optimize(self, *args):
        return self.minFun(args)