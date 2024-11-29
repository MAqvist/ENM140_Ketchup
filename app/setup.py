import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("app/festival-game-6f53a-firebase-adminsdk-x47fu-bdd2a42766.json")
firebase_admin.initialize_app(cred)
