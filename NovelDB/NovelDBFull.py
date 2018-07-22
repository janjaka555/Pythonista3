# coding: utf-8
import ui
import appex
import console
import codecs
import urllib
from bs4 import BeautifulSoup
import json
import re

BODY_TEMPLATE = '''
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>Preview</title>
<style type="text/css">
body {
	font-family: helvetica;
	font-size: 15px;
	margin: 10px;
}
</style>
</head>
<body>{{CONTENT}}</body>
</html>
'''
TH_TEMPLATE = '<th>{{A}}</th>'
HREF_TEMPLATE = '<a href="{{A}}">{{B}}</a>'

def write_th(d):
	return  TH_TEMPLATE.replace('{{A}}', d)
	
def write_td(d, align = 0):
	text = '<td'
	if align == 1:
		text += ' align = "right"'
	text += '>' + d + '</td>'
	return text
	
def write_href(l, t):
	text = HREF_TEMPLATE.replace('{{A}}', l)
	return text.replace('{{B}}', t)
	
def write_db(db):
	table = '<table border = "1" >'
	table += '<tr>'
	table += write_th('ncode')
	table += write_th('状態')
	table += write_th('作品')
	table += write_th('状況')
	table += write_th('話数')	
	table += write_th('初期掲載')
	table += write_th('最終更新')
	table += write_th('総合評価')
	table += write_th('文字数')			
	table += write_th('作者')
	table += write_th('評価')
	table += write_th('コメント')			
	for ncode in db:
		table += '<tr>'
		table += write_th(ncode)
		ni = db[ncode]
		table += write_td(ni['状態'])
		table += write_td(write_href(ni['URL'], ni['作品']))
		table += write_td(ni['状況'])
		table += write_td(ni['話数'])		
		if '初期掲載' in ni:
			text = re.split('[年 月日時分]', ni['初期掲載'])
			table += write_td(text[0] +'/' + text[2] + '/' + text[3])
		if '最終更新' in ni:
			text = re.split('[年 月日時分]', ni['最終更新'])
			table += write_td(text[0] +'/' + text[2] + '/' + text[3])
		else:
			table += write_td('')
		text = re.split('[pt]', ni['総合評価'])	
		table += write_td(text[0], 1)
		text = re.split('[文字]', ni['文字数'])					
		table += write_td(text[0], 1)
		if '作者URL' in ni:
			table += write_td(write_href(ni['作者URL'], ni['作者']))
		else:
			table += write_td(ni['作者'])
		table += write_td(ni['評価'])
		table += write_td(ni['コメント'])
		table += '</tr>'
	table += '</table>'
	return BODY_TEMPLATE.replace('{{CONTENT}}', table)
	
if __name__ == '__main__':
	db = {}
	try:
		with codecs.open('NovelDB.json', 'r', encoding = 'utf-8') as f:
			try:
				db = json.load(f)
				html = write_db(db)
				webview = ui.WebView(name='NovelDBFull')
				webview.load_html(html)
				webview.present()
				with codecs.open('NovelDB.html', 'w', encoding = 'utf-8') as f:
					f.write(html)
			except json.JSONDecodeError as e:		
				console.alert('データベースが壊れています', '', 'OK', hide_cancel_button=True)
	except IOError as e:
		console.alert('データベースがありません', '', 'OK', hide_cancel_button=True)
