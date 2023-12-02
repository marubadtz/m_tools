from dash import Dash, Input, Output, State, html, dcc, callback
import dash_bootstrap_components as dbc
import dash_auth
from os import getenv
import json
from collections import OrderedDict
import config

# App setup
VALID_USERNAME_PASSWORD_PAIRS = {config.USERNAME: config.PASSWORD}
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

server = app.server
app.title = "Marcom Tools"
app._favicon = ('favicon64r.png')

# Functions
# Get ready to format url
def get_universal_url(url):
    for l in langs:
        url = url.replace('/'+l+'/', '/')
    for d in domains:
        url = url.replace('.'+d+'/', '.')
    url = url.replace('armory.','').replace('news_ingame/','')
    url = url[:url.find('://')+3] + '%s' + url[url.find('://')+3:]
    if 'sgame.' in url:
        url = url[:url.find('sgame.')+6]  + '{}{}%s' + url[url.find('sgame.')+6:]
    else:
        url = url[:url.find('ships.')+6]  + '{}{}%s' + url[url.find('ships.')+6:]
    if url[-1] != '/':
        url = url + '/'
    return url

# Check if url is valid
def url_is_valid(url):
    if url.find('://') > 0 and url[:4] == 'http' and \
        (url.find('ships.') > 0 or url.find('wowsgame.') > 0) and \
        (url.find('.eu/') > 0 or url.find('.com/') > 0 or url.find('.asia/') > 0) or url.find('.cn/') > 0:
        return True
    else:
        return False

# Variables
code_temp = 'wgc-128-cmpt-kots-finals-marcom-1195'
name_temp = 'WGC_128_CMPT_KOTS_finals_MARCOM_1195'
url_temp = 'https://worldofwarships.eu/news/general-news/kots-xvi/'

