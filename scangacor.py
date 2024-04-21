import json
from search_engines import Bing,Google,Startpage,Brave,Duckduckgo,Aol,Yahoo
# read prov.txt
provinsiLinks = []
with open("prov-list.txt", "r") as f:
    for line in f:
        provinsiLinks.append(line.strip())

engine = Google()
for prov in provinsiLinks:
    print("SCAN : "+prov)
    searchResult = engine.search('gacor site:"'+prov+'"',pages=10)
    results = searchResult.results()
    
    with open("./result-scan-gacor/"+prov+".json", "w") as f:
        json.dump(results, f)

