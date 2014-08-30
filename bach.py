import sys, json, settings
sys.path.append("..")

series_json = open('series.json')
series = json.load(series_json)

def my_import(name, class_name):
    mod = __import__(name, fromlist=[class_name])
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, class_name)
    return mod

for site, urls in series.iteritems():
    class_name = settings.SPIDERS[site]
    module_nane = 'spiders.'+site+'_spider'
    Spider = my_import(module_nane, class_name)
    for url in urls:
        spider = Spider(url)
        spider.load_torrents()
