import firebase_admin
from firebase_admin import db

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("/Users/thayalanpraveen/Documents/GitHub/PlanetHunters/DSGP6/Prototype/UI_Test/planet-hunters-1b294-firebase-adminsdk-ksboi-00cff64782.json")
firebase_admin.initialize_app(cred , {
    'databaseURL': 'https://planet-hunters-1b294-default-rtdb.firebaseio.com'
})

test = "thayalan@outlook.com"
test = test.replace("@","")
test = test.replace(".","")
ref = db.reference('/users')
users_ref = ref.child(test)
test = users_ref.get()
array = test['History']['array']
print(array[0])

