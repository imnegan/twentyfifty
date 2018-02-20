from math import sqrt, sin, cos, sinh, cosh, acos, pi
import numpy as np

error = 1e-8
nMax = 1000

def stumpS(z): #checked
	if z>0:
		s=(sqrt(z)-sin(sqrt(z)))/(sqrt(z)**3)
	elif z<0:
		s=(sinh(sqrt(-z))-sqrt(-z))/(sqrt(-z)**3)
	else:
		s=1/6
	return s

def stumpC(z): #checked
	if z>0:
		c=(1-cos(sqrt(z)))/z
	elif z<0:
		c=(cosh(sqrt(-z))-1)/(-z)
	else:
		c=1/2
	return c

def kepler_U(dt, r0, vr0, alpha, mu): #checked
	'''D5 Algorithm 3.3'''
	x=sqrt(mu)*abs(alpha)*dt #checked
	n=0
	ratio=1
	while abs(ratio)>error and n<=nMax:
		n+=1
		C=stumpC(alpha*(x**2))
		S=stumpS(alpha*(x**2)) #checked
		
		F=r0*vr0/sqrt(mu)*(x**2)*C+(1-alpha*r0)*(x**3)*S+r0*x-sqrt(mu)*dt
		
		dFdx=r0*vr0/sqrt(mu)*x*(1-alpha*(x**2)*S)+(1-alpha*r0)*(x**2)*C+r0
		
		ratio=F/dFdx
		x=x-ratio

	if n>=nMax:
		try:
			raise ValueError("Newton's method error")
		except ValueError:
			print('More than', nMax, 'iterations')
	return x

def f_and_g(x, t, r0, alpha, mu):
	'''
	D.6 Calculation of the Lagrange coefﬁcients
	f and g and their time derivatives
	'''
	z=alpha*(x**2)
	f=1-x**2/r0*stumpC(z)
	g=t-1/sqrt(mu)*(x**3)*stumpS(z) #fixed
	return f, g

def fDot_and_gDot(x, r, r0, alpha, mu):
	'''
	;7)77)D.6 Calculation of the Lagrange coefﬁcients
	f and g and their time derivatives
	'''
	z=alpha*x**2
	fDot=sqrt(mu)/r/r0*(z*stumpS(z)-1)*x
	gDot=1-x**2/r*stumpC(z)
	return fDot, gDot

def rv_from_r0v0(R0, V0, t, mu):
	'''
	Algorithm 3.4
	Inputs:
		state vector (R0, V0)
		time lapse t
	Output:
		state vector (R, V)
	'''
	r0=np.linalg.norm(R0)
	v0=np.linalg.norm(V0)
	vr0=np.dot(R0, V0)/r0
	alpha=2/r0-v0**2/mu
	x=kepler_U(t,r0,vr0,alpha,mu)
	f,g=f_and_g(x, t, r0, alpha, mu)
	R=f*R0+g*V0
	r=np.linalg.norm(R)
	fDot,gDot=fDot_and_gDot(x, r, r0, alpha, mu)
	V=fDot*R0+gDot*V0
	return R, V

def coe_from_sv(R, V, mu):
	'''
	D.8 Algorithm 4.1: calculation of the orbital elements from the state vector
	Inputs:
		mu - gravitational parameter (kmˆ3; sˆ2)
		R - position vector
		V - velocity vector
	Output:
		coe - orbital elements [h e RA incl w TA]
			h = angular momentum (kmˆ2/s)
			e = eccentricity
			RA = right ascension of the ascending node (rad)
			incl = inclination of the orbit (rad)
			w = argument of perigee (rad)
			TA = true anomaly (rad)
	'''
	r=np.linalg.norm(R)
	v=np.linalg.norm(V)
	vr=np.dot(R,V)/r

	H=np.cross(R,V)
	h=np.linalg.norm(H)

	incl=acos(H[2]/h)

	N=np.cross([0,0,1],H)
	n=np.linalg.norm(N)

	if n!=0:
		RA=acos(N[0]/n)
		if N[1]<0:
			RA=2*pi-RA
	else:
		RA=0

	E=1/mu*((v**2-mu/r)*R-r*vr*V)
	e=np.linalg.norm(E)

	if n!=0:
		if e>error:
			w=acos(np.dot(N,E)/n/e)
			if E[2]<0:
				w=2*pi-w
		else:
			w=0

	if e>error:
		TA=acos(np.dot(E,R)/e/r)
		if vr<0:
			TA=2*pi-TA
	else:
		cp=np.cross(N,R)
		if cp[2]>=0:
			TA=acos(np.dot(N,R)/n/r)
		else:
			TA=2*pi-acos(dot(N,R)/n/r)

	a=h**2/mu/(1-e**2)

	return h, e, RA, incl, w, TA, a

def sv_from_coe(coe, mu):
	'''
	D.9 Algorithm 4.2: calculation of the state vector from the orbital elements
	'''
	h, e, RA, incl, w, TA, a=coe

	rp=(h**2/mu)*(1/(1+e*cos(TA)))*(cos(TA)*np.array([1,0,0])
		+sin(TA)*np.array([0,1,0]))

	vp=(mu/h)*(-sin(TA)*np.array([1,0,0])+(e+cos(TA))*np.array([0,1,0]))

	R3_W=np.array(	[[	cos(RA), 	sin(RA), 	0			],
					[	-sin(RA), 	cos(RA), 	0			],
					[	0,			0, 			1			]])

	R1_i=np.array(	[[	1, 			0,			0			],
					[	0,			cos(incl), 	sin(incl)	],
					[	0,			-sin(incl),	cos(incl)	]])

	R3_w=np.array(	[[ 	cos(w),		sin(w), 	0			],
					[	-sin(w),	cos(w),		0			],
					[	0,			0,			1			]])

	alpha=np.transpose(R3_W)
	bravo=np.transpose(R1_i)
	charlie=np.transpose(R3_w)

	Q_pX=np.dot(np.dot(alpha,bravo), charlie)
	
	r = np.dot(Q_pX,rp)
	v = np.dot(Q_pX,vp)

	return r, v

def mu(m,parentm):
	G=6.67408e-11  # G: gravitational constant
	return G*(parentm+m)
	
def periodEllipse(a,mu):
	'''Period for Circular & elliptical orbits'''
	return 2*pi*sqrt(a**3/mu)
	
def semimajorAxis(R0, V0, mu):
	r0=np.linalg.norm(R0)
	v0=np.linalg.norm(V0)
	vr0=np.dot(R0, V0)/r0
	alpha=2/r0-v0**2/mu
	return 1/alpha

if __name__ == "__main__":
    print('orbital.py is being run directly')
else:
    print('orbital.py loaded.')
