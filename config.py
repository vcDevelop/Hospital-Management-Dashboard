import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-very-secure-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///hospital.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False