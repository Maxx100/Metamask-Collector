from time import strftime, localtime

from filework import saver
from network import checker, searcher


def pprint(text: str, color="WHITE"):
	if color == "GREEN":
		print("\033[92m", end="")
	elif color == "RED":
		print("\033[91m", end="")
	elif color == "YELLOW":
		print("\033[93m", end="")
	print(text, end="\033[0m\n")


if __name__ == "__main__":
	while True:
		try:
			wallet = searcher()
		except Exception as err:
			pprint(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: Searcher error: {err}", "RED")
		else:
			while "error" in wallet.keys():
				pprint(f"Metamask error: {wallet["type"]}\n{wallet["error"]}", "RED")
				wallet = searcher()
			wallet2 = checker(wallet)
			while "error" in wallet2.keys():
				pprint(f"DeBank error: {wallet2["type"]}\n{wallet2["error"]}", "RED")
				wallet2 = checker(wallet)
			if wallet2["age"] != "None" or wallet2["bal"] != "$0":
				pprint(f"{wallet2["addr"]}\n{wallet2["age"]}\n{wallet2["bal"]}\n{wallet2["srp"]}\n", "GREEN")
			else:
				pprint(wallet2["addr"], "YELLOW")
			saver(wallet2)
