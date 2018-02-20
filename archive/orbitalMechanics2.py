import numpy as np
from math import *

au=149597870700


def norm(X):
	# returns magnitude x of vector cartesian X
	# USE np.linalg.norm(X) instead
	x=sqrt(np.dot(X,X))
	return x
	
def mu(m,parentm):
	G=6.67408e-11  # G: gravitational constant
	return G*(parentm+m)
	
def stumpS(z):
	'''D.4 p 600'''
	if z>0:
		s=(sqrt(z)-sin(sqrt(z)))/(sqrt(z))**3
	elif z<0:
		s=(sinh(sqrt(-z))-sqrt(-z))/(sqrt(-z))**3
	else:
		s=1/6.0
	return s

def stumpC(z):
	'''D.4 p 600'''
	if z>0:
		c=(1-cos(sqrt(z)))/z
	elif z<0:
		c=(cosh(sqrt(-z))-1)/(-z)
	else:
		c=1.0/2.0
	return c
	
def kepler_U(t,ro,vro,alpha,mu):
	'''D.5 p601'''
	a=alpha
	error = 1.0e-8
	nMax = 30
	x=sqrt(mu)*abs(a)*t
	n=0
	ratio=1.0
	while abs(ratio)>error and n<=nMax:
	# Newtons method
		n+=1
		z=a*x**2
		C=stumpC(z)
		S=stumpS(z)
		F=ro*vro/sqrt(mu)*x**2*C+(1-a*ro)*x**3*S+ro*x-sqrt(mu)*t
		dFdx=ro*vro/sqrt(mu)*x*(1-z*S)+(1-a*ro)*x**2*C+ro
		ratio=F/dFdx
		x=x-ratio
	return x
	
def rv_from_r0v0(R0,V0,t,mu):
	r0 = norm(R0)
	v0 = norm(V0)
	vr0 = np.dot(R0, V0)/r0
	alpha = 2/r0 - v0**2/mu
	x = kepler_U(t,r0,vr0,alpha,mu)
	f, g = f_and_g(x, t, r0, alpha,mu)
	R = f*R0 + g*V0
	r = norm(R)
	fdot, gdot = fDot_and_gDot(x, r, r0, alpha,mu)
	V = fdot*R0 + gdot*V0
	return np.array([R,V])
	
def coe_from_sv(mu,R,V):
	eps = 1e-10
	r = norm(R)
	v = norm(V)
	vr = np.dot(R,V)/r
	H = np.cross(R,V)
	h = norm(H)
	incl = acos(H[2]/h)
	N = np.cross(np.array([0,0,1]),H)
	n = norm(N)
	error = 1.0e-8
	
	if np.fabs(n)<error:
		RA = acos(N[0]/n)
		if N[1] < 0:
			RA = 2*pi - RA
	else:
		RA = 0
	
	E = 1/mu*((v**2 - mu/r)*R - r*vr*V)
	e = norm(E)
	
	if np.fabs(n)<error:
		if e > eps:
			w = acos(np.dot(N,E)/n/e)
			if E[2] < 0:
				w = 2*pi - w
		else:
			w = 0
	else:
		w = 0
	
	if e > eps:
		TA = acos(np.dot(E,R)/e/r)
		if vr < 0:
			TA = 2*pi - TA
	else:
		cp = np.cross(N,R)
		if cp[2] >= 0:
			TA = acos(np.dot(N,R)/n/r)
		else:
			TA = 2*pi - acos(np.dot(N,R)/n/r)
	if e==0: a=None
	else: a = h**2/mu/(1 - e**2)
	coe = [h,e,RA,incl,w,TA,a]
	return coe

	
	
class Sat: pass

sun=Sat()
earth=Sat()
sun.m=1.989e30
earth.m=5.97219e24
earth.R0=np.array([-1.708105047795956E-01, 9.648931350919518E-01, -9.590189321159192E-05])*au
earth.V0=np.array([-1.721265688032099E-02, -3.071877104787714E-03, 9.075238457855505E-07])*au/(24*60*60)
earth.mu=mu(earth.m, sun.m)
earth.coe=coe_from_sv(earth.mu, earth.R0, earth.V0)

print(earth.mu)
print(earth.R0)
print(earth.V0)
print(earth.coe)


