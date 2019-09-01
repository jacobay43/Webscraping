from urllib import robotparser
from urllib.error import URLError

def get_robots_parser(robots_url):
	'''
	args:
		robots_url(str): url of website's robot.txt e.g http://www.a.com/robot.txt
	returns:
		rp (robotparser.RobotFileParser)
	'''
	rp = robotparser.RobotFileParser()
	rp.set_url(robots_url)
	rp.read()
	return rp
def bot_allowed(user_agent, robots_url, url):
	'''
	args:
		user_agent(str): str representing user_agent of bot
		robots_url(str): url of website's robot.txt e.g http://www.a.com/robot.txt
		url(str): url of website e.g http://www.a.com
	returns:
		allowed(bool): True if access is allowed based on site's robot.txt
	'''
	allowed = False
	try:
		rp = get_robots_parser(robots_url)
		allowed = rp.can_fetch(user_agent, url)
	except URLError:
		allowed = False 
	return allowed

if __name__ == '__main__':
	file = open('site_robots_txts.txt', 'r') #predefined file containing urls of several sites
	print('\t\t[Output of bot_access_check.py]')
	print(f'{"Site":>5}{"URL":>25}{"Access":>40}')
	for line in file:
		line = line.split()
		print(f'{line[0]:<17}{line[1]:<35}{" ":<10}{"Allowed" if bot_allowed("good_boy",line[1]+"/robots.txt",line[1]) else "Not Allowed"}')
	file.close()
