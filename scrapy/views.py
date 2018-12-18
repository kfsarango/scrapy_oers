# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from bs4 import BeautifulSoup  as BS #analizar documentos html
from models import *
import requests
import xmltodict

# Create your views here.

def get_soup(link):
	web = requests.get(link)
	content = web.content
	soup = BS(content,'html.parser')
	return soup

def index_view(request):
	return render(request, 'index.html')

def scrapy_tb_revolution(request):
	domain = 'http://textbookrevolution.org'
	pageObj = Pages(id=1)
	type_oerObj = TypeOer(id=1)

	url = domain+'/index.php/Book:Lists/Subjects'
	web = requests.get(url)
	content = web.content
	soup = BS(content,'html.parser')
	cont_categories = soup.find('div',{'id':'bodyContent'})
	lista_cat = cont_categories.find('ul')
	dom_lis = lista_cat.find_all('li')
	#Recorriedo las categorias
	for li in dom_lis[1:len(dom_lis)-1]:
		tag_a = li.find('a')
		cat_oerObj = CategoryOers(name=tag_a.get_text())
		#cat_oerObj = CategoryOers(id=31,name=tag_a.get_text())
		cat_oerObj.save()
		print cat_oerObj.name

		web = requests.get(domain + tag_a.get('href'))
		content = web.content
		soup = BS(content,'html.parser')
		cont_link_books = soup.find('table',{'id':'querytable1'})
		dom_tr = cont_link_books.find_all('tr')

		#cuando la tabla tiene mas resultados
		txtLast = dom_tr[len(dom_tr)-1].get_text()
		if txtLast == '  … further results':
			further_results = domain + dom_tr[len(dom_tr)-1].find('a').get('href')
			web = requests.get(further_results)
			content = web.content
			soup = BS(content,'html.parser')
			divs_dom = soup.find('div',{'id':'bodyContent'})
			divs = divs_dom.find_all('div')
			tags_as = divs[2].find_all('a')
			last_url = domain + tags_as[len(tags_as)-1].get('href')
			#obteniedo de nuevo el html
			web = requests.get(last_url)
			content = web.content
			soup = BS(content,'html.parser')
			cont_link_books = soup.find('table',{'id':'querytable0'})
			dom_tr = cont_link_books.find_all('tr')
		'''
		1683 desde TextBook revolution
		'''
		#Recorriendo la tabla que tiene los textbooks
		for tr in dom_tr[1:]:
			print dom_tr.index(tr),'/',len(dom_tr)
			link_b = tr.find('td').find('a').get('href')
			web = requests.get(domain + link_b)
			content = web.content
			soup = BS(content,'html.parser')
			dom_tables = soup.find_all('table')
			oerObj = Oer()
			print len(dom_tables)
			if len(dom_tables) == 3:
				table1 = dom_tables[0].find_all('tr')
				table2 = dom_tables[1].find_all('tr')
			else:
				table1 = dom_tables[1].find_all('tr')
				table2 = dom_tables[2].find_all('tr')

			#table2
			dom_data = table1[0].find_all('td')
			b_title = dom_data[1].get_text()
			
			dom_data = table1[1].find_all('td')
			b_author = dom_data[1].get_text()
			
			dom_data = table1[2].find_all('td')
			b_subjects = dom_data[1].get_text()
			
			dom_data = table1[3].find_all('td')
			b_keywords = dom_data[1].get_text()
			
			dom_data = table1[4].find_all('td')
			b_education_level = dom_data[1].get_text()
			
			dom_data = table1[5].find_all('td')
			b_licences = dom_data[1].get_text()
			
			dom_data = table1[6].find_all('td')
			b_description = dom_data[1].get_text()
			
			oerObj.title = b_title
			oerObj.author = b_author
			oerObj.subjects = b_subjects
			oerObj.keywords = b_keywords
			oerObj.education_level = b_education_level
			oerObj.license = b_licences
			oerObj.description = b_description
			
			#table 2
			dom_data = table2[0].find_all('td')
			try:
				b_url = dom_data[1].find('a').get('href')
			except Exception as e:
				b_url = dom_data[1].get_text()
			
			dom_data = table2[1].find_all('td')
			try:
				b_download_link = dom_data[1].find('a').get('href')
			except Exception as e:
				b_download_link = dom_data[1].get_text()
			oerObj.url = b_url
			oerObj.download_link = b_download_link
			oerObj.type_oer = type_oerObj
			oerObj.pages = pageObj
			oerObj.category_oers = cat_oerObj
			oerObj.save()
			print 'GUARDADO -> ',oerObj.title,'\n'

	return HttpResponse('Scrapy End tb_revolution')


