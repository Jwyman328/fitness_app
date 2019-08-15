""" # to create the plot we need to get the data 
import pandas as pd 
from pandas_datareader.data import DataReader
from .models import Point_model
from django_pandas import read_frame

import dash
import dash_core_components as dcc 
import dash_html_components as html 


qs = User_point_input_model.objects.all()
df = read_frame(qs)

def dispatcher(request): #will take in content_type requests, return resposne 
    app = _create_app()
    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.content_type
    }
    with app.server.test_request_context(request.path, **params):
        app.server.preprocess_request()
        try:
            response = app.server.full_dispatch_request() # testing server response 
        except Exception as e: # if there is an error 
            response = app.server.make_response(app.server.handle_exception(e)) # return this if error 
        return response.get_data()



def _create_app():

 """