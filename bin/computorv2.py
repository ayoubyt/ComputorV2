import os
import sys
sys.path.insert(0, os.path.join(sys.path[0], '..'))

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
			# try:
				res = program.eval_input(text)
				print('You entered:', res)
			# except Exception as e:
			# 	print("\033[91mError: \033[0m", e)
	print('GoodBye!')


if __name__ == '__main__':
	main()
