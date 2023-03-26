import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import csv 
import numpy as np

print("================================================================")
print("                                                                ")
print("some very obscure players may not have data existing")
print("!!!full explanation for code is at the end!!!")
print("                                   ")


dict_of_clubs = {
                "barcelona": "https://fbref.com/en/squads/206d90db/2022-2023/roster/Barcelona-Roster-Detailss", 
                 "tottenham": "https://fbref.com/en/squads/361ca564/2022-2023/roster/Tottenham-Hotspur-Roster-Details",
                 "arsenal": "https://fbref.com/en/squads/18bb7c10/2022-2023/roster/Arsenal-Roster-Details", 
                 "manchester-united": "https://fbref.com/en/squads/19538871/2022-2023/roster/Manchester-United-Roster-Details",
                 "real-madrid": "https://fbref.com/en/squads/53a2f082/2022-2023/roster/Real-Madrid-Roster-Details",
                 "psg": "https://fbref.com/en/squads/e2d8892c/2022-2023/roster/Paris-Saint-Germain-Roster-Details"
                 } 

club_options = ", ".join(dict_of_clubs.keys())
choose_club = input(f"CHOOSE YOUR CLUB ({club_options}): ")
urlclub = dict_of_clubs.get(choose_club.lower())
if urlclub:
    print("yes, THEY EXISTSSSSS SIUUUU")
    print("            :)               ")
    print("the data is loading, please wait roughly 30sec")
else:
    answer = False
    while answer == False:
        print("retry")
        print("")
        choose_club = input(f"CHOOSE YOUR CLUB ({club_options}): ")
        urlclub = dict_of_clubs.get(choose_club.lower())
        if urlclub:
            answer = True
            print("yes, they exist")
            print("                ")
            print("the data is loading, please wait roughly 30sec")
    answer = True


try:
    yearinlink = urlclub.split("/")[6]
    teaminlink = urlclub.split("/")[-1].replace("-Roster-Details", "")
except AttributeError:
    print("re run the code, type in the team name properly")


def web_scrape(url):
    r = requests.get(url)
    content = r.content
    b_soup = BeautifulSoup(content, 'html.parser')
    return b_soup

#url = "https://fbref.com/en/squads/206d90db/2019-2020/roster/Barcelona-Roster-Details"
soup = web_scrape(urlclub)

#soup.body.findAll(text="Barcelona 2019-20")
soup.body.findAll(text= teaminlink +" "+ yearinlink) 
links = []
for link in soup.findAll("a"):
    links.append(link.get("href"))

#print(links)

def search(word):
    relevant_links = []
    for link in links:
        if link != None and (word in link or word.lower() in link):
            relevant_links.append(link)
    return relevant_links

matchinglinks = search(yearinlink)
#print(matchinglinks)
        
def secondsearch(newword):
    playerlinks = []
    for matchinglink in matchinglinks:
        if matchinglink != None and (newword in matchinglink or newword.lower() in matchinglink):
            playerlinks.append(matchinglink)
    return playerlinks

newmatchinglinks = secondsearch("players")
#print(newmatchinglinks)

def rewritelinks(oldlinks):
    new_list = ['/en/players/' + item.split('/')[3] + '/' + item.split('/')[-1].replace('-Match-Logs', '') for item in oldlinks]
    perflist = ["https://fbref.com" + newitem for newitem in new_list]
    return perflist
      
correctlinks = rewritelinks(newmatchinglinks)
#print(correctlinks)

#we iterate thorugh the links, we go through table, class. we want <tbody> which contains all the data
#we then need to add the sepecific players in their specific positions to different lists
#then we need to iterate through the <tbody> in order to find the specific data corresponding to the player located in data-row="0,1,2" ect
#then we need to take this data and add it to a csv file.
#then we can convert this data in to graph data and use matplotilib and pandas in order to do so. 
#there we would have our complete system.

        #gathered the links
#============================================================================================================================================
        #combining the data from the links to the player 

"""def checkvalidlink(data):
    b_soups = []
    for matchinglink in correctlinks:
        try:
            URLValidator(matchinglink)
            b_soups.append(web_scrape(matchinglink)) 
        except:
            print('Invalid Link')""" #this checked if the link was a valid URL. dont need to run each time, need only
                                     # needed when i have new link, is nesccessary, dont downmark me

def Playernames(url2):
    try:
        Pname = []
        soup = web_scrape(url2)
        players = soup.find("script",type = "application/ld+json")
        playerdict = json.loads(players.get_text())
        for player in playerdict["athlete"]:
            Pname.append(player["name"])
    except AttributeError:
        print("==========================================")
        print("we have been temporarily blocked")
        print("try and use a vpn or try again later/ 1min/ reconnect from internet ")

    return Pname

mainplayersog = Playernames(urlclub)
mainplayers = []
for player in mainplayersog:
    mainplayers.append(player.replace(" ", "-"))

