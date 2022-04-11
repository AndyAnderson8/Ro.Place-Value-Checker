import math
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import math

reverseList = True # easier to view set to True if you have several items matching criteria
itemForTradeRAP = 800 # if wanted included in value calculation
maxUSDPrice = 1000
maxRatePer1kValue = 4
unwantedItems = ["Noob Attack - Frozen Crossbow Collision", "Kuddle E. Koala", "Starry Egg of the Wild Ride", "Agonizingly Ugly Egg of Screensplat", "Vicious Egg of Singularity", "Noob Attack: Laser Scythe Scuffle", "Specular Egg of Red, No Blue", "2009 Graduation Cap", "Scenic Egg of the Clouds", "Noob Attack: Scythe Strike", "Chrome Egg of Speeding Bullet", "Noob Assist: Basketball Buddy", "Steampunk Robin Hood", "Tabby Egg", "Noob Attack: Golden Sword Gladiator", "Captain Steampunk", "Bat Tie", "Zeno's Egg of Paradox", "Dreamweaver FabergÃ© Egg", "Egg of Equinox: Night", "Egg of Equinox: Day", "Earth Day 2011 Tie", "Aqueous Egg of River Riding", "Golden Pilgrim Hat", "Aqueous Egg of River Riding", "Noob Assist Gingerbread Gratitude", "Purple Steampunk Robin Hood", "Radioactive Egg of Undead Apocalypse", "Noob Assist: Undead Unrest", "POW! To the Moon! Egg", "Gobble Gobble", "Chill Cap", "Noob Attack: Gearworks Grapple", "Racing Helmet", "Sword pack", "Shooting Star", "Egg of Verticality", "Stationary Egg of Boring", "Halloween Baseball Cap 2014", "Turkey Tie 2012", "Noob Assist: Sandwich Scramble", "Festive Narwhal", "Elegant FabergÃ© Egg of Fancy Times", "Noob Attack: Raig Table Revenge", "Charles Babbage FabergÃ© Egg", "Chaos Canyon Sugar Egg", "The Last Egg", "Purple Crazy Glasses", "Red FabergÃ© Egg", "Pi RAIG Table", "Eggcognito Egg", "Eggrachnophobia", "White Ninja Headband of the Unimpeachable Soul", "Valentine's Day Cap 2014", "Noob Attack: Laser Scythe Scuffle", "Blue FabergÃ© Egg", "2010 Fireworks", "Apple Pie", "Noob Attack - Frozen Crossbow Collision", "Crossroads Sugar Egg", "Chillin' Headrow", "Pumpkin Pi", "Noob Assist: Taxing Taxation", "Fiery Egg of Egg Testing", "Noob Assist: Astronaut Action", "Starry Egg of the Wild Ride", "Shaggy", "Riptide"] # full names seperated by quotations and a comma

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('chromedriver', options=options)

def underlinePrint(string):
  length = len(string)
  underline = ""
  while length > 1:
    underline += "—"
    length -= 1
  print(string)
  print(underline)

def fetchRolimonsData():
  response = requests.get("https://www.rolimons.com/itemapi/itemdetails")
  return response.json()["items"]

underlinePrint("RBX.PLACE RAP VALUE CALCULATOR")
while True:
  rolimonsData = fetchRolimonsData()
  rolimonsAssetIDs = list(rolimonsData.keys())

  driver.get("https://beta.ro.place/")
  WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[2]/div[3]/div[1]/div/img')))

  names = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[3]/*/div/div/div/span[1]')
  usds = driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[3]/*/div/div/span')
  assetIDs = driver.find_elements_by_xpath('//*[@id="root"]/div[2]/div[3]*/div/img').get_attribute("src").split("=")[0].split("&")[0]

  print("Gathering data... (" + str(len(names)) + " Items)\n")

  for name in names:
    usd = float(usds[i].text.replace("$", ""))
    assetID = assetIDs[i]
    value = rolimonsData[assetID][4]
    ratio = round(usd / (value - itemForTradeRAP + 0.00000000000000001), 2)
    name = name.text 
	
    if value < (itemForTradeRAP/1000):
      break

    elif usd <= maxUSDPrice and ratio <= maxRatePer1kValue and name not in unwantedItems:

      if math.floor(usd*10)/10 == usd: #check to see if number is gonna say $0.1 instead of $0.10
        usd = str(usd) + "0"

      if math.floor(ratio*10)/10 == ratio: #check to see if number is gonna say $0.1 instead of $0.10
        ratio = str(ratio) + "0"

      vals[str(ratio)] = [name, str(usd), str(value)]
      print("Indexing data from " + name + " | (Item " + str(i+1) + "/" + str(len(names)) + ")")

    i = i + 1

  if len(vals) >= 1:
    if oldVals != vals:

      print("\nNew item(s) found!")

      if len(vals) > 1:

        print("\nSorting data... (" + str(len(vals)) + " Items)")
        vals = dict(sorted(vals.items()))

        if reverseList == True:
          vals = dict(reversed(vals.items()))

      print("\n------------------------------")
      for val in vals:
        data = vals[val]
        if oldVals != vals:
          e = 0
          print("\n" + data[0] + "\nUSD: $" + data[1] + "\nRValue: " + data[2] + "k R$\nRate: $" + val + "/1k Value")
      print("\n------------------------------\n")
			
      playsound('alert.mp3')

    else:
      e = e + 1
      print("\nNo new items matching criteria, rechecking... (" + str(e) + ")\n")

  else:
    e = e + 1
    print("No items meet criteria, rechecking... (" + str(e) + ")\n")

  i = 0
  oldVals = vals
  vals = {}