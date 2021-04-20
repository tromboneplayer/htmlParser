from datetime import datetime, date
import json
from bs4 import BeautifulSoup


def main():
    
    path = "./"
    fileName = "tmf.html"

    with open(path+fileName) as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        
    tickerList = soup.find_all("span", class_="ticker")
    print("items = ", len(tickerList))
    
    t2 = list(map(lambda symbol: symbol.text.strip(), tickerList))
    print(t2)    

    with open("output.txt", "w") as txt_file:
        for line in t2:
            txt_file.write(line + "\n")

    


if __name__ == "__main__":
    main()