# encoding: utf-8
import psycopg2



class Jira():
	"""docstring for Jira"""
	def __init__(self, passwords):
		self.con = None
		self.cursor = None
		self.list_of_comments = None
		self.passwords = passwords


	def connect_to_db(self):
		print('Connecting')
		self.con = psycopg2.connect(database=self.passwords['database'], user=self.passwords['user'], password=self.passwords['password'], host=self.passwords['host'], port=self.passwords['port']) # 192.168.0.20
		self.cursor = self.con.cursor()



	@property
	def users(self):
		self.cursor.execute("SELECT lower_child_name FROM cwd_membership WHERE parent_name in ('support-users', '2d line', '2d line admin', '2 tech support') ")
		
		
		return [x[0] for x in self.cursor.fetchall()]


	def get_coordinating_issues(self):
		"""задачи на согласовании"""
		self.cursor.execute('''select ji.issuenum from jiraissue ji where ji.issuestatus = '10702'  ''')
		return [int( x[0] ) for x in self.cursor.fetchall() ]


	def get_last_comment_of_issue(self, issue):
		self.cursor.execute(f'''select au.lower_user_name, ji.issuenum from jiraaction j join jiraissue ji on ji.id = j.issueid join app_user au on lower(au.user_key) = lower(j.author) where ji.issuestatus = '10702' and ji.issuenum ='{issue}' order by j.created desc limit 1
			''')

		self.last_comment = self.cursor.fetchall() 
		 
		if len(self.last_comment) > 0:
			return True
		return  False


	def get_list_of_comments(self, issue):
		self.cursor.execute(f'''select au.lower_user_name, ji.issuenum from jiraaction j join jiraissue ji on ji.id = j.issueid join app_user au on lower(au.user_key) = lower(j.author) where ji.issuestatus = '10702' and ji.issuenum ='{issue}' order by j.created desc  
			''')

		self.list_of_comments = self.cursor.fetchall() 
		
		if len(self.list_of_comments) > 0:
			return True
		return  False


	def close_connection(self):
		self.con.close()
		self.cursor.close()


	@property
	def last_comments_of_issues(self):
		return [self.last_comment  for issue in  self.get_coordinating_issues() if  self.get_last_comment_of_issue(issue) ]


	@property
	def comments_of_issues(self):
		return [self.list_of_comments  for issue in  self.get_coordinating_issues() if  self.get_list_of_comments(issue) ]


	
	def get_creator_of_issue(self, issue):
		self.cursor.execute(f'''select au.lower_user_name from jiraissue ji join app_user au on au.user_key = ji.creator   where ji.issuenum = '{issue}'  ''')
		data = self.cursor.fetchall()
		 
		return data[0][0] 


	def get_coordinating_persons(self, issue):
		self.cursor.execute(f'''select au.lower_user_name from customfieldvalue c join jiraissue j on j.id = c.issue join app_user au on lower(au.user_key) = lower(c.stringvalue) where j.issuenum  = '{issue}' and c.customfield = '12806'  ''')
		data = self.cursor.fetchall()
		 
		return [x[0] for x in data]



	def get_creator_and_coordinating_persons(self, issuenum):
		creator = str(self.get_creator_of_issue(issuenum)).lower()
		coordinating_persons =  self.get_coordinating_persons(issuenum)

		return (str( creator).lower() , coordinating_persons)
		

	def check_if_issue_is_hanged(self, issue):
		
	
		issuenum = int(issue[0][1])

		

		creator, coordinating_persons = self.get_creator_and_coordinating_persons(issuenum)

		
		author = str(issue[0][0]).lower()


		if creator != author and author in coordinating_persons and author not in self.users:
			return issuenum
				

		return False


	def get_hanged_issues(self):
		
		
		try:
			self.connect_to_db()

			return [self.check_if_issue_is_hanged(issue) for issue in self.comments_of_issues if self.check_if_issue_is_hanged(issue) is not False]
		except Exception as e:
			print(e)
			return []
		else:
			pass
		finally:
			self.close_connection()
		
