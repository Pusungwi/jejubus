import urllib.request
import io
from lxml import etree

STATION_INFO_VALUE = '033_StationInfo.jsp'
SEARCH_URL = 'http://211.57.102.22/wap/mw2/031_SearchResult.jsp?'
SEARCH_VALUE = "제주" #"%BC%AD%C7%D8%BE%C6%C6%C4%C6%AE"
SEARCH_PARAM = urllib.parse.urlencode({'keyword': SEARCH_VALUE, 'page': 1}, encoding='cp949')

try:
	requestFullUrl = SEARCH_URL + SEARCH_PARAM
	recvSearchHtml = urllib.request.urlopen(requestFullUrl)
except IOError:
	print("URL address Error")
else:
	isFoundedStation = 0
	parser = etree.HTMLParser()
	recvRawHtml = recvSearchHtml.read()
	recvRawDecodedHtml = recvRawHtml.decode('cp949')
	recvParsedHtml = etree.parse(io.StringIO(recvRawDecodedHtml), parser) # result parsed tree
	#debug code
	#result = etree.tostring(recvParsedHtml.getroot(), pretty_print=True, method="html")
	#print(result)
	
	for htmlTree in recvParsedHtml.getiterator():
		for htmlValue in htmlTree.values():
			if htmlValue[0:len(STATION_INFO_VALUE)] == STATION_INFO_VALUE:
				isFoundedStation = 1
				print(htmlValue)
	
	if isFoundedStation == 0:
		print('Not Found')
