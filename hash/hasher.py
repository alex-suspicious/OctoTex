import json
import hashlib

class hasher():
	jsonFile = "hash/hashes.json"
	jsonData = ""

	def __init__(self):
		f = open(self.jsonFile, "r")
		jsonData = f.read()
		f.close()

		self.jsonData = json.loads( jsonData )
			
	def hash_file( self, filename ):
		h = hashlib.sha1()

		try:
			with open(filename,'rb') as file:
				chunk = 0
				while chunk != b'':
					chunk = file.read(1024)
					h.update(chunk)
		except Exception as e:
			return 0

		return h.hexdigest()


	def getJson( self ):
		return self.jsonData

	def saveJson( self ):
		f = open(self.jsonFile, "w")
		f.write( json.dumps( self.jsonData ) )
		f.close()

	def upscaled( self, file ):
		tempJson = self.jsonData["upscaled"]
		if( file in tempJson ):
			return tempJson[file] == self.hash_file(file)
		else:
			return False

	def materialized( self, file ):
		tempJson = self.jsonData["materialized"]
		if( file in tempJson ):
			return tempJson[file] == self.hash_file(file)
		else:
			return False

	def loaded( self, file ):
		tempJson = self.jsonData["loaded"]
		if( file in tempJson ):
			return tempJson[file] == self.hash_file(file)
		else:
			return False

	def saved( self, file ):
		tempJson = self.jsonData["saved"]
		if( file in tempJson ):
			return tempJson[file] == self.hash_file(file)
		else:
			return False


	def add_upscaled( self, file ):
		self.jsonData["upscaled"][file] = self.hash_file(file)

	def add_materialized( self, file ):
		self.jsonData["materialized"][file] = self.hash_file(file)

	def add_loaded( self, file ):
		self.jsonData["loaded"][file] = self.hash_file(file)

	def add_saved( self, file ):
		self.jsonData["saved"][file] = self.hash_file(file)