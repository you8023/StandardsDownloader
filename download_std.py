import requests
from fpdf import FPDF
from PIL import Image
from lxml import etree
import time, random, os

def get_tiltle_url(origin_url):
	# 获取文档的标题和url链接
	title = ""
	url = ""
	msg = ""
	html = etree.HTML(requests.get(origin_url).text)
	try:
		header = html.xpath("//div[@class='page-header']")
		title = header[0].xpath("//h4/text()")
		# std_id = header[0].xpath("//div/b/text()")
		url = header[0].xpath("//h4/a/@href")
		msg = header[0].xpath("//h4/span/@title")
	except Exception as e:
		msg = f"错误信息：{e}"
	title = title[0].replace("\r", "").replace("\n", "").replace("\t", "").replace(" ", "") if len(title) > 0 else ""
	# title = f"{std_id[0].replace(' ', '')}：{title}" if len(std_id) > 0 else title
	url = url[0] if len(url) > 0 else ""
	msg = msg[0] if len(msg) > 0 else ""
	return title, url, msg

def get_pictures(the_url, path):
	# 获取图片
	page_num = 0
	headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
	}
	all_num = 0
	while True:
		time.sleep(3*random.random())
		print("Downloading picture " + str(page_num))
		url = f"{the_url.replace('attachment/onlineRead', 'hbba_onlineRead_page')}/{page_num}.png"
		img_req = requests.get(url=url, headers=headers)
		if b"404 Not Found" in img_req.content:
			all_num = page_num
			print("Downloading finished, the count of all pictures is " + str(all_num))
			break;
		file_name = path + str(page_num) + ".png"
		f = open(file_name, "wb")
		f.write(img_req.content)
		f.close()
		# 将图片保存为标准png格式
		im = Image.open(file_name)
		im.save(file_name)
		page_num += 1
	return all_num

def combine_pictures_to_pdf(path, pdf_name, all_num):
	# 合并图片为pdf
	print("Start combining the pictures...")
	page_num = 0
	file_name = path + str(page_num) + ".png"
	cover = Image.open(file_name)
	width, height = cover.size
	pdf = FPDF(unit = "pt", format = [width, height])
	while all_num > page_num:
		try:
			print("combining picture " + str(page_num))
			file_name = path + str(page_num) + ".png"
			pdf.add_page()
			pdf.image(file_name, 0, 0)
			page_num += 1
		except Exception as e:
			print(e)
			break;
	pdf.output(pdf_name, "F")

def remove_pictures(path, all_num):
	# 删除原图片
	page_num = 0
	while all_num > page_num:
		try:
			print("deleting picture " + str(page_num))
			file_name = path + str(page_num) + ".png"
			os.remove(file_name)
			page_num += 1
		except Exception as e:
			print(e)
			break;

if __name__ == "__main__":
	# 文件存储的路径
	path = "E:\\test\\standards_download\\"
	base_url = "https://hbba.sacinfo.org.cn"
	# 需要的资料的网址
	origin_url = input("input the url: ")
	title, url, msg = get_tiltle_url(origin_url)
	if url == "":
		if msg == "":
			print("获取文档信息失败，请检查文档链接是否正确！")
		else:
			print(f"获取文档信息失败：{msg}")
		exit()
	
	print(f"开始下载标准《{title}》...")
	all_num = get_pictures(base_url + url, path)
	pdf_name = title + ".pdf"
	combine_pictures_to_pdf(path, pdf_name, all_num)
	remove_pictures(path, all_num)