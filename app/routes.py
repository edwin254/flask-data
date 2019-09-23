from flask import render_template
from app import app
import requests
import pandas as pd

data_url = "https://opendata.arcgis.com/datasets/ea875858ec11462ab4e8a2ef5dc2c4ce_0/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json"

@app.route('/')
@app.route('/index')
def index():
               
    response = requests.get(data_url)
    html_table = {}
    if response.status_code == 200:
        data = response.json()
        features = data.get('features')
        pd_series = [data['attributes'] for data in features] 
        for pd_dict in pd_series:
            pd_dict['Year'] = pd_dict['Year_and_Quarter'].split()[0]

        df = pd.DataFrame(pd_series,columns=['Sector', 'OBJECTID','Year_and_Quarter','Kshs_Million', 'Year']) 

        del df['OBJECTID'] 
        
        df1 = df.groupby(['Sector','Year']).sum()
        df2 = df.groupby(['Year','Sector']).sum()

        sector_year = df1.to_html()
        year_sector = df2.to_html()
    
    # return html_table
    return render_template('index.html', sector_year=sector_year, year_sector=year_sector) 