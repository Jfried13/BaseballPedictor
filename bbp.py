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
SH = []
SF = []

page = requests.get('https://www.rotowire.com/baseball/player_stats.htm?season=2011')
soup = BeautifulSoup(page.text, 'html.parser')

body = soup.find_all('tbody')
trs = body[0].find_all('tr')

for player in trs:
	player_stats = player.find_all('td')
	player_name = [x.strip() for x in player_stats[0].text.split(',')]
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
	RBI.append(player_stats[9].text)
	HR.append(player_stats[10].text)
	SB.append(player_stats[11].text)
	walk.append(player_stats[12].text)
	CS.append(player_stats[13].text)
	HBP.append(player_stats[14].text)
	AVG.append(player_stats[15].text)
	OPS.append(player_stats[16].text)
	OBP.append(player_stats[17].text)
	SLG.append(player_stats[18].text)
	SH.append(player_stats[19].text)
	SF.append(player_stats[20].text)


# Open database connection
db = pymysql.connect("localhost","testuser","hello","TESTDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
   LAST_NAME, AGE, SEX, INCOME) \
   VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
   ('Macie', 'Mohan', 20, 'M', 2000)

insert_player = "INSERT INTO PLAYER(FIRST_NAME, LAST_NAME, TEAM, \
				POS, GAMES, AB, RUNS, HITS, DOUBLES, TRIPLES, RBI, HR, \
				SB, WALKS, CS, AVG, OPS, OBP, SLG, SH, SF) \
				VALUES ('%s', '%s', '%s', '%s', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', '%d', \
						'%f', '%f', '%f', '%f', '%d', '%d' )" % \
				(first_name[0], last_name[0], team[0], pos[0], G[0], AB[0], R[0], H[0], DOUBLES[0], TRIPLES[0], 
					RBI[0], HR[0], SB[0], walk[0], CS[0], HBP[0], AVG[0], OPS[0], OBP[0], SLG[0], SH[0], SF[0])

create_player_table = """CREATE TABLE PLAYER (
   FIRST_NAME  CHAR(20) NOT NULL,
   LAST_NAME  CHAR(20) NOT NULL,
   TEAM CHAR(20) NOT NULL,
   POS char(5) NOT NULL,
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
   AVG FLOAT NOT NULL,  
   OPS FLOAT NOT NULL,
   OBP FLOAT NOT NULL,
   SLG FLOAT NOT NULL,
   SH INT NOT NULL,
   SF INT NOT NULL)"""

try:
   # Execute the SQL command
   cursor.execute("DROP TABLE IF EXISTS PLAYER")
   cursor.execute(create_player_table)
   cursor.execute(insert_player)

   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()


	#for stat in player_stats:
	#	print(stat.text)
