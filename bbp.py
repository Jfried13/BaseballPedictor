import requests
from bs4 import BeautifulSoup
import csv
import pymysql


first_name = []
last_name = []
team = []
pos = []
G = []
AB = [] 
R = []
H = []
DOUBLES = []
TRIPLES = []
RBI = []
HR = []
SB = []
walk = []
CS = []
HBP = []
AVG = []
OPS = []
OBP = []
SLG = []
SO = []
SH = []
SF = []

itemBank = []

page = requests.get('https://www.rotowire.com/baseball/player_stats.htm?season=2011')
soup = BeautifulSoup(page.text, 'html.parser')

body = soup.find_all('tbody')
trs = body[0].find_all('tr')
#print(len(trs))
p = trs[0]
ps = p.find_all('td')
for player in trs:
    player_stats = player.find_all('td')
    player_name = [x.strip() for x in player_stats[0].text.split(',')]
    if "'" in player_name[0]:
       print("TRUE")
       print(player_name)
       tempName = player_name[0].replace("'", '')
       print(tempName)
       last_name.append(tempName)
    else:
       last_name.append(player_name[0])
    first_name.append(player_name[1])
    team.append(player_stats[1].text)
    pos.append(player_stats[2].text)
    G.append(player_stats[3].text)
    AB.append(player_stats[4].text)
    R.append(player_stats[5].text)
    H.append(player_stats[6].text)
    DOUBLES.append(player_stats[7].text)
    TRIPLES.append(player_stats[8].text)
    HR.append(player_stats[9].text)
    RBI.append(player_stats[10].text)
    SB.append(player_stats[11].text)
    CS.append(player_stats[12].text)
    walk.append(player_stats[13].text)
    SO.append(player_stats[14].text)
    SH.append(player_stats[15].text)
    SF.append(player_stats[16].text)
    HBP.append(player_stats[17].text)
    AVG.append(player_stats[18].text)
    OBP.append(player_stats[19].text)
    SLG.append(player_stats[20].text)
    OPS.append(player_stats[21].text)



# Open database connection
db = pymysql.connect("localhost","root","password","TESTDB")

# prepare a cursor object using cursor() method
cursor = db.cursor()


insert_player = """INSERT INTO PLAYER(FIRST_NAME, LAST_NAME, TEAM, \
				POS, GAMES, AB, RUNS, HITS, DOUBLES, TRIPLES, RBI, HR, \
				SB, WALKS, CS, HBP, AVG, OPS, OBP, SLG, SH, SF) \
				VALUES ('%s', '%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', \
						'%d', '%f', '%f', '%f', '%f', '%d', '%d' )"""


create_player_table = """CREATE TABLE PLAYER (
   FIRST_NAME  CHAR(20) NOT NULL,
   LAST_NAME  CHAR(20) NOT NULL,
   TEAM CHAR(20) NOT NULL,
   POS CHAR(5) NOT NULL,
   GAMES INT NOT NULL,
   AB INT NOT NULL,
   RUNS INT NOT NULL,
   HITS INT NOT NULL,
   DOUBLES INT NOT NULL,
   TRIPLES INT NOT NULL,
   RBI INT NOT NULL,
   HR INT NOT NULL,
   SB INT NOT NULL,
   WALKS INT NOT NULL,
   CS INT NOT NULL,
   HBP INT NOT NULL,
   AVG FLOAT NOT NULL,  
   OPS FLOAT NOT NULL,
   OBP FLOAT NOT NULL,
   SLG FLOAT NOT NULL,
   SH INT NOT NULL,
   SF INT NOT NULL)"""

for index in range(0, 663):
      itemBank.append((
         last_name[index],
         first_name[index],
         team[index],
         pos[index],
         int(G[index]),
         int(AB[index]),
         int(R[index]),
         int(H[index]),
         int(DOUBLES[index]),
         int(TRIPLES[index]),
         int(HR[index]),
         int(RBI[index]),
         int(SB[index]),
         int(CS[index]),
         int(walk[index]),
         int(SO[index]),
         int(SH[index]),
         int(SF[index]),
         int(HBP[index]),
         float(AVG[index]),
         float(OBP[index]),
         float(SLG[index]),
         float(OPS[index])
      ))


try:
   #print(itemBank)
   # Execute the SQL command
   cursor.execute("DROP TABLE IF EXISTS PLAYER")
   cursor.execute(create_player_table)
   
   for num in range(0,663):
   #while num < 663:
      print("inserting player number {}".format(num))
      cur_player_insert = "INSERT INTO PLAYER(FIRST_NAME, LAST_NAME, TEAM, POS, \
         GAMES, AB, RUNS, HITS, DOUBLES, TRIPLES, RBI, HR, \
         SB, WALKS, CS, HBP, AVG, OPS, OBP, SLG, SH, SF) \
         VALUES ('%s', '%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', \
         '%d', '%f', '%f', '%f', '%f', '%d', '%d' )" % \
         (first_name[num], last_name[num], team[num], pos[num], int(G[num]), int(AB[num]), int(R[num]), int(H[num]), int(DOUBLES[num]), 
		 int(TRIPLES[num]), int(RBI[num]), int(HR[num]), int(SB[num]), int(walk[num]), int(CS[num]), int(HBP[num]), float(AVG[num]), 
		 float(OPS[num]), float(OBP[num]), float(SLG[num]), int(SH[num]), int(SF[num]))
      cursor.execute(cur_player_insert)
   # Commit your changes in the database
      db.commit()
   #print("SQUEEK")
   #cursor.executemany(insert_player, itemBank)
   #print('here')
   #db.commit()
except:
    # Rollback in case there is any error
    db.rollback()

# disconnect from server
db.close()