# Json templates and maps
country_lang_map = OrderedDict([('AD', 'en'), ('AE', 'en'), ('AF', 'en'), ('AG', 'en'), ('AI', 'en'), ('AL', 'en'), ('AM', 'ru'), ('AO', 'en'), ('AP', 'en'), ('AQ', 'en'), ('AR', 'es-mx'), ('AS', 'en'), ('AT', 'de'), ('AU', 'en'), ('AW', 'en'), ('AX', 'en'), ('AZ', 'ru'), ('BA', 'en'), ('BB', 'en'), ('BD', 'en'), ('BE', 'fr'), ('BF', 'fr'), ('BG', 'en'), ('BH', 'en'), ('BI', 'fr'), ('BJ', 'fr'), ('BL', 'en'), ('BM', 'en'), ('BN', 'en'), ('BO', 'es-mx'), ('BQ', 'en'), ('BR', 'pt-br'), ('BS', 'en'), ('BT', 'en'), ('BV', 'en'), ('BW', 'en'), ('BZ', 'en'), ('CA', 'en'), ('CC', 'en'), ('CD', 'fr'), ('CF', 'en'), ('CG', 'fr'), ('CH', 'de'), ('CI', 'fr'), ('CK', 'en'), ('CL', 'es-mx'), ('CM', 'fr'), ('CN', 'zh-sg'), ('CO', 'es-mx'), ('CR', 'es-mx'), ('CU', 'es-mx'), ('CV', 'en'), ('CW', 'en'), ('CX', 'en'), ('CY', 'en'), ('CZ', 'cs'), ('DE', 'de'), ('DJ', 'fr'), ('DK', 'en'), ('DM', 'en'), ('DO', 'es-mx'), ('DZ', 'en'), ('EC', 'es-mx'), ('EE', 'en'), ('EG', 'en'), ('EH', 'en'), ('ER', 'en'), ('ES', 'en'), ('ET', 'en'), ('EU', 'en'), ('FI', 'en'), ('FJ', 'en'), ('FK', 'en'), ('FM', 'en'), ('FO', 'en'), ('FR', 'fr'), ('GA', 'fr'), ('GB', 'en'), ('GD', 'en'), ('GE', 'en'), ('GF', 'en'), ('GG', 'en'), ('GH', 'en'), ('GI', 'en'), ('GL', 'en'), ('GM', 'en'), ('GN', 'fr'), ('GP', 'en'), ('GQ', 'en'), ('GR', 'en'), ('GS', 'en'), ('GT', 'es-mx'), ('GU', 'en'), ('GW', 'en'), ('GY', 'en'), ('HK', 'zh-tw'), ('HM', 'en'), ('HN', 'es-mx'), ('HR', 'en'), ('HT', 'en'), ('HU', 'en'), ('ID', 'en'), ('IE', 'en'), ('IL', 'en'), ('IM', 'en'), ('IN', 'en'), ('IO', 'en'), ('IQ', 'en'), ('IR', 'en'), ('IS', 'en'), ('IT', 'it'), ('JE', 'en'), ('JM', 'en'), ('JO', 'en'), ('JP', 'ja'), ('KE', 'en'), ('KG', 'ru'), ('KH', 'en'), ('KI', 'en'), ('KM', 'fr'), ('KN', 'en'), ('KP', 'en'), ('KR', 'ko'), ('KW', 'en'), ('KY', 'en'), ('KZ', 'en'), ('LA', 'en'), ('LB', 'en'), ('LC', 'en'), ('LI', 'de'), ('LK', 'en'), ('LR', 'en'), ('LS', 'en'), ('LT', 'en'), ('LU', 'fr'), ('LV', 'en'), ('LY', 'en'), ('MA', 'fr'), ('MC', 'fr'), ('MD', 'ru'), ('ME', 'en'), ('MF', 'en'), ('MG', 'fr'), ('MH', 'en'), ('MK', 'en'), ('ML', 'fr'), ('MM', 'en'), ('MN', 'ru'), ('MO', 'zh-sg'), ('MP', 'en'), ('MQ', 'en'), ('MR', 'en'), ('MS', 'en'), ('MT', 'en'), ('MU', 'fr'), ('MV', 'en'), ('MW', 'en'), ('MX', 'es-mx'), ('MY', 'en'), ('MZ', 'en'), ('NA', 'en'), ('NC', 'en'), ('NE', 'fr'), ('NF', 'en'), ('NG', 'en'), ('NI', 'es-mx'), ('NL', 'en'), ('NO', 'en'), ('NP', 'en'), ('NR', 'en'), ('NU', 'en'), ('NZ', 'en'), ('O1', 'en'), ('OM', 'en'), ('PA', 'es-mx'), ('PE', 'es-mx'), ('PF', 'en'), ('PG', 'en'), ('PH', 'en'), ('PK', 'en'), ('PL', 'pl'), ('PM', 'en'), ('PN', 'en'), ('PR', 'es-mx'), ('PS', 'en'), ('PT', 'en'), ('PW', 'en'), ('PY', 'es-mx'), ('QA', 'en'), ('RE', 'fr'), ('RO', 'en'), ('RS', 'en'), ('RW', 'fr'), ('SA', 'en'), ('SB', 'en'), ('SC', 'fr'), ('SD', 'en'), ('SE', 'en'), ('SG', 'zh-sg'), ('SH', 'en'), ('SI', 'en'), ('SJ', 'en'), ('SK', 'cs'), ('SL', 'en'), ('SM', 'it'), ('SN', 'fr'), ('SO', 'en'), ('SR', 'en'), ('ST', 'en'), ('SV', 'es-mx'), ('SX', 'en'), ('SY', 'en'), ('SZ', 'en'), ('TC', 'en'), ('TD', 'fr'), ('TF', 'fr'), ('TG', 'fr'), ('TH', 'en'), ('TJ', 'ru'), ('TK', 'en'), ('TL', 'en'), ('TM', 'ru'), ('TN', 'fr'), ('TO', 'en'), ('TR', 'en'), ('TT', 'en'), ('TV', 'en'), ('TW', 'zh-tw'), ('TZ', 'en'), ('UA', 'en'), ('UG', 'en'), ('UM', 'en'), ('US', 'en'), ('UY', 'es-mx'), ('UZ', 'ru'), ('VA', 'it'), ('VC', 'en'), ('VE', 'es-mx'), ('VG', 'en'), ('VI', 'en'), ('VN', 'en'), ('VU', 'en'), ('WF', 'en'), ('WS', 'en'), ('YE', 'en'), ('YT', 'fr'), ('ZA', 'en'), ('ZM', 'en'), ('ZW', 'en')])
country_domain_map = {'AD': 'eu', 'AE': 'eu', 'AF': 'eu', 'AG': 'com', 'AI': 'com', 'AL': 'eu', 'AM': 'eu', 'AO': 'eu', 'AP': 'asia', 'AQ': 'com', 'AR': 'com', 'AS': 'com', 'AT': 'eu', 'AU': 'asia', 'AW': 'com', 'AX': 'eu', 'AZ': 'eu', 'BA': 'eu', 'BB': 'com', 'BD': 'asia', 'BE': 'eu', 'BF': 'eu', 'BG': 'eu', 'BH': 'eu', 'BI': 'eu', 'BJ': 'eu', 'BL': 'com', 'BM': 'com', 'BN': 'asia', 'BO': 'com', 'BQ': 'com', 'BR': 'com', 'BS': 'com', 'BT': 'asia', 'BV': 'com', 'BW': 'eu', 'BZ': 'com', 'CA': 'com', 'CC': 'com', 'CD': 'eu', 'CF': 'com', 'CG': 'eu', 'CH': 'eu', 'CI': 'eu', 'CK': 'com', 'CL': 'com', 'CM': 'eu', 'CN': 'asia', 'CO': 'com', 'CR': 'com', 'CU': 'com', 'CV': 'eu', 'CW': 'com', 'CX': 'asia', 'CY': 'eu', 'CZ': 'eu', 'DE': 'eu', 'DJ': 'eu', 'DK': 'eu', 'DM': 'com', 'DO': 'com', 'DZ': 'eu', 'EC': 'com', 'EE': 'eu', 'EG': 'eu', 'EH': 'eu', 'ER': 'eu', 'ES': 'eu', 'ET': 'eu', 'EU': 'eu', 'FI': 'eu', 'FJ': 'asia', 'FK': 'eu', 'FM': 'asia', 'FO': 'eu', 'FR': 'eu', 'GA': 'eu', 'GB': 'eu', 'GD': 'com', 'GE': 'eu', 'GF': 'com', 'GG': 'eu', 'GH': 'eu', 'GI': 'eu', 'GL': 'com', 'GM': 'eu', 'GN': 'eu', 'GP': 'com', 'GQ': 'eu', 'GR': 'eu', 'GS': 'com', 'GT': 'com', 'GU': 'com', 'GW': 'eu', 'GY': 'com', 'HK': 'asia', 'HM': 'com', 'HN': 'com', 'HR': 'eu', 'HT': 'com', 'HU': 'eu', 'ID': 'asia', 'IE': 'eu', 'IL': 'eu', 'IM': 'eu', 'IN': 'asia', 'IO': 'asia', 'IQ': 'eu', 'IR': 'eu', 'IS': 'eu', 'IT': 'eu', 'JE': 'eu', 'JM': 'com', 'JO': 'eu', 'JP': 'asia', 'KE': 'eu', 'KG': 'eu', 'KH': 'asia', 'KI': 'asia', 'KM': 'eu', 'KN': 'com', 'KP': 'asia', 'KR': 'asia', 'KW': 'eu', 'KY': 'com', 'KZ': 'eu', 'LA': 'asia', 'LB': 'eu', 'LC': 'com', 'LI': 'eu', 'LK': 'asia', 'LR': 'eu', 'LS': 'eu', 'LT': 'eu', 'LU': 'eu', 'LV': 'eu', 'LY': 'eu', 'MA': 'eu', 'MC': 'eu', 'MD': 'eu', 'ME': 'eu', 'MF': 'com', 'MG': 'eu', 'MH': 'asia', 'MK': 'eu', 'ML': 'eu', 'MM': 'asia', 'MN': 'eu', 'MO': 'asia', 'MP': 'asia', 'MQ': 'com', 'MR': 'eu', 'MS': 'com', 'MT': 'eu', 'MU': 'eu', 'MV': 'asia', 'MW': 'eu', 'MX': 'com', 'MY': 'asia', 'MZ': 'eu', 'NA': 'eu', 'NC': 'com', 'NE': 'eu', 'NF': 'com', 'NG': 'eu', 'NI': 'com', 'NL': 'eu', 'NO': 'eu', 'NP': 'asia', 'NR': 'asia', 'NU': 'asia', 'NZ': 'asia', 'O1': 'eu', 'OM': 'eu', 'PA': 'com', 'PE': 'com', 'PF': 'asia', 'PG': 'asia', 'PH': 'asia', 'PK': 'eu', 'PL': 'eu', 'PM': 'com', 'PN': 'com', 'PR': 'com', 'PS': 'eu', 'PT': 'eu', 'PW': 'asia', 'PY': 'com', 'QA': 'eu', 'RE': 'eu', 'RO': 'eu', 'RS': 'eu', 'RW': 'eu', 'SA': 'eu', 'SB': 'asia', 'SC': 'eu', 'SD': 'eu', 'SE': 'eu', 'SG': 'asia', 'SH': 'eu', 'SI': 'eu', 'SJ': 'eu', 'SK': 'eu', 'SL': 'eu', 'SM': 'eu', 'SN': 'eu', 'SO': 'eu', 'SR': 'eu', 'ST': 'eu', 'SV': 'com', 'SX': 'com', 'SY': 'eu', 'SZ': 'eu', 'TC': 'com', 'TD': 'eu', 'TF': 'eu', 'TG': 'eu', 'TH': 'asia', 'TJ': 'eu', 'TK': 'com', 'TL': 'asia', 'TM': 'eu', 'TN': 'eu', 'TO': 'asia', 'TR': 'eu', 'TT': 'com', 'TV': 'asia', 'TW': 'asia', 'TZ': 'eu', 'UA': 'eu', 'UG': 'eu', 'UM': 'com', 'US': 'com', 'UY': 'com', 'UZ': 'eu', 'VA': 'eu', 'VC': 'com', 'VE': 'com', 'VG': 'com', 'VI': 'com', 'VN': 'asia', 'VU': 'asia', 'WF': 'asia', 'WS': 'com', 'YE': 'eu', 'YT': 'eu', 'ZA': 'com', 'ZM': 'eu', 'ZW': 'eu', '01': 'cn'}
langs = list({val for key, val in country_lang_map.items()})
domains = ['eu', 'com', 'asia', 'cn']

