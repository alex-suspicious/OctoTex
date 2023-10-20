import json
import re


class usda:
	data = None
	parameters = ["00000",""]
	name = ""

	def __init__(self, path_text):
		if( path_text[-1] == "a" and path_text[-2] == "d" ):
			self.name = path_text.split("/")[-1].split(".")[0]
			self.extension = path_text.split("/")[-1].split(".")[1]

			f = open(path_text,"r")
			self.data = f.read()
			f.close()
		else:
			self.data = path_text


	def jsonify(self):
		print("\nJsonifying USDA...\n")
		tempData = self.data
		tempData = re.sub(r'(.*) (.*) = (.*) \(', r'"\1 \2": \3,\n"custom_\2" = (',tempData)

		tempData = tempData.replace(")","}")
		tempData = tempData.replace("(","{")
		tempData = re.sub(r'(.*) = (.*)', r'"\1": "\2",',tempData)
		tempData = re.sub(r'over "(.*)"', r'"over \1":',tempData)
		tempData = re.sub(r'def (.*) "(.*)"', r'"def \1 \2":',tempData)
		tempData = re.sub(r'(.+) (.+) {', r'"\1 \2": {',tempData)

		

		tempData = tempData.replace("\n","__NEWLINE__")
		tempData = tempData.replace("\"\"","\"")
		tempData = tempData.replace("\"{\",","{")
		tempData = tempData.replace("  ","")


		tempData = tempData.replace("__NEWLINE__","\n")
		tempData = tempData.replace(",\n}","\n}")
		tempData = tempData.replace(",\n\n}","\n\n}")
		tempData = tempData.replace("\" \": {","{")
		tempData = tempData.replace("}\n\n\"","},\n\n\"")
		tempData = tempData.replace("}\n\"","},\n\"")
		tempData = tempData.replace("\": @","\": \"@")
		tempData = tempData.replace("@,","@\",")

		tempData = tempData.replace("""#usda 1.0
{
"upAxis": "Y"
},""","")


		tempData = re.sub(r'"over (.+)":\n{\n"references": "(.+)"\n}', r'"parameters_over \1":\n{\n"references": "\2"\n},\n"over \1":',tempData)
		#tempData = tempData.replace("\"\"def","\"def")
		#tempData = tempData.replace("\":\": ","\": ")
		#tempData = tempData.replace("\"[\"","[\"")
		#tempData = tempData.replace("\"]\"","\"]")

		print( tempData )
		#tempData = tempData.replace(":\n{",": {")
		return "{" + tempData + "}"


	def usdaVar(self,block, spaces = None):
		tempBlock = ""
		keys = list(block.keys())

		for x in range( len(block) ):
			key = keys[x]
			temp = block[key]
			#print( temp )
			
			if( "{" in str(temp) ):
				if( "custom_" in str(key) ):
					tempBlock += " (" + self.usdaVar(temp, spaces+1) + "\n" + ("    "*spaces) + ")"
				elif( "parameters_" in str(key) ):
					self.parameters = [ str(key).replace("parameters_",""), "\n" + "    "*spaces + "(" + self.usdaVar(temp, spaces+1) + "\n" + ("    "*spaces) + ")" ]
					#print(self.parameters)
				elif( "outputs:out" in str(key) ):
					tempBlock += "\n" + ("    "*spaces) + key + " (" + self.usdaVar(temp, spaces+1) + "\n" + ("    "*spaces) + ")"
				else:
					addEqual = "\n" + ("    "*spaces)
					if( "customData" in str(key) ):
						addEqual = " = "
					if( "dictionary range" in str(key) ):
						addEqual = " = "

					if( "def " in str(key) ):
						key = key.split(" ")
						def_name = key.pop()
						key = " ".join(key) + " \"" + def_name + "\"" 

					if( "over " in str(key) ):
						key = key.split(" ")
						def_name = key.pop()
						key = " ".join(key) + " \"" + def_name + "\"" 

					if( self.parameters[0] in key.replace("\"","") ):
						tempBlock += "\n" + ("    "*spaces) + key + self.parameters[1] + addEqual + "{" + self.usdaVar(temp, spaces+1) + "\n" + ("    "*spaces) + "}"
					else:
						tempBlock += "\n" + ("    "*spaces) + key + addEqual + "{" + self.usdaVar(temp, spaces+1) + "\n" + ("    "*spaces) + "}"

					
			else:
				template = "\"@var\""
				if( str(temp).replace(".","").isdigit() ):
					template = "@var"
				if( "false" in str(temp) or "true" in str(temp) or "@" in str(temp) ):
					template = "@var"
				if( "</" in str(temp) and ">" in str(temp) ):
					template = "@var"

				tempBlock += "\n" + ("    "*spaces) + key + " = " + template.replace("@var", str(temp))

		return tempBlock

	def json2usda(self):
		tempData = self.data
		array = json.loads(tempData)
		#tempData = tempData[1:-1]
		#newUsda = ""

		newUsda = self.usdaVar(array, 0)
		newUsda = """#usda 1.0
(
    upAxis = "Y"
)
"""	+ newUsda

		return newUsda

	def returnJson(self):
		#return json.loads(self.jsonify())
		data = self.jsonify()
		json_object = json.loads( data )

		json_formatted_str = json.dumps(json_object, indent=2)
		return json_formatted_str