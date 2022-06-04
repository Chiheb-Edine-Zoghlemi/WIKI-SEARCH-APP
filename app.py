
####################################################################
#                                                                  #
#                          PACKAGES                                #
#                                                                  #
####################################################################

from flask import Flask, render_template, request, jsonify, make_response
from flask_cors import CORS
import colorama
from termcolor import cprint
colorama.init()
import requests as req
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup as bs 
import json

####################################################################
#                                                                  #
#                        app config                                #
#                                                                  #
####################################################################

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = '571ebf8e13ca209536c29be68d435c00'
db = SQLAlchemy(app)

####################################################################
#                                                                  #
#                           Database                               #
#                                                                  #
####################################################################

########################## Page Table ##############################
class pages(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text())
    url = db.Column(db.Text())
    content = db.Column(db.Text())
    page_language = db.Column(db.String(50))
    length = db.Column(db.Integer())
    latitude = db.Column(db.Integer())
    longitude = db.Column(db.Integer())
    logo = db.Column(db.Text())
    page_information = db.Column(db.Text())
    def __init__(self, id, title, url, content, page_language, length, latitude, longitude,logo, page_information,):
        self.id = id
        self.title = title
        self.url = url
        self.content = content
        self.page_language = page_language
        self.length = length
        self.latitude = latitude
        self.longitude = longitude
        self.logo = logo
        self.page_information = page_information

