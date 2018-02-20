# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 09:40:10 2016

@author: Paul.Egan
"""
import numpy as np
from math import *

G=6.67408e-11  # G: gravitational constant
au=149597870700.  # au: astronomical unit in m

def norm(X):
	# returns magnitude x of vector cartesian X
	# USE np.linalg.norm(X) instead
	x=sqrt(np.dot(X,X))
	return x

def order_of_magnitude(flt):
	x=int(flt)
	oom=0
	while x>0:
		x=x/10
		oom+=1
	return oom

def rotate2D(theta):
	'''returns the rotation matrix in 2D'''
	rotation_matrix=np.array([[cos(theta),-sin(theta)],
	[sin(theta),cos(theta)]])
	return rotation_matrix

def rotation3D(R0,theta):
	# returns the rotation matrix in 3D
	# Usage: S1=np.dot(rotation(theta),S0)
	tx,ty,tz = theta
	Rx = np.array([[1,0,0], [0, cos(tx), -sin(tx)], [0, sin(tx),cos(tx)]])
	Ry = np.array([[cos(ty), 0, -sin(ty)], [0, 1, 0], [sin(ty), 0,cos(ty)]])
	Rz = np.array([[cos(tz), -sin(tz), 0], [sin(tz), cos(tz), 0],[0,0,1]])
	rotation=np.dot(Rx, np.dot(Ry, Rz))
	return np.dot(rotation(theta),R0)

def mu(m,parentm):
	G=6.67408e-11  # G: gravitational constant
	return G*(parentm+m)

def alpha(mu,R0,V0):
	'''inverse of semimajor axis'''
	r0=norm(R0)
	v0=norm(V0)
	return 2/r0-v0**2/mu

def periodEllipse(a,mu):
	'''Period for Circular & elliptical orbits'''
	return 2*pi*sqrt(a**3/mu)

def rp(a,e):
	'''Radius of periapsis
	TODO: Fix for parabola'''
	#https://en.wikipedia.org/wiki/Apsis
	return a*(1-e)

def vp(a,e,mu):
	'''Velocity of periapsis
	TODO: Fix for parabola'''
	#https://en.wikipedia.org/wiki/Apsis
	return sqrt((1+e)*mu/((1-e)*a))

def REllipse(a,e,period,t):
	'''position vector for elliptical orbits'''
	M=(2*pi*t/period)%(2*pi)
	if e>0.8: E=pi
	else: E=M
	if e*cos(E)==1.0:
		E=1-e*cos(E)
	else:
		error=10E-15
		counter=0
		ratio=1
		while fabs(ratio)>error and counter<30:
			ratio=(E-e*sin(E)-M)/(1-e*cos(E))
			E=E-ratio;
			counter=counter+1
	theta=2*atan2((1+e)**0.5*sin(E/2),(1-e)**0.5*cos(E/2))
	r=a*(1-e*cos(E))
	return np.array((r*cos(theta),r*sin(theta)))

def RHyperbola(a,e,mu,t):
	error = 1.e-15
	#t - to = [(-a)3/k]1/2 M from http://www.bogan.ca/orbits/kepler/orbteqtn.html
	M=t/(sqrt(-a**3/mu))
	F=M
	ratio=1
	while abs(ratio)>error:
		ratio=(e*sinh(F)-F-M)/(e*cosh(F)-1)
		F=F-ratio
	theta=2*atan(sqrt((e+1)/(e-1))*tanh(F/2))
	r=a*(e*cosh(F)-1) #eq 3.43
	return np.array((r*cos(theta),r*sin(theta)))

def RParabola():
	#TODO
	return 0.0

def e(mu,R0,V0):
	return norm(1/mu*((norm(V0)**2-mu/norm(R0))*R0-norm(R0)*np.dot(R0,V0)/norm(R0)*V0))

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

def f_and_g(x,t,ro,alpha,mu):
	'''D.6 p 603'''
	a=alpha
	z=a*x**2
	f=1-x**2/ro*stumpC(z)
	g=t-1/sqrt(mu)*x**3*stumpS(z)
	return (f,g)

def fDot_and_gDot(x,r,ro,alpha,mu):
	a=alpha
	z=a*x**2
	fdot=sqrt(mu)/r/ro*(z*stumpS(z)-1)*x
	gdot=1-x**2/r*stumpC(z)
	return (fdot,gdot)

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

def sv_from_coe(h,e,RA,incl,w,TA,mu):
	# coe - orbital elements {h,e,RA,incl,w,TA}
	# h = angular momentum (kmˆ2/s) **function
	# e = eccentricity
	# RA = right ascension of the ascending node (rad) ***0 for 2d 
	# incl = inclination of the orbit (rad) ***0 for 2d
	# w = argument of periapsis
	# TA = true anomaly (rad)

	rp = (h**2/mu)*(1/(1+e*cos(TA)))*(cos(TA)*np.array([1,0,0])+sin(TA)*np.array([0,1,0]))
	vp = (mu/h)*(-sin(TA)*np.array([1,0,0])+(e+cos(TA))*np.array([0,1,0]))
	R3_W = np.array([[cos(RA),sin(RA),0],
	[-sin(RA),cos(RA),0],
	[0,0,1]])
	R1_i = np.array([[1,0,0],
	[0,cos(incl),sin(incl)],
	[0,-sin(incl),cos(incl)]])
	R3_w = np.array([[cos(w),sin(w),0],
	[-sin(w),cos(w),0],
	[0,0,1]])
	Q_pX = R3_W*R1_i*R3_w # TODO: Check this is correct matrix multiplication
	r = Q_pX*rp
	v = Q_pX*vp
	return r, v

def coe_from_sv(mu,R,V):
	eps = 1e-10
	r = norm(R)
	v = norm(V)
	vr = np.dot(R,V)/r
	H = np.cross(R,V)
	h = norm(H)
	incl = acos(H(3)/h)
	N = cross(np.array([0,0,1]),H)
	n = norm(N)
	if n == 0:
		RA = acos(N(1)/n)
		if N[1] < 0:
			RA = 2*pi - RA
	else:
		RA = 0
	E = 1/mu*((v**2 - mu/r)*R - r*vr*V)
	e = norm(E)
	if n== 0:
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

# Mathematical functions-------------------------
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

def h(a,e,mu):
	if e<1: return sqrt(mu*a*(1-e)**2)
	else: 
		print('ERROR: e>=1')
		pass
