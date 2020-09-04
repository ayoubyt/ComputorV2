import os
import sys
sys.path.insert(0, os.path.join(sys.path[0], '..'))

import asyncio
import selectors
selector = selectors.SelectSelector()
loop = asyncio.SelectorEventLoop(selector)
asyncio.set_event_loop(loop)

from computorv2.exceptions import ComputerV2Exception
from computorv2 import main as program

def main():
	while True:
		try:
			text = program.prompt_session.prompt('> ')
		except KeyboardInterrupt:
			continue
		except EOFError:
			break
		else:
			try:
				if (text):
					res = program.eval_input(text)
					print(res)
			except ComputerV2Exception as e:
				print(e)
	print('GoodBye!')


if __name__ == '__main__':
	main()
