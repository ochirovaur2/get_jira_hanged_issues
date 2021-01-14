import time

					
def timer(timer=4):
	while timer >= 0:

		days = timer // (60 * 60 * 24) 
		hours = (timer % (60 * 60 * 24) ) // 3600

		minutes = ( (timer % (60 * 60 * 24) ) % 3600 ) // 60

		sec =  ( (timer % (60 * 60 * 24) ) % 3600 ) % 60

		print (f"Sleep: {days}:{hours}:{minutes}:{sec}")
		time.sleep(1)
		timer = timer - 1