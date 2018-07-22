# coding: utf-8
import ui
import sys
import appex
import console
import codecs
import urllib
from bs4 import BeautifulSoup
import json
import re

url = ''

def getNovelInfo():
	ncode = ''
	novelInfo = {}
	if not url:
		return ncode, novelInfo		
	else:
		html = urllib.request.urlopen(url)
		soup = BeautifulSoup(html, 'html5lib') 
		for a in soup.find_all('a'):
			if a.string =='小説情報':
				url2 = a.get('href')
		html2 = urllib.request.urlopen(url2)
		soup2 = BeautifulSoup(html2, 'html5lib')
		print(soup2)
		ncode = soup2.find('p', {'id' : 'ncode'}).string
		novelInfo['作品'] = soup.title.string
		novelInfo['URL'] = url
		div = soup2.find('div', {'id' : 'pre_info'})
		novelInfo['状況'] = div.find('span').string
		novelInfo['話数'] = re.split('[全部分]', list(div.strings)[2])[1]
		for tr in soup2.find_all('tr'):
			th = tr.find('th').string
			td = tr.find('td').text
			if th == '作者名':
				a = tr.find('a')
				if not a:
					novelInfo['作者'] = re.split('[\n]', td)[0]
				else:
					novelInfo['作者'] = a.string
					novelInfo['作者URL'] = a.get('href')
			elif th == '掲載日':
				novelInfo['初期掲載'] = td		
			elif th == '最新部分掲載日':
				novelInfo['最終更新'] = td
			elif th == '総合評価':
				novelInfo['総合評価'] = td
			elif th == '文字数':
				novelInfo['文字数'] = td
		return ncode, novelInfo

def SegCntlTap(sender):
	pass
	
def ButtonTap(sender):
	db = {}
	try:
		with codecs.open('NovelDB.json', 'r', encoding = 'utf-8') as f:
			try:
				db = json.load(f)
			except json.JSONDecodeError as e:	
				console.alert('データベースが壊れています', '', 'OK', hide_cancel_button=True)
				sender.superview.close()
				sys.exit()
	except IOError as e:
		pass
	ncode, novelInfo = getNovelInfo()
	novelInfo['状態'] = ['読中', '読了', '保留'][sender.superview['SegCntl1'].selected_index]
	novelInfo['評価'] = str(5 - sender.superview['SegCntl2'].selected_index)
	novelInfo['コメント'] = sender.superview['TextField'].text
	if not ncode:
		console.alert('"小説を読もう！"のwebページではありません！', '', 'OK', hide_cancel_button=True)
		sender.superview.close()
		sys.exit()
	db[ncode] = novelInfo
	with codecs.open('NovelDB.json', 'w', encoding = 'utf-8') as f:
		json.dump(db, f, ensure_ascii = False, indent = 4)
	console.alert('小説情報をデータベースに登録しました！', '', 'OK', hide_cancel_button=True)
	sender.superview.close()
	sys.exit()
							
if __name__ == '__main__':
	url = appex.get_text()
	v = ui.load_view()
	v.present('sheet')