text_temp = '''"note": null,
"code": "%s",
"name": "%s",
"urls": [
    {
        "url": "%s",
        "country": "%s"
    },'''

# Layout elements
title = html.H1('TE JSON Generator', id='title1')
input_name = dbc.Input(id='input_name', placeholder="WGC_128_CMPT_KOTS_finals_MARCOM_1195")
check_armory = dcc.Checklist(['Armory'], [], id='check_armory', labelStyle={"display": "flex", "align-items": "center"})
check_lang = dcc.Checklist(['/lang/'], [], id='check_lang', labelStyle={"display": "flex", "align-items": "center"})
check_ingame = dcc.Checklist(['/news_ingame/'], [], id='check_ingame', labelStyle={"display": "flex", "align-items": "center"})
input_url = dbc.Input(id='input_url', placeholder="https://worldofwarships.eu/news/general-news/kots-xvi")
btn_download = dbc.Button('Download JSON', id='btn_download', color="primary",
                       outline=True, n_clicks=0, disabled=False, 
                          style = {'width':'180px'})

# Layout body
tab1_content = dbc.Container(
html.Div([
    dbc.Row([title], style = {'margin-left':'7px', 'margin-top':'40px', 'margin-bottom':'20px'}),
    dbc.Row([dbc.Col([input_name], width=6), 
             dbc.Col([check_armory], width=1), dbc.Col([check_lang], width=1), dbc.Col([check_ingame], width=1)]),   
    dbc.Row([dbc.Col([input_url], width=9),
             dbc.Col([btn_download])], style = {'margin-top':'7px'}, align="center"),
    dbc.Row([html.Div(id='output_parse', style = {'color':'#90EE90'}),
            html.Div(id='trigger', children=0, style=dict(display='none'))]),
            html.Div(id='url_note', children=''),
    html.H6('JSON example:', style={'margin-top':'30px'}),
    dcc.Textarea(
        id='json_example',
        value= text_temp % (code_temp, name_temp, url_temp, 'AD'),
        style={'width': '90%', 'height': 210},
        draggable = False,
        readOnly=True),
    dcc.Download(id='download_json'),
        ], className='main_div'
),style={"height": "100vh", "width": "70%", "font-family":"Motiva Sans, Sans-serif"})

