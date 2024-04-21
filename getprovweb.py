from search_engines import Bing,Google

engine = Google()
results = engine.search('intitle:"Pemerintah Provinsi" site:"go.id""')
links = results.hosts()
# remove duplicate
links = list(dict.fromkeys(links))
print(links)
# save to text
with open("provweb.txt", "w") as f:
    for link in links:
        f.write(link + "\n")
