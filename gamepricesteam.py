import requests, bs4, json, time

setgames = []
games = []
naoprecificado = []
resAllGamesSteam = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/');
resAllGamesSteam.raise_for_status();

def findGameCatalogPricesDB(name):
    query =  json.dumps({"name": name})
    url = 'https://api.mlab.com/api/1/databases/randomkeysbox/collections/games?apiKey=j7xm963vICVfSSop9KrwWraF8fMMf9_w&q=' + query
    try:
      return json.loads(requests.get(url).text)
    except:
      return {}


def getSteamPrice(name):
  price = 0;
  datastore = json.loads(resAllGamesSteam.text);
  apps = datastore["applist"]["apps"];
  steamGame = list(filter(lambda g: g['name'].strip().upper() == name.strip().upper(), apps));
  appid = 0;
  
  if(len(steamGame) > 0):
    appid = steamGame[0]['appid'];
  if(appid == 0):
    return 0;  	
  
  resSteamApi = requests.get('https://store.steampowered.com/api/appdetails?appids=' + str(appid) + '&cc=brl');
  resSteamApi.raise_for_status();
  datastore = json.loads(resSteamApi.text)[str(appid)];

  if('data' in datastore):
    datastore = datastore['data']
    if('price_overview' in datastore.keys()):
      price = datastore['price_overview']['initial'];
  
  return price;

def toFloat(value):
 strV = str(value);
 strV = strV[0:len(strV)-2] + '.' + strV[len(strV)-2:];
 return float(strV);

def addGame(dict):
  if dict['name'] not in setgames:
    setgames.append(dict['name'])
    games.append(dict)

f = open('steamgames.txt', 'r');

for name in set(f):
  price = toFloat(getSteamPrice(name));
  if price == 0:
    catalog = findGameCatalogPricesDB(name)
    if 'message' not in catalog and len(catalog) > 0 and len(catalog[0]) == 3:
      catalog = catalog[0]
      addGame(catalog)  
    else:
      naoprecificado.append(name)  
  elif price >= 19.90:
    addGame({'name':name.strip(), 'price':price})

total = 0
for game in games:
  total = total + game['price']
  print(game['name'].strip() + ': ' + str(game['price']));

print('total:' + str(total) + "\n\n");

for i in naoprecificado:
  print(i)

f.close()