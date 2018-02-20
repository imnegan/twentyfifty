#use the callhorizons env to run, ie:
#(C:\Users\paul.egan1\AppData\Local\Continuum\Miniconda3) C:\Users\paul.egan1>activate callhorizons

firstJan2050=2469807.5 #from http://www.onlineconversion.com/julian_date.htm


import callhorizons

saturn = callhorizons.query('699', smallbody=False)
#saturn.set_discreteepochs('2451234.5')
saturn.set_discreteepochs(firstJan2050)
saturn.get_elements()

for fieldName in saturn.fields:
    print(fieldName, saturn[fieldName])