def scrapy_tb_galileo(request):
	domain = 'https://oer.galileo.usg.edu/'
	pageObj = Pages(id=2)
	type_oerObj = TypeOer(id=1)
	cat_oerObj = CategoryOers(id=35)

	url = domain+'all-textbooks/'
	soup = get_soup(url)

	pagination_dom = soup.find('div',{'class':'adjacent-pagination'})

	dom_a = pagination_dom.find_all('a')
	for a in dom_a[2:]:
		url_page = a.get('href')
		soup = get_soup(url_page)
		lista_items = soup.find('ul',{'id':'gallery_items'})
		dom_lis = lista_items.select('> li')
		for li in dom_lis:
			url_oer = li.find('a',{'class':'cover'}).get('href')
			soup = get_soup(url_oer)
			
			cont_download = soup.find('div',{'id':'file-list'})
			full_text = cont_download.find('div',{'id':'full-text'})
			url_download = full_text.find('a').get('href')
			name_download = full_text.find('p').get_text()
			#para obtener los enlaces de descarga
			try:
				more_links = soup.find('div',{'class':'files'}).find_all('p')
			except Exception as e:
				more_links = []
				print e

			cont_abtract = soup.find('div',{'id':'abstract'})
			ps = cont_abtract.find_all('p')
			t_description = ''
			for p in ps:
				t_description = t_description + p.get_text()+'\n'
			t_title = soup.find('div',{'id':'course_title'}).find('p').get_text()
			try:
				t_number = soup.find('div',{'id':'courseno'}).find('p').get_text()
			except Exception as e:
				t_number = ''
			try:
				t_license = soup.find('div',{'id':'distribution_license'}).find_all('a')
				t_license = t_license[1].get_text()
			except Exception as e:
				t_license = ''
			try:
				t_identifier = soup.find('div',{'id':'identifier'}).find('h4')+' '+soup.find('div',{'id':'identifier'}).find('p')
			except Exception as e:
				t_identifier = ''
			try:
				t_pub_date = soup.find('div',{'id':'publication_date'}).find('p').get_text()
			except Exception as e:
				t_pub_date = ''
			try:
				t_publisher = soup.find('div',{'id':'publisher'}).find('p').get_text()
			except Exception as e:
				t_publisher = ''
			try:
				t_keywords = soup.find('div',{'id':'keywords'}).find('p').get_text()
			except Exception as e:
				t_keywords = ''
			try:
				t_subjects = soup.find('div',{'id':'bp_categories'}).find('p').get_text()
			except Exception as e:
				t_subjects = ''
			try:
				t_recommend_citactio = soup.find('div',{'id':'recommended_citation'}).find('p').get_text().replace('\n',' ')
			except Exception as e:
				t_recommend_citactio = ''

			oerObj = Oer()
			oerObj.description = t_description
			oerObj.title = t_title
			oerObj.number = t_number
			oerObj.license = t_license
			oerObj.identifier = t_identifier
			oerObj.publisher = t_publisher
			oerObj.publication_date = t_pub_date
			oerObj.keywords = t_keywords
			oerObj.subjects = t_subjects
			oerObj.recommended_citation = t_recommend_citactio
			oerObj.type_oer = type_oerObj
			oerObj.pages = pageObj
			oerObj.category_oers = cat_oerObj
			oerObj.save()
			print oerObj.title,' GUARDADO!'

			dowloadObj = Downloads()
			dowloadObj.name = name_download
			dowloadObj.url = url_download
			dowloadObj.oer = oerObj
			dowloadObj.save()
			for l in more_links:
				link_d = l.find('a').get('href')
				dowloadObj = Downloads()
				dowloadObj.name = l.get_text().replace('\n',' ')
				dowloadObj.url = link_d
				dowloadObj.oer = oerObj
				dowloadObj.save()

	return HttpResponse('ok')

