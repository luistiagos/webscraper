import requests, bs4, json, time

dollarValue = 4;

resAllGamesSteam = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/');
resAllGamesSteam.raise_for_status();

def getSteamPrice(name):
  price = 0;
  datastore = json.loads(resAllGamesSteam.text);
  apps = datastore["applist"]["apps"];
  steamGame = list(filter(lambda g: g['name'] == name.strip(), apps));
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

def scrapper(url, listGames):
  res = requests.get(url)
  res.raise_for_status()
  soup = bs4.BeautifulSoup(res.text, "html.parser");
  games = [];
  gamesFiltered = [];

  li = soup.select('.products-grid');
  print(li);  

listGames = [];
scrapper('https://plati.market/', listGames);
