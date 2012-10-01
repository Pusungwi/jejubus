import urllib.request
import urllib.parse
import io
from lxml import etree

SYSTEM_ROOT_URL = 'http://211.57.102.22/wap/mw2/'
ARRIVAL_INFO_URL = '035_ArrivalList.jsp'
SEARCH_URL = '031_SearchResult.jsp'

def search_station_by_name(station_str):
	station_str = "제주" #"%BC%AD%C7%D8%BE%C6%C6%C4%C6%AE" 임시용으로 지정
	SEARCH_PARAM = urllib.parse.urlencode({'keyword': station_str, 'page': 1}, encoding='cp949')
	try:
		requestFullUrl = SYSTEM_ROOT_URL + SEARCH_URL + '?' + SEARCH_PARAM
		recvSearchHtml = urllib.request.urlopen(requestFullUrl)
	except IOError:
		print("URL address Error")
	else:
		resultLists = []
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
				if htmlValue[0:len(STATION_INFO_URL)] == STATION_INFO_URL:
					isFoundedStation = 1
					rawParsedClass = urllib.parse.urlparse(htmlValue)
					parsedHtmlQueryDict = urllib.parse.parse_qs(rawParsedClass.query) 
					resultLists.append(parsedHtmlQueryDict)
					#print(parsedHtmlQueryDict)
	
	
		if isFoundedStation == 0:
			print('Not Found')
		else:	
			#get arrival list
			#arrivalInfoUrl = SYSTEM_ROOT_URL + ARRIVAL_INFO_URL + '?stid=' + resultLists + '&ndID=' + resultLists + '&bit=0' U.C
			print(resultLists)