#!/usr/bin/env python3

import os
import sys
sys.path.insert(0, os.path.join(sys.path[0], '..'))
import asyncio
import selectors
selector = selectors.SelectSelector()
loop = asyncio.SelectorEventLoop(selector)
asyncio.set_event_loop(loop)
import argparse

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

from computorv2.exceptions import ComputerV2Exception
from computorv2 import main as program


prompt_session = PromptSession(history=FileHistory('.ComputorV2History'))

def main():

	#parsing command line arguments
	argparser = argparse.ArgumentParser()
	argparser.add_argument("-f", "--file", help="read from file with path PATH", metavar="PATH")
	args = argparser.parse_args()

	if (args.file):
		with open(args.file, "r") as f:
			for l in f:
				try:
					program.eval_input(l)
				except ComputerV2Exception as e:
					print(e)
	else :
		while True:
			try:
				text = prompt_session.prompt('> ')
			except KeyboardInterrupt:
				continue
			except EOFError:
				break
			else:
				try:
					if (text):
						res = program.eval_input(text)
						print(res)
				except Exception as e:
					print("\033[91merror :\033[0m", e)

if __name__ == '__main__':
	main()
