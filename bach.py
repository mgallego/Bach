import sys, json, settings,time,os
sys.path.append("..")

dir_path = os.path.dirname(os.path.abspath(__file__))
series_json = open(dir_path +'/series.json')
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
    count = 0
    for url in urls:
	try:
		count = 0
		spider = Spider(url)
		print "Searching " + url
		spider.load_torrents()
	except:
		print "Error " + count
	     	if (count < 5):
			time.sleep(5)
	         	spider = Spider(url)
                 	spider.load_torrents()
		 	count = count + 1
