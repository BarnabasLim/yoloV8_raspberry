from datetime import datetime
import configparser
import time
import cv2
import os
from service.telegramBot import TelegramBot
from utils.utils import cat

class DataController:
	def __init__(self, telegram=False, wifibroadcast=False, debug=False ):
		self.config=configparser.ConfigParser()
		self.config.read("./yoloV8_picam/credentials/config.ini")
		
		self.report_id=datetime.now().strftime("d_%d_%m_%Y_t_%H_%M_%S")
		
		self.target_map_list={
			"vehicle":["car", "truck"],
			"person": ["person"],
			"bike":["bicycle"]
		}

		self.max_captured_stuff={}
		
		self.telegramBot=TelegramBot(
			token=self.config['Telegram']['secretToken'],
			channel_id=self.config['Telegram']['channelId']
		)
		
		self.img_path=f'captured_vehicle/{self.report_id}_{len(self.telegramBot.imgList)}.jpg'
		self.text=''

	def __del__(self):
		del self.max_captured_stuff
	
	def step(self, detected_obj, img):
		if(sum(detected_obj.values())>0):
			if(len(self.telegramBot.imgList)<5):
				img=img*255
				self.update_max_captured_stuff_obj(detected_obj)
				
				if(sum(self.max_captured_stuff.values())>0):
					self.update_text()
					self.update_img_path()
					if not cv2.imwrite(self.img_path, img):
						raise Exception("Could not write image")
					cat(self.img_path)
					if(self.telegramBot):
						self.telegramBot.addImg(img_path=self.img_path, text=self.text)
					os.remove(self.img_path)
			else:
				self.step_end()
		
	def step_end(self):
		self.telegramBot.sendImgList()
	
	def update_max_captured_stuff_obj(self, detected_obj):
		#Updates self.max_captured_stuff
		captured_stuff={}
		
		for detection in detected_obj:
			for key in self.target_map_list.keys():
				if detection in self.target_map_list[key]:
					if key in captured_stuff:
						captured_stuff[key]=captured_stuff[key]+detected_obj[detection]
					else:
						captured_stuff[key]=detected_obj[detection]
		for key in captured_stuff:
			if key in self.max_captured_stuff:
				self.max_captured_stuff[key]=max(self.max_captured_stuff[key],captured_stuff[key])
			else:
				self.max_captured_stuff[key]=captured_stuff[key]
	
	def update_text(self):
		self.text=''
		for key in self.max_captured_stuff:
			self.text=f'max {key} detected: {self.max_captured_stuff[key]}\n'
			
	def update_img_path(self):
		self.img_path=f'captured_vehicle/{self.report_id}_{len(self.telegramBot.imgList)}.jpg'
	