########################## Terms Table ##############################
class terms(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_page = db.Column(db.Integer,db.ForeignKey('pages.id'))
    type = db.Column(db.String(150))
    content = db.Column(db.Text())
    def __init__(self,  id_page, type, content):
        self.id_page = id_page
        self.type = type
        self.content = content 

####################################################################
#                                                                  #
#                        END POINTS                                #
#                                                                  #
####################################################################

###############  HTML TEMPLATES ###################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Data')
def data():
    return render_template('data.html')
    
###############  GET ALL DATA  ###################
@app.route('/get_data', methods=['POST'])
def get_data():
    parsed_data = []
    pages_data = pages.query.all()
    logo = None
    for p in pages_data:

        page = {
        'id':p.id,
        'title':p.title,
        'url':f'<a href="{p.url}">{p.url}</a>',
        'page_language':p.page_language,
        'length':p.length,
        'alias':'<ul>',
        'lables':'<ul>',
        'description':'<ul>',
        'latitude':p.latitude,
        'longitude':p.longitude,
        'logo': f'<img src="{p.logo}" width="100%"/>'  if p.logo     else None,
        'info':p.page_information
        }
        # addign the lias 
        alias = terms.query.filter_by(id_page=p.id,type="Alias")
        for a in alias:
            page['alias'] = page['alias'] + '<li>'+a.content.strip()+'</li><br>'
        page['alias']  =  page['alias'] +'</ul>'
        # adding the lables 
        lables = terms.query.filter_by(id_page=p.id,type="Label")
        for l in lables:
            page['lables'] = page['lables'] + '<li>'+l.content.strip()+'</li><br>'
        page['lables']  =  page['lables'] +'</ul>'
        # addign the descriptions 
        description = terms.query.filter_by(id_page=p.id,type="Description")
        for d in description:
            page['description'] = page['description'] + '<li>'+d.content.strip()+'</li><br>'
        page['description']  =  page['description'] +'</ul>'
        parsed_data.append(page)
    return make_response(jsonify(parsed_data), 200)
   
###############  Term querying ###################
@app.route('/get_pages_term', methods=['POST'])
def get_pages_term():
    term = request.form.get('TERM')
    if term:
        print(f'[ The Term you are searching for => {term} ]')
    nbr = request.form.get('NUMBER')

    if nbr:
        nbr= int(nbr)
        print(f'[ The Number of pages you are searching for => {nbr} ]')
    else:
        nbr = 10
    
    with req.Session() as s :
            URL = "https://en.wikipedia.org/w/api.php"
            PARAMS = {
                "action": "query",
                "format": "json",
                "list": "search",
                "utf8": 1,
                "formatversion": "2",
                "srsort": "just_match",
                "srsearch": term,
                "srlimit": nbr

            }
            result = s.get(url=URL, params=PARAMS)
            if(result.status_code == 200):
                data = result.json()['query']['search']
                parsed_data = []
                for d in data:
                    creation_data = d.get('timestamp')
                    if creation_data:
                        creation_data=creation_data.split('T')[0]
                    page = {
                        'id':d.get('pageid'),
                        'size':d.get('size'),
                        'word_count':d.get('wordcount'),
                        'title':d.get('title'),
                        'date':creation_data

                    }
                    parsed_data.append(page)
                return make_response(jsonify(parsed_data), 200)
            else:
                return 'Unable to scrap the request',400


###############  Geolocation querying ###################
@app.route('/get_pages_geo', methods=['POST'])
def get_pages_geo():  
    longitude = request.form.get('LONG')
    if longitude:
        print(f'[ The Longitude you are searching for => {longitude} ]')
    latitude = request.form.get('LATI')
    if longitude:
        print(f'[ The Latitude you are searching for => {latitude} ]')
    nbr = request.form.get('NUMBER')
    if nbr:
        nbr= int(nbr)
        print(f'[ The Number of pages you are searching for => {nbr} ]')
    else:
        nbr = 10
    radius = request.form.get('RADIUS')
    PARAMS = {
                    "action": "query",
                    "format": "json",
                    "list": "geosearch",
                    "formatversion": "2",
                    "gscoord": f"{latitude}|{longitude}",
                    "gslimit": nbr
            }
    if radius:
        PARAMS['gsradius']=radius
    with req.Session() as s :
            URL = "https://en.wikipedia.org/w/api.php"
            result = s.get(url=URL, params=PARAMS)
            if(result.status_code == 200):
               
                data = result.json()['query']['geosearch']
                parsed_data = []
                for d in data:
                    page = {
                        'id':d.get('pageid'),
                        'lat':d.get('lat'),
                        'lon':d.get('lon'),
                        'dist':d.get('dist'),
                        'title':d.get('title'),
                    }
                    parsed_data.append(page)
                return make_response(jsonify(parsed_data), 200)
            else:
                return 'Unable to scrap the request',400

def parse_info_page(html):
    info = {'logo':[]}
    soup = bs(html, "html.parser")
    table = soup.find('table',class_='infobox')
    if table:
        rows = table.find_all('tr')
        for r in rows : 
            if r.find('th'):
                if r.find('td'):
                    attribute = r.find('th').text.strip()
                    value = r.find('td').text.strip()
                    info[attribute]=value
            else:
                if r.find('img'):
                    info['logo'].append('https:'+r.find('img').get('src'))
    if info['logo']:
        info['logo'] = info['logo'][0]
    return info

                    

@app.route('/download/<id_page>', methods=['POST'])
def download(id_page):
    PARAMS = {
	"action": "query",
	"format": "json",
	"prop": "pageterms|info|extracts|coordinates|pageprops",
	"pageids": id_page,
	"utf8": 1,
	"formatversion": "2",
	"wbptterms": "alias|label|description",
	"inprop": "url|displaytitle",
	"explaintext": 1
    }  
    with req.Session() as s :
        URL = "https://en.wikipedia.org/w/api.php"
        result = s.get(url=URL, params=PARAMS)
        if(result.status_code == 200):
            data = result.json()['query']['pages'][0]
            if data.get('coordinates'):
                lat=data['coordinates'][0].get('lat')
                long=data['coordinates'][0].get('lon')
            else:
                lat = None
                long =None
            info_dict = content  = None
            
            page_content_req = s.get(url=URL, params={"action": "parse","format": "json","pageid": id_page,"prop": "wikitext","utf8": 1,"formatversion": "2"}) 
            if page_content_req.status_code == 200:
                content = page_content_req.json()['parse']['wikitext'].strip()
            req_html = s.get(url=data.get('fullurl')) 
            if req_html.status_code == 200:
                rawhtml = req_html.text
                info_dict = parse_info_page(rawhtml)
                if info_dict.get('logo'):
                    logo=info_dict.pop('logo')
                else:
                    logo = None
            new_page = pages(id_page, data.get('displaytitle'), data.get('fullurl'), content, data.get('pagelanguage'), 
            data.get('length'), lat, long,logo, json.dumps(info_dict))
            db.session.add(new_page)
            db.session.commit()
            if data.get('terms'):
                ## adding the alias 
                alias = data['terms'].get('alias') if data['terms'].get('alias') else [] 
                for a in alias:
                    new_term = terms(id_page, 'Alias', a)
                    db.session.add(new_term)
                    db.session.commit()
                labels = data['terms'].get('label') if data['terms'].get('label') else [] 
                ## adding the lables ##
                for l in labels:
                    new_term = terms(id_page, 'Label', l)
                    db.session.add(new_term)
                    db.session.commit()
                ## adding the descriptions 
                descriptions = data['terms'].get('description') if data['terms'].get('description') else [] 
                for des in descriptions:
                    new_term = terms(id_page, 'Description', des)
                    db.session.add(new_term)
                    db.session.commit()
            return 'Donwlod is done', 200
        else:
            return 'Unable to scrap the request',400
        
    
    

####################################################################
#                                                                  #
#                           MAIN                                   #
#                                                                  #
####################################################################

def credit():
    print('\n===============================================================')
    cprint('This product is Developed By : Chiheb Edine Zoghlemi ', 'blue')
    print('Contact Links :')
    print('Email   📧 => chihebedine.zoghlemi@gmail.com ')
    print('===============================================================')


if __name__ == '__main__':
    credit()
    db.create_all()
    app.run(host='0.0.0.0', debug=True)
