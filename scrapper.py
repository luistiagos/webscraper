import requests, bs4, json, time

dollarValue = 4.40;

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
  
  try:
    resSteamApi = requests.get('https://store.steampowered.com/api/appdetails?appids=' + str(appid) + '&cc=brl');
    resSteamApi.raise_for_status();
    datastore = json.loads(resSteamApi.text)[str(appid)];
  except:
    time.sleep(1)
    return getSteamPrice(name)  		

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

  names = soup.select('.DIG4-Orange-14');
  for e in names:
    name = e.getText().strip(); 
    games.append({"name":name, "valor":0, "valorLoja":0, "valorSteam":0});

  index = 0;
  prices = soup.select('.DIG4-White-14-Strike');
  for price in prices: 
    games[index]["valor"] = float(price.getText().strip()[1:]);
    index = index + 1;

  index = 0;
  pricesStore = soup.select('.DIG4-White-16');
  for store in pricesStore:
    if('$' in store.getText()):
      storePrice = store.getText().strip()[1:]; 
      if(len(storePrice) > 0):
        games[index]["valorLoja"] = float(storePrice);
        index = index + 1;

  preco = 0;	
  for game in games:
    name = game['name'].encode(encoding='UTF-8',errors='strict').decode('utf8');
    game['name'] = name;
    if (len(list(filter(lambda g: g['name'] == name, listGames))) == 0 and game["valor"] > 5 and game["valorLoja"] < 2.0):   
      preco = getSteamPrice(game['name']);	
      if (int(preco) >= 1900):
        game['valorSteam'] = preco;
        print(game);
        listGames.append(game);
        time.sleep(1);

listGames = [];
scrapper('http://www.dailyindiegame.com/site_list_topsellers.html', listGames);
scrapper('http://www.dailyindiegame.com/site_list_newgames.html', listGames);
scrapper('http://www.dailyindiegame.com/site_list_indievault.html', listGames);
scrapper('http://www.dailyindiegame.com/site_list_specials.html', listGames);

for i in range(0,19):
  scrapper('http://dailyindiegame.com/site_list_category-action_' + str(i) + '.html', listGames);

for i in range(0,14):
  scrapper('http://dailyindiegame.com/site_list_category-strategy_' + str(i) + '.html', listGames);

for i in range(0,9):
  scrapper('http://dailyindiegame.com/site_list_category-rpg_' + str(i) + '.html', listGames);

for i in range(0,19):
  scrapper('http://dailyindiegame.com/site_list_category-casual_' + str(i) + '.html', listGames);

for i in range(0,3):
  scrapper('http://dailyindiegame.com/site_list_category-racing_' + str(i) + '.html', listGames);

for i in range(0,2):
  scrapper('http://dailyindiegame.com/site_list_category-sports_' + str(i) + '.html', listGames);

for i in range(0,19):
  scrapper('http://dailyindiegame.com/site_list_category-indie_' + str(i) + '.html', listGames);

for i in range(0,19):
  scrapper('http://dailyindiegame.com/site_list_category-adventure_' + str(i) + '.html', listGames);

for i in range(0,6):
  scrapper('http://dailyindiegame.com/site_list_category-simulation_' + str(i) + '.html', listGames);

for i in range(0,2):
  scrapper('http://dailyindiegame.com/site_list_category-earlyaccess_' + str(i) + '.html', listGames);

for g in listGames:
  g["valorLoja"] = g["valorLoja"] * dollarValue;
  g["desconto"] = 100 - (g["valorLoja"] / g["valorSteam"]);

listGames = sorted(listGames, key = lambda i: (i['desconto']), reverse=True);

f= open("games.txt","w+");

for g in listGames:
  game = str(g["name"]) + '  ' + str(g["valorSteam"]) + '  ' + str(g["valorLoja"]);
  try:
    f.write(game + '\n');
  except:
    print("An exception occurred");

f.close();