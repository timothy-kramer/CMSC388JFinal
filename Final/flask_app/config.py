# Stores all configuration values
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
MONGODB_HOST = os.environ.get('MONGODB_HOST')
# MONGODB_SETTINGS = {
#     'db': 'CMSc388J',
#     'host': 'mongodb+srv://tkramer2:Halo@cluster0.pwvtz.mongodb.net/CMSc388J?retryWrites=true&w=majority&appName=Cluster0'
# }
#MONGODB_HOST = 'mongodb+srv://tkramer2:Halo@cluster0.pwvtz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
