#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess, shlex
import requests


def run(cmd):
	res = subprocess.run(
		shlex.split(cmd),
		stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
	print(res.stderr)
	print(res.stdout)
	return res

#%%

def import_pgp_key():
	run('wget https://raw.githubusercontent.com/spesmilo/electrum/master/pubkeys/ThomasV.asc')
	run('gpg --import ThomasV.asc')

def download_electrum():
	url = 'https://download.electrum.org/'
	r = requests.get(url, allow_redirects=True)
	html_text = r.text

	rows = html_text.split('<a href="')
	table = [row.split('/"') for row in rows]
	available_versions = sorted([s[0] for s in table
						  if s[0].replace('.','').isdigit()])
	last_version = available_versions[-1]

	prefix = '{}{}/'.format(url, last_version)
	binary = 'Electrum-{}.tar.gz'.format(last_version)
	signature = '{}.asc'.format(binary)

	run('wget {}{} {}{}'.format(prefix, binary, prefix, signature))
	return binary, signature


def verify(signature):
	run('gpg --verify {}'.format(signature.split('/')[-1]))
	y = input("Please check if the signature was good? (y/n)")
	return y == 'y'


def install(binary):
	y = input('Running \nsudo pip3 install {}? (y/n)'.format(binary))
	if y == 'y':
		run('pkexec pip3 install {}/{}'.format(os.getcwd(), binary))
		return True
	return False

def modify_electrum(installed_file='/usr/local/bin/electrum'):
	temp_file = os.path.join(os.getcwd(), 'run_electrum')
	with open(installed_file , 'r') as file:
		text = file.read()
		new_text = text.replace("""parser = get_parser()
	    args = parser.parse_args()""",
		"""parser = get_parser()
	    args = parser.parse_args()
	    if not args.server:
	        args.server = 'localhost:50002'
	    args.auto_connect = False
	    args.oneserver = True""")

	with open(temp_file, 'w') as file:
		file.write(new_text)


	y = input('Overwrite electrum to disable autoconnect? (y/n)')
	if y == 'y':
		run('pkexec mv {} {}'.format(temp_file, installed_file))


#%%

import_pgp_key()
binary, signature = download_electrum()
verified = verify(signature)
if verified:
	installed = install(binary)
	if installed:
		modify_electrum()

#%%