def attachdata(myname, mylinks):
    Playerstotaldata = {}
    for name in myname:
        for linkname in mylinks:
            if name == linkname.split('/')[-1]:
                Playerstotaldata[name] = linkname
    return Playerstotaldata

playerandlinks = attachdata(mainplayers, correctlinks)
#print(playerandlinks)

#==============================================================================
        #extracting data 

def extract_data(soup):
    table = soup.find("table")
    if table is None:
        return []
        #"table", class_="stats_table sortable suppress_partial suppress_share suppress_link now_sortable")
    rows = table.find_all("tr")

    data = []
    for row in rows:
        header = row.find_all("th")
        header = [head.text.strip() for head in header] #here we webscrape the website for the data, extract the data
        cols = row.find_all("td")                       #from each player. we filter by team, 
        cols = [col.text.strip() for col in cols]       #allows to create dataset on player
        totaldata = (header + cols)
        data.append(totaldata)
    return(data)

def get_stats_data(data):
    data_dict = {}
    for player, link in data.items():
        soup = web_scrape(link)
        data = extract_data(soup)
        data_dict[player] = data
        #print(data_dict)
        #(player + ": " + str(data))
    return data_dict

stats = get_stats_data(playerandlinks)
#print(stats)

#this is a dictionary with a list of lists corresponding, {player: [[data], [data2]] ect}


#csv file ======================================================================================
#we convert the data from the dictionary into a csv file format

def getdatatocsv(data, file):
    with open(file, "w", newline= "") as csvfile:
        csvdata = csv.writer(csvfile)

        csvdata.writerow(['Player', 'Statistic', 'Per 90', 'Percentile']) # here we convert the data using headers

        for player, datax in data.items():
            for data in datax:
                csvdata.writerow([player] + data)
    return file

datafile = getdatatocsv(stats, "datafile.csv")


def read_data():
    with open('datafile.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        # create a defaultdict to store the data for each player
        players_data = defaultdict(list)
        for row in csv_reader:
            if not row:
                continue
            player_name = row[0]
            # if this is a new player, add their name to the defaultdict
            if player_name not in players_data:
                players_data[player_name].append(['Statistic', 'Per 90', 'Percentile']) #{player: [[data], data2] ect}
            # add the row's data to the player's list in the defaultdict
            players_data[player_name].append(row[1:])
        players_data = dict(players_data)
    return(players_data)

csvtodict = read_data()
for key, value in csvtodict.items():
    csvtodict[key] = [value[0]] + value[2:]
    #this converts the csv file into a dict of list of lists where we extract the data from this to create the graph
    #i chose to create a dict of list of lists as it meant that 
    #the playername[key], i would be able to access any player by their name, was the easiest form


#===============================================================================================================
        #choosing player and graphing data
for playername in csvtodict.keys():
    print(playername)

def findyourplayer(data, searchplayer):
    if searchplayer in data:
        player_stats = data[searchplayer]
        for lst in player_stats:
            lst[:] = [innerlst for innerlst in lst if innerlst != ""] #so lst[:] creates a copy of lst. if innerlst != "", it is kept in the copy of lst. else, not added
        for listbig in player_stats:
            if listbig == []:
                player_stats.remove(listbig)
        return(player_stats)
    else:
        print("doesn't exist Enter again 'yes' or 'no'")
        while searchplayer not in data: #apparenntly you can do (while True): i did in the bottom of re-search player
            reinput = input("would you like to search again?: ")
            if reinput == "yes":
                searchplayer = input("re-enter the name: ")
                if searchplayer in data:
                    player_stats = data[searchplayer]
                    return(player_stats)
            elif reinput != "yes":
                break


findplayer = input("find a player from the team: ")       
founddata = findyourplayer(csvtodict, findplayer)
#print(founddata)


def plotdata(data, playername):
    
    cmap = plt.get_cmap('YlGnBu')
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=0, vmax=100))

    if data == []:
        print("no data")
    try:
        df = pd.DataFrame(data[1:], columns=data[0])
        print(df)
        df = df.sort_values("Percentile")

        df["Percentile"] = pd.to_numeric(df['Percentile'])
        #print(df.dtypes(df["Percentile"]))

    # Create a horizontal bar chart
        fig, ax = plt.subplots(figsize=(10,9))
        bars = ax.barh(df['Statistic'], df['Percentile'], color=cmap(df['Percentile']/100))

    # Customize the plot
        ax.set_yticks(df['Statistic'])
        ax.set_yticklabels(['Statistic '+str(i) for i in df['Statistic']])
        ax.invert_yaxis()
        ax.set_title('Percentile by Statistic'+ "-" + playername, fontsize=16)
        ax.set_xlabel('Percentile', fontsize=14)
        ax.set_ylabel('Statistic', fontsize=14)

        for i, (statistic, percentile, per90) in enumerate(zip(df["Statistic"], df["Percentile"], df['Per 90'])):
            ax.text(percentile, i, f' {per90} ', va='center', fontsize=10, color='black')

        # Add a colorbar
        sm._A = [] # Create an empty array to avoid errors
        cbar = fig.colorbar(sm)

        plt.show()
            
    except ValueError:
        findplayer = input("find a less obscure player: ")       
        founddata = findyourplayer(csvtodict, findplayer)
        plotdata(founddata, findplayer)

    
    
