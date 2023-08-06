#! python3

"""this is pixiv module for comiccrawler

Ex:
	http://www.pixiv.net/member_illust.php?id=2211832

"""

import re
import json
from html import unescape
from io import BytesIO
from urllib.parse import urljoin, urlencode
from zipfile import ZipFile

from node_vm2 import eval

from ..core import Episode, grabhtml
from ..error import PauseDownloadError

domain = ["www.pixiv.net"]
name = "Pixiv"
noepfolder = True
config = {
	"cookie_PHPSESSID": "請輸入Cookie中的PHPSESSID"
}

def get_init_data(html):
	js = re.search("(var globalInitData =.+?)</script>", html, re.DOTALL).group(1)
	return eval("""
	Object.freeze = n => n;
	""" + js + """
	globalInitData;
	""")

def get_title_from_init_data(html, url):
	init_data = get_init_data(html)
	user = next(iter(init_data["preload"]["user"].values()))
	return "{} - {}".format(user["userId"], user["name"])

def get_title(html, url):
	if "globalInitData" in html:
		return get_title_from_init_data(html, url)
	return "[pixiv] " + unescape(re.search("<title>([^<]+)", html).group(1))
	
def check_login(data):
	if not data.get("userData"):
		raise PauseDownloadError("you didn't login!")
		
def check_login_html(html):
	if "pixiv.user.loggedIn = true" not in html and "login: 'yes'" not in html:
		raise PauseDownloadError("you didn't login!")
		
def get_episodes(html, url):
	if "ajax/user" in url:
		works = json.loads(html)["body"]["works"]
		s = []
		for id, data in sorted(works.items(), key=lambda i: int(i[0])):
			s.append(Episode(
				"{} - {}".format(id, data["title"]),
				"https://www.pixiv.net/member_illust.php?mode=medium&illust_id={}".format(id)
			))
		return s

	if "globalInitData" in html:
		init_data = get_init_data(html)
		check_login(init_data)
		
		id = int(next(iter(init_data["preload"]["user"])))
		
		all = grabhtml("https://www.pixiv.net/ajax/user/{}/profile/all".format(id))
		all = json.loads(all)
		
		ep_ids = [int(id) for id in list(all["body"]["illusts"]) + list(all["body"]["manga"])]
		ep_ids.sort()
		ep_ids.reverse()
		
		urls = []
		for i in range(0, len(ep_ids), 48):
			ids = ep_ids[i:i + 48]
			query = [("ids[]", str(id)) for id in ids] + [("is_manga_top", "0")]
			urls.append("https://www.pixiv.net/ajax/user/{}/profile/illusts?{}".format(
				id, urlencode(query)))
		cache[id] = iter(urls)
		return []
	
	check_login_html(html)
	s = []
	# search result?
	match = re.search('id="js-mount-point-search-result-list"data-items="([^"]+)', html)
	if match:
		data = unescape(match.group(1))
		for illust in json.loads(data):
			s.append(Episode(
				"{illustId} - {illustTitle}".format_map(illust),
				urljoin(url, "/member_illust.php?mode=medium&illust_id={illustId}".format_map(illust))
			))
			
	# single image
	if "member_illust.php?mode=medium&illust_id" in url:
		s.append(Episode("image", url))
		
	return s[::-1]
	
cache = {}

def get_nth_img(url, i):
	return re.sub(r"_p0(\.\w+)$", r"_p{}\1".format(i), url)

def get_images(html, url):
	init_data = get_init_data(html)
	check_login(init_data)
	illust_id = re.search("illust_id=(\d+)", url).group(1)
	illust = init_data["preload"]["illust"][illust_id]
	
	if illust["illustType"] != 2: # normal images
		first_img = illust["urls"]["original"]
		return [get_nth_img(first_img, i) for i in range(illust["pageCount"])]
		
	# https://www.pixiv.net/member_illust.php?mode=medium&illust_id=44298524
	ugoira_meta = "https://www.pixiv.net/ajax/illust/{}/ugoira_meta".format(illust_id)
	ugoira_meta = json.loads(grabhtml(ugoira_meta))
	cache["frames"] = ugoira_meta["body"]["frames"]
	return ugoira_meta["body"]["originalSrc"]

# def errorhandler(er, crawler):
	# http://i1.pixiv.net/img21/img/raven1109/10841650_big_p0.jpg
	# Private page?
	# if is_403(er):
		# raise SkipEpisodeError
			
def imagehandler(ext, bin):
	"""Append index info to ugoku zip"""
	if ext == ".zip":
		bin = pack_ugoira(bin, cache["frames"])
		ext = ".ugoira"
	return ext, bin
	
def pack_ugoira(bin, frames):
	with BytesIO(bin) as imbin:
		with ZipFile(imbin, "a") as zip:
			data = json.dumps({"frames": frames}, separators=(',', ':'))
			zip.writestr("animation.json", data.encode("utf-8"))
		return imbin.getvalue()

def get_next_page(html, url):
	match = re.search("href=\"([^\"]+)\" rel=\"next\"", html)
	if match:
		return urljoin(url, unescape(match.group(1)))
		
	match = re.search("ajax/user/(\d+)", url) or re.search("member_illust\.php\?id=(\d+)", url)
	if match:
		id = int(match.group(1))
		try:
			return next(cache[id])
		except StopIteration:
			del cache[id]