def scrapy_tb_bccampus(request):
	domain = 'https://open.bccampus.ca/'
	pageObj = Pages(id=3)
	type_oerObj = TypeOer(id=1)
	cat_oerObj = CategoryOers(id=35)
	for x in xrange(10,271,10):
		print 'Page: ',x
		url = domain+'find-open-textbooks/?start='+str(x)+'&subject=&contributor=&searchTerm=&keyword='
		soup = get_soup(url)
		dom_ul = soup.find('div',{'class':'col-md-9'})
		dom_ul = dom_ul.find('ul',{'class':'no-bullets'})
		li_lst = dom_ul.find_all('li')
		for li in li_lst:
			h4 = li.find('h4')
			#recuperando los subjects
			t_subjects = ''
			try:
				subject_lst = li.find_all('h4')
				small_lst = subject_lst[1].find_all('small')
				for sm in small_lst:
					if len(small_lst)-1 == small_lst.index(sm):
						t_subjects = t_subjects + sm.find('a').get_text()
					else:
						t_subjects = t_subjects + sm.find('a').get_text() + ', '
			except Exception as e:
				print e
			strong_lst = li.find_all('strong')
			#para obtener fecha del TB
			idx_date = li.get_text().find('Date:') + 6
			t_date = li.get_text()[idx_date:idx_date+12]
			
			url_oer = domain + 'find-open-textbooks/?' + h4.find('a').get('href')
			soup = get_soup(url_oer)
			dom_data = soup.find('div',{'class':'col-md-9'})
			t_title = dom_data.find('h2').get_text()
			p_lst = dom_data.find_all('p')
			t_source = ''
			for p in p_lst[:len('p_lst')-1]:
				strong = p.find('strong').get_text()
				if strong == 'Description':
					t_description = p.find('span').get_text()
				if strong == 'Author':
					t_author = p.find('span').get_text()
				if strong == 'Original source:':
					try:
						t_source = p.find('a').get('href')
					except Exception as e:
						t_source = p.find('span').get_text()
			oerObj = Oer()
			oerObj.title = t_title
			oerObj.description = t_description
			oerObj.author = t_author
			oerObj.source = t_source
			oerObj.publication_date = t_date
			oerObj.subjects = t_subjects
			oerObj.type_oer = type_oerObj
			oerObj.pages = pageObj
			oerObj.category_oers = cat_oerObj
			oerObj.save()
			

			dowload_lst = dom_data.find('ul',{'class':'list-unstyled'})
			li_lst = dowload_lst.find_all('li')
			for li in li_lst:
				dowloadObj = Downloads()
				dowloadObj.name = li.get_text()[11:]
				dowloadObj.url = li.find('a').get('href')
				dowloadObj.oer = oerObj
				dowloadObj.save()
			print oerObj.title,' Saved!'
	return HttpResponse('ok')


def get_data_oer_commons(url_course):
	try:
		soup = get_soup(url_course)
		div_material_body = soup.find('div',{'class':'material-body'})
		material_main_data = div_material_body.find('div',{'class':'col-sm-8'})
		c_title = material_main_data.find('h1').find('a').get_text()
		c_url = material_main_data.find('a',{'id':'goto'}).get('href')
		div_rating = material_main_data.find('div',{'class':'item-rating'})
		c_rating = len(div_rating.find_all('i',{'class':'active-star'}))

		div_material_detail = soup.find('div',{'class':'material-details'})
		c_description = div_material_detail.find('dl',{'class':'materials-details-abstract'}).find('dd').get_text()

		data_first_part = div_material_detail.find('dl',{'class':'materials-details-first-part'})
		first_detail_lst = data_first_part.find_all('dt')
		first_data_lst = data_first_part.find_all('dd')
		c_subject, c_level, c_author, c_mat_type, c_provider, c_set_provider, c_date, c_grades = '','','','','','','',''
		for dt in first_detail_lst:
			tag_name = dt.get_text()
			idx = first_detail_lst.index(dt)
			data_of_tag = first_data_lst[idx].get_text().replace('\n',' ').strip()
			if tag_name == 'Subject:':
				c_subject = data_of_tag
			if tag_name == 'Level:':
				c_level = data_of_tag
			if tag_name == 'Material Type:':
				c_mat_type = data_of_tag
			if tag_name == 'Author:':
				c_author = data_of_tag
			if tag_name == 'Grades:':
				c_grades = data_of_tag
			if tag_name == 'Provider:':
				c_provider = data_of_tag
			if tag_name == 'Provider Set:':
				c_set_provider = data_of_tag
			if tag_name == 'Date Added:':
				c_date = data_of_tag
		
		data_second_part = div_material_detail.find('div',{'class':'material-details-second-part'})
		second_detail_lst = data_second_part.find_all('dt')
		second_data_lst = data_second_part.find_all('dd')
		c_license, c_language, c_media_f = '','',''
		for dt in second_detail_lst:
			tag_name = dt.get_text()
			idx = second_detail_lst.index(dt)
			data_of_tag = second_data_lst[idx].get_text().replace('\n',' ').strip()
			if tag_name == 'License:':
				c_license = data_of_tag
			if tag_name == 'Language:':
				c_language = data_of_tag
			if tag_name == 'Media Format:':
				c_media_f = data_of_tag
		#find Tags of course
		dom_tags = soup.find('section',{'class':'item-tags'})
		li_lst = dom_tags.find_all('li')
		tags_lst = []
		for li in li_lst:
			tags_lst.append(li.find('a').get_text())
		c_tags = ', '.join(tags_lst)
		
		oerObj = Oer()
		oerObj.title = c_title
		oerObj.url = c_url
		oerObj.rating = c_rating
		oerObj.description = c_description
		oerObj.subject = c_subject
		oerObj.education_level = c_level
		oerObj.author = c_author
		oerObj.material_type = c_mat_type
		oerObj.provider = c_provider
		oerObj.set_provider = c_set_provider
		oerObj.publication_date = c_date
		oerObj.license = c_license
		oerObj.language = c_language
		oerObj.media_format = c_media_f
		oerObj.tags = c_tags

		return oerObj

	except Exception as e:
		oerObj = Oer()
		oerObj.title = 'Fail'
		oerObj.url = url_course
		print e
		return oerObj

	#print c_subject,'\n', c_level,'\n', c_author,'\n', c_mat_type,'\n', c_provider,'\n', c_set_provider,'\n', c_date

