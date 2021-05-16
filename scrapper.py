import requests
import webbrowser
import bs4
import csv
import re
import os

def build_csv():
    quest_completed = []
    quest_count = 0
    link = "https://www.malayalachalachithram.com/listsongs.php?tot=147&g=1414&p="
    with open("data/dataset.csv", "w") as ifile:
        writer = csv.writer(ifile)
        csv_arr = []
        for i in range(5):
            res = requests.get(link + str(i))
            noStarchSoup = bs4.BeautifulSoup(res.text, "html.parser")
            table = noStarchSoup.findAll("table", {"class": "mdetails"})
            for rows in table:
                for row in rows:
                    row_arr = []
                    cells = row.findAll('td')
                    if(not cells):
                        continue
                    row_arr.append(cells[2].getText())
                    for a in cells[1].find_all('a', href=True):
                        row_arr.append(a.getText()[:-4])
                        row_arr.append(
                            "https://www.malayalachalachithram.com/" + a['href'])
                    csv_arr.append(row_arr)
        writer.writerows(csv_arr)
        ifile.close()

def isManglish(str):
 
    # Regex to check string is
    # alphanumeric or not.
    regex = "^(?=.*[a-zA-Z])(?=.*[0-9])[A-Za-z0-9]+$"
 
    # Compile the ReGex
    p = re.compile(regex)
 
    # If the string is empty
    # return false
    if(str == None):
        return False
 
    # Return if the string
    # matched the ReGex
    if(re.search(p, str)):
        return True
    else:
        return False


def lyrics_scrap():
    with open("data/dataset.csv", "r") as ifile:
        reader = csv.reader(ifile)
        song_num=0
        for i,csv_row in enumerate(reader):
            res = requests.get(csv_row[2])
            noStarchSoup = bs4.BeautifulSoup(res.text, "html.parser")
            table = noStarchSoup.findAll("table", {"id": "tbllyrics"})
            rows = next(iter(table))
            row = next(iter(rows))
            cells = row.findAll('td')
            lyricsless = cells[0].findAll('script')
            if(lyricsless):
                print(i,csv_row[2])
                continue
            lyrics = (cells[0].getText())
            writer = (cells[0]).findAll('em')
            if writer : lyrics = lyrics.replace(next(iter(writer)).getText(),"")
            text_file = open("data/lyrics/"+str(song_num)+".txt", "w")
            song_num+=1
            n = text_file.write(lyrics)
            text_file.close()
            


if __name__ == "__main__":
    lyrics_scrap()