tab2_content = dbc.Container(
    html.Div(
        [html.P("This is Tool#2!", className="card-text"),
        dbc.Button("Don't click here", color="danger")]
    ), className="mt-3")

tabs = dbc.Tabs(
    [dbc.Tab(tab1_content, label="TE json"),
    dbc.Tab(tab2_content, label="Tool#2"),
    dbc.Tab("This tab's content is never seen", label="Tool#3")])

app.layout = html.Div([tabs])

# Callbacks
# Update checklist on changing url
@callback(Output('check_armory', 'value'), Output('check_lang', 'value'), Output('check_ingame', 'value'), 
          Input('input_url', 'value'), prevent_initial_call=True)
def check_url_params(url):
    if url_is_valid(url):
        armory = ['Armory'] if 'armory.' in url else ['']
        lang = ['/lang/'] if any(['/'+l+'/' in url for l in langs + ['zh-cn']]) else ['']
        news_ingame = ['/news_ingame/'] if '/news_ingame/' in url else ['']
        return armory, lang, news_ingame
    else:
        return [], [], []

# Update json example on parametars changes
@callback(Output('json_example', 'value'), Output('url_note', 'children'),
          Input('input_url', 'value'), Input('input_name', 'value'), Input('check_armory', 'value'), 
          Input('check_lang', 'value'), Input('check_ingame', 'value'), 
          State('input_name', 'placeholder'), State('input_url', 'placeholder'),
          prevent_initial_call=True)
