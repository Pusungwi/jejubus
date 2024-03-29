#!/usr/bin/env python 

#Title : jejubus
#Version : 0.1
#Author : Yi 'Pusungwi' Yeon Jae
#Description : a getting data from jeju bus information script
#License : read LICENSES

import urllib.request
import urllib.parse
import io
from lxml import etree

SYSTEM_ROOT_URL = 'http://211.57.102.22/wap/mw2/'
STATION_LOCATION_URL = '032_StationLocation.jsp' #HTML 소스 값에서 스테이션 정보가 하나씩 나오는건 이 JSP 이름임. 이 이름이 들어간 내용의 소스를 찾아 긁어온다.
ARRIVAL_INFO_URL = '035_ArrivalList.jsp'
SEARCH_URL = '031_SearchResult.jsp'

def search_station_by_name_with_page(station_str, page_num):
	SEARCH_PARAM = urllib.parse.urlencode({'keyword': station_str, 'page': page_num}, encoding='cp949')
	resultDictsList = []
	
	try:
		requestFullUrl = SYSTEM_ROOT_URL + SEARCH_URL + '?' + SEARCH_PARAM
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
				if htmlValue[0:len(STATION_LOCATION_URL)] == STATION_LOCATION_URL:
					isFoundedStation = 1
					rawParsedClass = urllib.parse.urlparse(htmlValue)
					parsedHtmlQueryDict = urllib.parse.parse_qs(rawParsedClass.query) 
					resultDictsList.append(parsedHtmlQueryDict)
					#print(parsedHtmlQueryDict)

		#if isFoundedStation == 0:
		#	print('Not Found')
		#else:	
		#	get arrival list
		#	arrivalInfoUrl = SYSTEM_ROOT_URL + ARRIVAL_INFO_URL + '?stid=' + resultDictsList + '&ndID=' + resultDictsList + '&bit=0' U.C
		#	print(resultDictsList)		

	#결과 개수가 한개면 stID와 ndID를 기초로 바로 결과 띄워주게 함.
	# 리턴되는 딕셔너리 값 예제 : [{'keyword': ['제주시외버스터미널'], 'page': ['1'], 'stID': ['405000991'], 'stName': ['제주시외버스터미널'], 'stX': ['15480690'], 'stY': ['47004'], 'ndID': ['4050119000']}]		
	for stationDict in resultDictsList:
		targetStID = stationDict['stID'][0]
		targetNdID = stationDict['ndID'][0]

		print("--------------------------------------------------------")
		print("결과값의 도착정보를 가져옵니다. target : " + stationDict['stName'][0])
		print("stID : " + targetStID + " ndID : " + targetNdID)
		get_arrival_information_from_id(targetStID, targetNdID)

	return resultDictsList

def search_station_by_name(station_str):
	page_num = 0
	resultStationsList = []
		
	while True:
		page_num = page_num + 1
		print("내용 검색 중...")
		print(page_num)
		pageDictsList = search_station_by_name_with_page(station_str, page_num)
		if pageDictsList == []:
			break
		else:
			for stationList in pageDictsList:
				resultStationsList.append(stationList)
	
	print(resultStationsList)
	return resultStationsList
	
def get_arrival_information_from_id(stID, ndID):
	try:
		arrivalInfoUrl = SYSTEM_ROOT_URL + ARRIVAL_INFO_URL + '?stID=' + str(stID) + '&ndID=' + str(ndID) + '&bit=0'
		print("arrival info url : " + arrivalInfoUrl)
		recvInfoHtml = urllib.request.urlopen(arrivalInfoUrl)
	except IOError:
		print("URL address error - arrival info")
	else:
		resultList = []
		parser = etree.HTMLParser()
		recvRawHtml = recvInfoHtml.read()
		recvRawDecodedHtml = recvRawHtml.decode('cp949')
		recvParsedHtml = etree.parse(io.StringIO(recvRawDecodedHtml), parser) # result parsed tree
		
		for htmlTree in recvParsedHtml.getiterator("table"):
			for subHtmlTree in htmlTree.iter('div'): # div에 도착정보가 다 있어서 수정을 하게 됨.
				encodedText = subHtmlTree.text.encode('cp949', 'ignore')
				resultByte = encodedText.decode('cp949')
				resultList.append(str(resultByte))

		print(resultList)
			
if __name__ == "__main__":
	#search_station_by_name("제주시청")
	get_arrival_information_from_id(405000725,4050099200) # 제주시외버스터미널 코드
