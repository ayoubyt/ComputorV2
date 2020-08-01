import re
from prompt_toolkit import PromptSession
from .expression import infix_to_rpn

prompt_session = PromptSession()

def eval_asignment(text : str):
	varName, expr = text.split("=")
	return text

def eval_expression(text : str):
	expr = text.split("=")[0]
	return str (infix_to_rpn(expr))


def eval_input(text : str):
	# remove whitespaces
	text = re.sub(r"\s+", "", text)
	res : str = ""
	if "=" in text:
		if text.count("=") > 1:
			raise NameError("just one '=' symbole must be in the expression")
		if (text[-1] == "?"):
			res = eval_expression(text)
		else:
			res = eval_asignment(text)
	return res
