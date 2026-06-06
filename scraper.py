import pandas as pd
import requests
from bs4 import BeautifulSoup
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

res=requests.get("https://www.howstat.com/Cricket/Statistics/IPL/SeriesMatches.asp?s=2026")
print("status: ",res.status_code)
#print(res.text[:1000])

soup=BeautifulSoup(res.text,"html.parser")

tables=soup.find_all("table")

table=tables[3]
match_rows=table.find_all("tr")
#print(len(match_rows))
"""for row in rows[1:11]:
    cols=row.find_all("td")
    print(cols[0].text)"""

#cols=match_rows[3].find_all("td")


data=[]
for match_row in match_rows[3:13]:
    cols=match_row.find_all("td")

    date=cols[1].text.strip()
    teams_text=cols[2].text.strip()
    venue=cols[3].text.strip()
    result=cols[4].text.strip()
    if " v " in teams_text:
        team1,team2=teams_text.split(" v ", 1)
    else:
        team1,team2=teams_text, ""
    link=cols[5].find("a")

    scorecard_url = ("https://www.howstat.com/Cricket/Statistics/IPL/"+link["href"])
    score_res=requests.get(scorecard_url)
    score_soup=BeautifulSoup(score_res.text,"html.parser")
    score_tables=score_soup.find_all("table")
    players=[]
    for table_index in [5,7]:
        try:
            batting_table=score_tables[table_index]
            for batting_row in batting_table.find_all("tr"):
                batting_cols =batting_row.find_all("td")
                if len(batting_cols)>=3:
                    try:
                        player=batting_cols[0].text.strip()
                        if player.upper()=="TOTAL":
                            continue
                        if player.upper()=="EXTRAS":
                            continue
                        runs=int(batting_cols[2].text.strip())
                        players.append((player,runs))
                    except:
                        pass
        except IndexError:
            pass
    #print(players)
    top_scorer=max(players,key=lambda x:x[1])

    data.append({
        "date":date,
        "team1":team1,
        "team2":team2,
        "venue":venue,
        "result":result,
        "top_scorer":top_scorer[0],
        "score":top_scorer[1]
    })
df=pd.DataFrame(data)
print(df)
df.to_csv("match_data.csv",index=False)