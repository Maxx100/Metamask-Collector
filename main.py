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
		wallet = searcher()
		if "error" in wallet.keys():
			pprint(f"Metamask error: {wallet["type"]}", "RED")
			pprint(f"{wallet["error"]}", "YELLOW")
			continue
		wallet = checker(wallet)
		if "error" in wallet.keys():
			pprint(f"DeBank error: {wallet["type"]}", "RED")
			pprint(f"{wallet["error"]}", "YELLOW")
			continue
		if wallet["age"] != "None" or wallet["bal"] != "$0":
			pprint(f"{wallet["addr"]}\n{wallet["age"]}\n{wallet["bal"]}\n{wallet["srp"]}\n", "GREEN")
		else:
			print(wallet["addr"])
		saver(wallet)
