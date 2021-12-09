import tweepy
import pickle
import time
import random

class TwitterBot:
	
	def __init__(self):
		self.filename = './Files/user.data'
		self.testId = 1468526465889144833

	def store_data(self,data):
		fw = open(self.filename, 'wb')
		pickle.dump(data, fw)
		fw.close()

	def read_data(self):
		try: fd = open(self.filename, 'rb')
		except FileNotFoundError:
			with open(self.filename, "w+") as fd:
				pass
		try: return pickle.load(fd)
		except: return []

	def delete_data(self, user_to_delete):
		data = self.read_data()
		names = [k['name'] for k in data]
		index = names.index(user_to_delete)
		data.pop(index)
		self.store_data(data)

	def view_user_data(self, user):
		data = self.read_data()

		names = [k['name'] for k in data]
		index = names.index(user)

		user_data = data[index]
		name = user_data['name']
		ck  = user_data['API_DATA']['consumer_key']
		cs  = user_data['API_DATA']['consumer_secret']
		at  = user_data['API_DATA']['access_token']
		ats = user_data['API_DATA']['access_token_secret']
		return [name, ck, cs, at, ats]

	def add_new_user(self, name, consumer_key, consumer_secret, access_token, access_token_secret, edit_profile):
		data = self.read_data()
		if not edit_profile:
			names = [d['name'] for d in data]
			if name in names:
				return False

		new_user = {"name": name,
					"API_DATA":{
						 'consumer_key': consumer_key, 
						 'consumer_secret': consumer_secret, 
						 'access_token': access_token, 
						 'access_token_secret': access_token_secret}}
		data.append(new_user)
		self.store_data(data)
		return True

	def get_total_user(self):
		data = self.read_data()
		return len(data)


	def check_if_valid_keys(self, ck, cs, at, ats):
		client = tweepy.Client(consumer_key= ck,consumer_secret= cs,access_token= at, access_token_secret= ats)
		try:
			client.like(self.testId)
			client.unlike(self.testId)
			return True
		except:
			return False

	def like_n_retweet(self, tweet_id, max_delay):
		data = self.read_data()
		if len(data) == 0: return False
		delay = [random.randint(0, max_delay) for d in data]
		for i in range(len(data)):
			d   = data[i]
			ck  = d['API_DATA']['consumer_key']
			cs  = d['API_DATA']['consumer_secret']
			at  = d['API_DATA']['access_token']
			ats = d['API_DATA']['access_token_secret']
			try:
				client = tweepy.Client(consumer_key= ck,consumer_secret= cs,access_token= at, access_token_secret= ats)
				client.like(tweet_id)
				client.retweet(tweet_id)
				time.sleep(delay[i])
			except:
				return False
		return True

