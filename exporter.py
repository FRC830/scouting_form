import os

def save_data(data, path):
	with open(path, 'a') as f:
		f.write('\n'+data['comments'])
		#needs to be modified to incorporate csv files and data dictionary

