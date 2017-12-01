''' 
Requests allow you to send HTTP/1.1 requests. 
You can add headers, form data, multipart files, and parameters 
with simple Python dictionaries, and access the response data in the same way.
'''

import requests

''' 
Beautiful Soup is a Python library for pulling data 
out of HTML and XML files. It works with your favorite parser to 
provide idiomatic ways of navigating, searching, and modifying the parse tree. 
It commonly saves programmers hours or days of work.
'''

from bs4 import BeautifulSoup

r = requests.get("http://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c = r.content

soup=BeautifulSoup(c,"html.parser")

all=soup.find_all("div",{"class":"propertyRow"})

all[0].find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")

page_nr=soup.find_all("a",{"class":"Page"})[-1].text
print(page_nr)
l=[]

base_url="http://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s="
for page in range(0,int(page_nr)*10,10):
	print(base_url+str(page)+".html.Paginate")
	r=requests.get(base_url+str(page)+".html.Paginate")
	c=r.content
	soup=BeautifulSoup(c,"html.parser")
	all=soup.find_all("div",{"class":"propertyRow"})

	for item in all:
		d={}
		d["Address"] = item.find_all("span",{"class","propAddressCollapse"})[0].text
		try:
			d["Locality"] = item.find_all("span",{"class","propAddressCollapse"})[1].text
		except:
			d["Locality"] = None
		d["Price"] = item.find("h4",{"class","propPrice"}).text.replace("\n","").replace("","")
		try:
			d["Beds"]=item.find("span",{"class","infoBed"}).find("b").text
		except:
			d["Beds"] = None
		
		try:
			d["Area"]=item.find("span",{"class","infoSqFt"}).find("b").text
		except:
			d["Area"] = None
		
		try:
			d["Full Baths"]=item.find("span",{"class","infoValueFullBath"}).find("b").text
		except:
			d["Full Baths"] = None
		
		try:
			d["Half Baths"]=item.find("span",{"class","infoValueHalfBath"}).find("b").text
		except:
			d["Half Baths"] = None
		for column_group in item.find_all("div",{"class":"columnGroup"}):
			for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
				if "Lot Size" in feature_group.text:
					d["Lot Size"] = feature_name.text
		l.append(d)

import pandas
df=pandas.DataFrame(l)
df.to_csv("Output.csv")