def update_json_example(val_url, val_name, val_armory, val_lang, val_news_ingame, name_place, url_place):
    armory = 'armory.' if 'Armory' in val_armory  else ''
    news_ingame = 'news_ingame/' if '/news_ingame/' in val_news_ingame else ''
    name = val_name if val_name is not None else name_place
    code = name.lower().replace('_','-').replace(' ','-')
    url = val_url if val_url is not None else url_place
    lang = '' if '/lang/' not in val_lang else 'en/' if '.cn/' not in url else 'zh-cn/'
    domain = 'cn'  if '.cn/' in url  else country_domain_map['AD']
    country = '01'  if '.cn/' in url  else 'AD'
    if url_is_valid(url):
        url_univ = get_universal_url(url) % (armory, news_ingame)
        url_note = ''
    else:
        url_univ = get_universal_url(url_place) % (armory, news_ingame)
        url_note = 'wrong url'
    return text_temp % (code, name, url_univ.format(domain + '/', lang), country), url_note

# Download json on button click
@callback(Output('download_json', 'data'), 
          Input('btn_download', 'n_clicks'), State('input_url', 'value'), State('input_name', 'value'), State('check_armory', 'value'), 
          State('check_lang', 'value'), State('check_ingame', 'value'), State('url_note', 'children'), prevent_initial_call=True)
def download_json(n_clicks, url, val_name, val_armory, val_lang, val_news_ingame, url_note):
    if n_clicks > 0 and url is not None and val_name is not None and url_note == '':
        armory = 'armory.' if 'Armory' in val_armory  else ''
        news_ingame = 'news_ingame/' if '/news_ingame/' in val_news_ingame else ''
        url_univ = get_universal_url(url) % (armory, news_ingame)
        code = val_name.lower().replace(' ', '-').replace('_', '-')
        template_data= {"lpsets": [{"note": "", "code": code, "name": val_name, "urls": []}]}
        country_lang_map_used = {'01':'zh-cn'} if '.cn/' in url else country_lang_map
        # Create json tempalte
        for country, lang in country_lang_map_used.items():
            lang = lang + '/' if '/lang/' in val_lang else ''
            template_data['lpsets'][0]['urls'].append({'url':url_univ.format(country_domain_map[country] + '/', lang), 'country':country})
        content = json.dumps(template_data, indent=4)
        filename = val_name + '_te_links.json'
        return dict(content=content, filename=filename)

if __name__ == "__main__":
    app.run_server(debug=True)