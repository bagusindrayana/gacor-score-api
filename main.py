from search_engines import Bing,Google

engine = Google()
results = engine.search('Gacor site:"go.id"')
links = results.links()

print(links)