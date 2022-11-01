import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic,QtNetwork
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from time import sleep
from random import randint
from bs4 import BeautifulSoup
import threading
import requests
from functools import partial
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor#,setUrlRequestInterceptor



web = None

class UI(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi('userinterface.ui',self)
		
		

		start_btn = self.findChild(QPushButton,"start_browsing")
		start_btn.clicked.connect(self.start_browse)
		proxy_btn = self.findChild(QPushButton,"proxybutton")
		proxy_btn.clicked.connect(self.load_proxy)
		self.view_counting = self.findChild(QLabel,"view_count")


		self.url = None
		self.proxylist = None
		self.views_required = None
		self.view_count = None
		self.proxy_file_path = None
		self.video_length = None
		



	def start_browse(self):

		
		self.url = self.findChild(QTextEdit,"urlbox").toPlainText()
		self.video_id = self.findChild(QTextEdit,'video_id').toPlainText()
		self.views_required = self.findChild(QTextEdit,"views_required_input").toPlainText()
		self.view_count = self.findChild(QLabel,"view_count").text()
		self.video_length = self.findChild(QTextEdit,"video_length").toPlainText()




		self.thread = Worker(self.views_required,self.proxylist,self.video_length,self.url)
		self.thread.change_value.connect(self.browse_with_proxy)
		self.thread.start()

		




	def load_proxy(self):
		filename,type_ = QFileDialog.getOpenFileName(self,"select proxy file","","Text files (*.txt)")

		if filename:

			self.proxy_file_path = filename

			with open(filename) as f:
				mylist = [line.rstrip('\n') for line in f]
				self.proxylist = mylist

				sel_list = self.findChild(QListWidget,"proxy_list")

				for proxy in self.proxylist:
					sel_list.addItem(proxy)
				

	

		
	def browse_with_proxy(self,get_proxy):

			ip = get_proxy.split(":")[0]
			port = get_proxy.split(":")[1]
			view_counts = get_proxy.split(":")[2]

			proxy = QtNetwork.QNetworkProxy()
			proxy.setType(QtNetwork.QNetworkProxy.Socks5Proxy)
			proxy.setHostName(ip)
			proxy.setPort(int(port))
			QtNetwork.QNetworkProxy.setApplicationProxy(proxy)

			def runtimer2():
				try:
					web.page().runJavaScript(js)
					QTimer.singleShot(20*1000, partial(runtimer2))
					#web.page().runJavaScript(close_concent_js)
				except:
					print("can not run javascript")

			def runtimer():
				try:
					web.page().runJavaScript(js)
					QTimer.singleShot(20*1000, partial(runtimer2))
					#web.page().runJavaScript(close_concent_js)
				except:
					print("can not run javascript")
			def clicker():
				web.page().runJavaScript(searchpage_js)

			def onLoadFinished(ok,ip,port,view_counts):
				if ok:

					web_url = web.url().toString()
					print(web_url," and proxy is ",ip," port is ",port)
					if "google.com/sorry" in web_url or "consent" in web_url:
						port_ = int(port)+1
						final_proxy = str(ip)+":"+str(port_)+":"+str(view_counts)

						return self.browse_with_proxy(final_proxy)
					
					
					#runtimer()
					QTimer.singleShot(10*1000, partial(clicker))

					QTimer.singleShot(20*1000, partial(runtimer))


			close_concent_js = '''

				setInterval(function (){document.querySelector(".tp-yt-paper-button").click()},10000)

				

			'''


			searchpage_js = """

			


			document.querySelector('a[href*="{0}"]').click()
			""".format(self.video_id)
					
					

			js = """

				
				

				setInterval(function skipad(){document.querySelector(".ytp-ad-skip-button-text").click()},3000
				)

				setInterval(function consent(){document.querySelector(".tp-yt-paper-button").click()},3000
				)

				setInterval(function (){
				let sleep = ms => new Promise(r => setTimeout(r, ms));
				let settingbtn = document.querySelector(".ytp-settings-button");
				settingbtn.click();
				sleep(500);
				let open_quality = document.getElementsByClassName("ytp-panel-menu")[0].lastChild;
				open_quality.click();
				sleep(500);

				let qualityOptions = [...document.getElementsByClassName("ytp-menuitem")];
				qualityOptions[qualityOptions.length-2].click();
				console.log("done");
				},20000)


				

				
				"""

			web = QWebEngineView()

			def cookie_filter(request):
				print(f"firstPartyUrl: {request.firstPartyUrl.toString()}, origin: {request.origin.toString()}, thirdParty? {request.thirdParty}")
				return False

			cookie_store = QWebEngineProfile.defaultProfile().cookieStore()
			#cookie_store.setCookieFilter(cookie_filter)
			#cookie_store.deleteAllCookies()
			
			web.settings().setAttribute(QWebEngineSettings.PlaybackRequiresUserGesture, False)
			#request_interceptor = NWUrlRequestInterceptor({"referrer":"facebook.com"})
			#QWebEngineProfile.defaultProfile().setUrlRequestInterceptor(request_interceptor)
			web.load(QUrl(self.url))

			
			
			web.loadFinished.connect(lambda:onLoadFinished("ok",ip,port,view_counts))

			

			

			

			

			

			

			
			box = self.findChild(QGridLayout,"browser_layout")
			while box.count():
			    item = box.takeAt(0)
			    widget = item.widget()
			    # if widget has some id attributes you need to
			    # save in a list to maintain order, you can do that here
			    # i.e.:   aList.append(widget.someId)
			    widget.deleteLater()

			box.addWidget(web)



			
			self.view_counting.setText(str(view_counts))


	def onLoadFinished(self,ok):
		pass





		


class Worker(QThread):

	def __init__(self,views_required,proxylist,video_length,video_url):
		self.views_required = views_required
		self.proxylist = proxylist
		self.video_length = video_length
		self.video_url = video_url
		super().__init__()

	change_value = pyqtSignal(str)

	def run(self):
		
		for view in range(0,int(self.views_required)):
			
			a_random_number = randint(0,len(self.proxylist)-1)
			
			get_proxy_ = self.proxylist[a_random_number]
			print(get_proxy_)

			

			self.change_value.emit(get_proxy_+":"+str(view+1))
			
			
			print("started sleeping")
			self.sleep(int(self.video_length))



			
			


		







app = QApplication(sys.argv)

ui = UI()
ui.show()

sys.exit(app.exec_())
