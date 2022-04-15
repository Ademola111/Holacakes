#first open init beside the template folder which is the top root init. 
# after the init inside the template next is config.py not in instance
from flask import Flask
from flask_wtf.csrf import CSRFProtect

from flask_sqlalchemy import SQLAlchemy
from flask_msearch import Search

#instantiate an object of Flask app
app = Flask(__name__, instance_relative_config=True)
csrf=CSRFProtect(app)

#Load the config file
from holacakesapp import config
app.config.from_object(config.ProductionConfig)
app.config.from_pyfile('config.py', silent=False) #this is the config in instance folders

#database connection
db=SQLAlchemy(app)
search = Search()
search.init_app(app)

#load your routes here
from holacakesapp.myroutes import adminroutes, userroutes #since routes is now a module on its own

#Load forms
from holacakesapp import forms

#load models
from holacakesapp import models