def scrapy_oer_commons(request):
	domain = 'https://www.oercommons.org'
	pageObj = Pages(id=4)
	type_oerObj = TypeOer(id=2)
	soup = get_soup(domain+'/oer')
	categories_lst = soup.find('ul',{'class':'browse-group-list'}).find_all('li')
	for li in categories_lst[11:]:
		url_category = li.find('a').get('href')
		url_category = url_category[url_category.find('general_subject='):]
		spans = li.find('a').find_all('span')
		category_name = spans[0].get_text()
		print category_name
		checkCategory = CategoryOers.objects.filter(name=category_name)
		#comprobando si el material existe en la base de datos
		if len(checkCategory) == 0:
			checkCategory = CategoryOers()
			checkCategory.name = category_name
			checkCategory.save()
			print checkCategory.name,' Saved'
		else:
			checkCategory = checkCategory[0]

		nro_items = spans[1].get_text()
		nro_items = nro_items.replace('(','')
		nro_items = nro_items.replace(')','')
		number_resources = int(nro_items)

		nro_interactions = number_resources / 100
		nro_interactions = nro_interactions // 1
		resources_missing = number_resources - (nro_interactions * 100)

		#item_start = 80
		item_start = 3080
		#last id , en la anterior categoria : 8857
		for x in xrange(30,nro_interactions):
			url = domain + '/browse?batch_start='+str(item_start)+'&f.'+url_category
			soup = get_soup(url)
			div_cnt = soup.find('div',{'class':'index-items'})
			articles_lst =  div_cnt.find_all('article')
			#Recorriendo los cursos de la pagina
			for a in articles_lst:
				print articles_lst.index(a),' | page: ',item_start,' | nro IT: ',x,'/',nro_interactions
				url_src = a.find('a',{'class':'item-link'}).get('href')
				myOerObj = get_data_oer_commons(url_src)
				myOerObj.type_oer = type_oerObj
				myOerObj.pages = pageObj
				myOerObj.category_oers = checkCategory
				myOerObj.save()
				print 'OER-> ',myOerObj.title,' SAVED'

			item_start = item_start +  100
			print 'new page:', item_start

		#obteniendo los faltantes
		item_start = item_start - 80
		if resources_missing >= 20:
			item_start = item_start + (resources_missing - 15)
		url = domain + '/browse?batch_start='+str(item_start)+'&f.'+url_category
		print url
		soup = get_soup(url)
		div_cnt = soup.find('div',{'class':'index-items'})
		articles_lst =  div_cnt.find_all('article')
		nro_last_items = len(articles_lst)
		print nro_last_items
		print resources_missing
		nro_start_recolention = nro_last_items - resources_missing
		for a in articles_lst[nro_start_recolention:]:
			print articles_lst.index(a),' | pageL: ',item_start
			url_src = a.find('a',{'class':'item-link'}).get('href')
			myOerObj = get_data_oer_commons(url_src)
			myOerObj.type_oer = type_oerObj
			myOerObj.pages = pageObj
			myOerObj.category_oers = checkCategory
			myOerObj.save()
			print 'OER-> ',myOerObj.title,' SAVED'
	return HttpResponse('Listo')
