# twenty fifty to do

* Classes and modules
+ Methods & Functions
- Objects & General stuff to do


* game [twentyfifty.py]
	+ initialisation
		+ load modules DONE
		+ load sats
			- download sv0 for 
				planets, DONE
				moons and 
				key asteroids
			+ importsatdata DONE
			- radius data

* physical model
	* Orbital mechanics [sat.py]
		+ state vector rv_from_r0v0(R0, V0, t, mu) DONE
		+ mu DONE
		+ period(sv0)
		+ sphereOfInfluence(mass)
		+ semimajorAxis()
			- exception for hyperbole
	* Sat [sat.py]
		+ newParent()
			+ @mu(self) DONE
		+ stateVector(t)
		* Ship
			+ hoffman transfer
		* asteroids
			* asteroid spawner

* controllers
	* i/o
		* buttons	
		+ displaySystem(sat, time, outerChild=None)
			- displays sat in centre
			- scales to outer sat 
				- default largest semimajorAxis
			- logarithmic scale
			- displays child sats in orbit
			- timeWarp set to outerSat
		* MainBackground
			* SystemSprite
				* SatSprite
				- systemSprite
				- satSprites
			- mainSystemNode
			- solarSystemInsetNode
			- selectedSystemCalloutNode
			* buttons
			* info windows
				* game time
				- key event notifications (clickable)
		* time
			+ outer sat orbits in 20s
		* video
			+ scale()
				- logarithmic
				- default sat with the largest orbit: system.children[-1].semimajorAxis
				- if no sats, zoom to twice the radius

		
	* events [event.py]
		* event DONE
		* event manager DONE
		- event members DONE
		* timed events
		
	- debugging