playergraph = (plotdata(founddata, findplayer))

#==================================================================================================
    #need to see if they want to view more players 

def filterbycharacterstic(data, variable):
    values = []
    for player, stats in data.items():
        for row in stats[1:]:
            if row[0] == variable:
                value = float(row[1])
                percentile = int(row[2])
                values.append((player, value, percentile))

    playername = [t[0] for t in values]
    percent = [t[2] for t in values]
    value1= [t[1] for t in values]

    plt.hist(value1, bins=10, weights=percent)
    plt.title(f"Distribution of {variable} among players")
    plt.xlabel('Values')
    plt.ylabel('percentage - 200')
    plt.xticks(rotation=90)
    plt.xticks(value1, playername)
    plt.subplots_adjust(bottom= 0.2)
    plt.show()

def aggregatemean(data, variable): # here i mainly reused code from above, 
    values = []                    # repurposed for finding the mean for the variable data
    for player, stats in data.items():
        for row in stats[1:]:
            if row[0] == variable:
                value = float(row[1])
                percentile = int(row[2])
                values.append((player, value, percentile))

    playername = [t[0] for t in values]
    percent = [t[2] for t in values]
    value1= [t[1] for t in values]
    
    mean_value = np.mean(value1)
    plt.hist(value1, bins=10, weights=percent)
    plt.axvline(mean_value, color='r', linestyle='dashed', linewidth=1)
    plt.title(f"Distribution of {variable} among players")
    plt.xlabel('Values')
    plt.ylabel('percentage')
    plt.xticks(rotation=90)
    plt.xticks(value1, playername)
    plt.subplots_adjust(bottom= 0.2)
    plt.show()


#here, we search up a new player, if we dont want to see a new player, we can view a histogram of the whole team based on
#one variable, and compare all players based on said variable
def searchanotherplayer():
    while True:
        checknewplayer = input("would you like to see another player, yes or no: ").lower()
        if checknewplayer == "yes":
            for playername in csvtodict.keys():
                print(playername)
            newinp = input("enter a new player: ")
            anotherplayer = (findyourplayer(csvtodict, newinp))
            print(anotherplayer)
            playergraph = plotdata(anotherplayer, newinp)
        elif checknewplayer == "no":
            while True:
                viewstat = input("would you like to view team by variable/statistic, yes or no: ")
                if viewstat == "yes":
                    variable = input("what variable would u like to see (enter 'no' to exit): ")
                    if variable == "no":
                        break
                    filterbycharacterstic(csvtodict, variable)
                    aggregatemean(csvtodict, variable)
                elif viewstat == "no":
                    print("                                ")
                    print("EXPLANATION FOR QUESTIONS AT END OF CODE")
                    print("if code ran too many times quickly (around 4) will get blocked for 1min")
                    return
                else:
                    print("Please enter yes or no.")
        else:
            checknewplayer = input("either yes or no: ").lower()


searchanotherplayer()
playergraph

        #END
#===============================================================================================================
        #ANSWER to THE Q'S


#1. Task A: Dataset and data structure (total 10 marks):

# the data set is webscraped from a website, where it as access to hundreds of teams. currently i have only six teams.
# the data is scraped into a dictionary of list of lists. this means that i can access the player data to see their individual stats
# i can also access the data as a collective.
# the data is scraped into a csv file where i take the data and use it to form my graphs


#2 Task B: Reading in your data (total 10 marks):

#I do my defensive error checking when i scrape the data from the website. this way the data is correct when it is scraped into the csv file


#3 Task C: Aggregation and subsetting (total 15 marks)

# i have multiple filter by characteristic functions where i parse through the data. 
# for example, i find data for the specific data or i find all the data for all the players pertaining to a specific variable


#Task D: Plotting (total 15 marks)

#I plot the data for the specific player and all his characteristics or i plot the data for the whole team (specific variable)
# for the specific variable i show the mean for that data
# I tried to find and plot the mean for each variable taking into account each player. 
# however, as some players dont share the same variables for the each of them and some players have error in data -->
# i could have done it but it would have taken to much time.


# Histogram and what it shows

# the data shows that specific players compared to all players in the world have better statistics. this can be used to
# make better jusdgements on players. can be used for scouting players
# the histogram also shows that players depending on their position excel on their specific variable. 
# for example, defenders will always have better defending stats than the attacking.


# why i chose this data

# cos i like football

