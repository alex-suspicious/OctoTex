#import webview
import os

import asyncio
import plugins
import functions
import plugins
from aiohttp import web

import sys
import json
import inspect
sys.path.append('nvidia')

from octahedral import *
import webbrowser


req_types = {
	"html":"text/html",
	"json":"application/javascript",
	"png":"image/*",
	"js":"application/javascript",
	"css":"text/css",
	"woff2":"application/x-font-woff2",
	"jpg":"image/*",
	"jpeg":"image/*",
	"ttf":"application/octet-stream",
	"ico":"image/x-icon",
	"hdr":"image/vnd.radiance"
}

cache_types = {
	"html":False,
	"json":False,
	"png":False,
	"js":False,
	"css":False,
	"woff2":True,
	"jpg":False,
	"jpeg":False,
	"ttf":True,
	"ico":True,
	"hdr":True
}

def callback(request):
	func_name = str(request).split("/")[2]
	func_name = func_name.replace(" >","")

	if( func_name in plugins.functions and "." in func_name ):
		func_done = plugins.functions[func_name]
	else:
		func_done = getattr(functions, func_name)

	params = request.rel_url.query
	normal_params = {}
	like_parameters = []
	for k in set(params.keys()):
	    normal_params[k] = params.getall(k)
	
	#param_keys = list( normal_params.keys() ) 

	func_params = inspect.signature(func_done);
	func_param_names = [param.name for param in func_params.parameters.values()]

	for x in range( len(func_param_names) ):
		like_parameters.append( f"normal_params[ \"{func_param_names[x]}\" ][0]" )
	
	code = """
try:
	result = func_done(""" + ",".join(like_parameters) + """)
except Exception as e:
	result = "Error: " + str(e)
	"""
	print(code)
	env = globals()
	envl = locals()
	
	exec(code, env, envl)
	result = envl['result']
	print( result )
	#print(f"\n\n\n\n{result}\n\n\n\n\n")
	#if( "texture" in params ):
	#	result = func_done( params["texture"] )
	#else:
	#	result = func_done()

	return web.Response(text=result)

def returnNormal(request):
	requestNew = str(request).replace("<Request GET ","").replace(" >","")
	if( requestNew == "/<" ):
		return

	fileName = requestNew.split("/")[-1]

	LightspeedOctahedralConverter.convert_octahedral_file_to_dx("textures/processing/normals/" + fileName, "webui/textures/temp/" + fileName)

	f = open("webui/textures/temp/" + fileName, "rb")
	file = f.read()
	f.close()

	return web.Response( body=file, content_type="image/*")

async def all_routing( request, index = False ):
	requestNew = str(request).replace("<Request GET ","").replace(" >","")
	if( requestNew == "/<" ):
		return

	if( index ):
		requestNew = "/index.html"

	fileType = requestNew.split(".")
	if( "." not in requestNew ):
		requestNew = requestNew + ".html"
		fileType = [requestNew,"html"]


	if( fileType[len(fileType)-1].split("?")[0] == "map" ):
		return

	reqType = req_types[ fileType[len(fileType)-1].split("?")[0] ]

	cache = cache_types[ fileType[len(fileType)-1].split("?")[0] ]

	if( "image" in reqType or "octet" in reqType or "woff2" in reqType ):
		try:
			f = open("webui/" + requestNew, "rb")
			file = f.read()
			f.close()
			return web.Response( body=file, content_type=reqType)
		except Exception as e:
			requestNew = requestNew.replace("upscaled","diffuse")
			f = open("webui/" + requestNew, "rb")
			file = f.read()
			f.close()
			return web.Response( body=file, content_type=reqType)


	f = open("webui/" + requestNew, "r", encoding="utf8")
	file = f.read()
	f.close()


	headers = {}
	if( cache ):
		headers.update( {'Cache-Control': "max-age=86400"} )

	response = web.Response( text=file, content_type=reqType, headers=headers)
	return response

async def index_routing( request ):
	return await all_routing(request, True)

async def processing_routing( request ):
	requestNew = str(request).replace("<Request GET ","").replace(" >","")
	if( requestNew == "/<" ):
		return

	fileType = requestNew.split(".")
	if( "." not in requestNew ):
		requestNew = requestNew + ".html"
		fileType = [requestNew,"html"]


	if( fileType[len(fileType)-1].split("?")[0] == "map" ):
		return

	reqType = req_types[ fileType[len(fileType)-1].split("?")[0] ]

	cache = cache_types[ fileType[len(fileType)-1].split("?")[0] ]

	if( "image" in reqType or "octet" in reqType or "woff2" in reqType ):
		try:
			f = open("textures/" + requestNew, "rb")
			file = f.read()
			f.close()
			return web.Response( body=file, content_type=reqType)
		except Exception as e:
			requestNew = requestNew.replace("upscaled","diffuse")
			f = open("textures/" + requestNew, "rb")
			file = f.read()
			f.close()
			return web.Response( body=file, content_type=reqType)


	f = open("textures/" + requestNew, "r", encoding="utf8")
	file = f.read()
	f.close()


	headers = {}
	if( cache ):
		headers.update( {'Cache-Control': "max-age=86400"} )

	response = web.Response( text=file, content_type=reqType, headers=headers)
	return response
	
async def plugins_routing( request ):
	pluginName = request.match_info.get('name', "error")
	f = open("plugins/" + pluginName + "/index.html", "r", encoding="utf8")
	file = f.read()
	f.close()

	response = web.Response( text=file, content_type="text/html")
	return response

def aiohttp_server():
	plugins.load()

	app = web.Application()
	app.add_routes([web.get('/callback/{key:.+}', callback)])
	app.add_routes([web.get('/processing/normal/{key:.+}', returnNormal)])

	
	app.add_routes([web.get("/processing/{key:.+}", processing_routing)])
	app.add_routes([web.get(r"/plugin/{name}", plugins_routing)])
	app.add_routes([web.get("/{key:.+}", all_routing)])
	app.router.add_get('/', index_routing)

	runner = web.AppRunner(app)
	return runner


def run_server(runner):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(runner.setup())
    print("http://localhost:27015")
    webbrowser.open('http://localhost:27015', new=2)

    site = web.TCPSite(runner, 'localhost', 27015)
    loop.run_until_complete(site.start())
    loop.run_forever()


run_server( aiohttp_server() )
