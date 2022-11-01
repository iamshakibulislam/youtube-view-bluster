import pyautogui as pg
from time import sleep

how_many_window = int(input("how many windows you want to open ? "))

for window in range(0,how_many_window):


	sleep(5)
	#opening the python script by double clicking it
	soft_icon_select = pg.locateCenterOnScreen("img/bluster_soft.png",confidence=0.7)
	pg.moveTo(soft_icon_select)
	pg.click(soft_icon_select,clicks=2)
	sleep(10)

	#input in the software gui
	search_url_sel = pg.locateCenterOnScreen("img/search_url.png",confidence=0.7)
	pg.moveTo(search_url_sel)
	pg.click()

	op = open("settings.config","r")
	conf = eval(op.read())
	search_url = conf["search_url"]
	video_id = conf["video_id"]
	views_required = conf["views_required"]
	duration = conf["duration"]
	op.close()

	pg.write(search_url)

	sel_video_id = pg.locateCenterOnScreen("img/video_id.png",confidence=0.7)
	pg.moveTo(sel_video_id)
	pg.click()
	pg.write(video_id)

	sel_views_required = pg.locateCenterOnScreen("img/views_required.png",confidence=0.7)
	pg.moveTo(sel_views_required)
	pg.click()
	pg.write(views_required)

	sel_duration = pg.locateCenterOnScreen("img/video_length.png",confidence=0.7)
	pg.moveTo(sel_duration)
	pg.click()
	pg.write(duration)


	sel_proxy_button = pg.locateCenterOnScreen("img/load_proxy_button.png",confidence=0.7)
	pg.moveTo(sel_proxy_button)
	pg.click()

	sleep(2)


	sel_proxy_file = pg.locateCenterOnScreen("img/proxy_file.png",confidence=0.7)
	pg.moveTo(sel_proxy_file)
	pg.click()


	sel_proxy_load = pg.locateCenterOnScreen("img/proxy_load.png",confidence=0.7)
	pg.moveTo(sel_proxy_load)
	pg.click()

	sleep(2)


	sel_start_browsing = pg.locateCenterOnScreen("img/start_browsing.png",confidence=0.7)
	pg.moveTo(sel_start_browsing)
	pg.click()

	sleep(25)

	sel_minimize = pg.locateCenterOnScreen("img/minimize_soft.png",confidence=0.5)
	pg.moveTo(sel_minimize)
	pg.click()


	sel_minimize_t = pg.locateCenterOnScreen("img/minimize_soft.png",confidence=0.5)
	pg.moveTo(sel_minimize_t)
	pg.click()




