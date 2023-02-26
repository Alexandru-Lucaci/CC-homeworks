# CC-homework

## GET
/ - returns the index.html

/get_data - return a json dictionary with all the film caracteristics

/get/?name=test&type=test&film=test - return a json dictionary. Tries to find a dictionary for the first parameters, if not it will search for the second one

## POST

/?name=test&type=test&film=test&checked=on - add a raw to the html table. checked=on means that it will not duplicates 

## PUT

/?"name='name'&newname='NewName'&newtype='NewType'&newfilm='NewFile'"

/?"id='id'&newname='NewName'&newtype='NewType'&newfilm='NewFilm"
## DELETE
/?name='NewName'

/?id='14'
## Ngrok command 

 ngrok.exe http 8000 
 
