import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('alarm/photo-reminder.json')
firebase_admin.initialize_app(cred)