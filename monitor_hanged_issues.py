# encoding: utf-8
from utilities_dir.classes.Jira import Jira 
from utilities_dir.functions.timer import timer 
from utilities_dir.logger.setup_logger import setup_logger 	
from passwords.passwords import passwords

def main():

	logger = setup_logger('info_logger', 'logs/info_logs.log')
	jira = Jira(passwords['jira_db_replica'])

	while True:
		try:
			hanged_issues = jira.get_hanged_issues()

			if len(hanged_issues) > 0:

				logger.info(f'{hanged_issues}')
				
		except Exception as e:
			logger.critical(f'{e}')
		else:
			pass
		finally:
			timer(60 * 3)
	
	


if __name__ == '__main__':
	main()