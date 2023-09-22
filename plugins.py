import os

functions = {}

def load():
	print("Plugins loading...")
	plugins = os.listdir("plugins/")
	array_files = []

	env = {}
	cp = locals()

	for x in range(len(plugins)):
		temp = plugins[x]
		f = open(f"plugins/{temp}/functions.py","r")
		code = f.read()
		f.close()

		exec(code, {}, env)
		cleanEnv = {}
		env_keys = list(env.keys())

		for y in range( len(env_keys) ):
			if( env_keys[y] not in cp ):
				cleanEnv[y] = env[env_keys[y]]
				functions[ temp + "." + env_keys[y] ] = cleanEnv[y]

	print("Done!")
