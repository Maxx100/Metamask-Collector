from time import strftime, localtime, time

from filework import saver
from network import Net


net = Net()
stats = {"found": 0, "time_start": time()}


def beauty_time(secs) -> str:
	secs = int(secs)
	seconds = secs % 60
	secs //= 60
	minutes = secs % 60
	secs //= 60
	hours = secs % 24
	secs //= 24
	days = secs
	if days == 0 and hours == 0 and minutes == 0:
		return f"{seconds}s"
	if days == 0 and hours == 0:
		return f"{seconds}s {minutes}m"
	if days == 0:
		return f"{seconds}s {minutes}m {hours}h"
	return f"{seconds}s {minutes}m {hours}h {days}d"


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
			wallet = net.searcher()
		except Exception as err:
			pprint(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: Searcher error: {err}", "RED")
		else:
			while "error" in wallet.keys():
				pprint(f"Metamask error: {wallet["type"]}\n{wallet["error"]}", "RED")
				wallet = net.searcher()
			wallet2 = net.checker(wallet)
			while "error" in wallet2.keys():
				pprint(f"DeBank error: {wallet2["type"]}\n{wallet2["error"]}", "RED")
				wallet2 = net.checker(wallet)
			if wallet2["age"] != "None" or wallet2["bal"] != "$0":
				pprint(f"{wallet2["addr"]}\n{wallet2["age"]}\n{wallet2["bal"]}\n{wallet2["srp"]}\n", "GREEN")
			else:
				pprint(wallet2["addr"], "YELLOW")
			saver(wallet2)
			stats["found"] += 1
			pprint(
				f"STATISTIC: \t"
				f"FOUND: \t{stats["found"]}\n\t\t\t"
				f"TIME: \t{beauty_time(time() - stats["time_start"]).replace(" ", "\n\t\t\t\t\t")}"
				f"\n\t\t\tWPM: \t{round(int(time() - stats["time_start"]) / 60 / stats["found"], 3)}",
				"YELLOW"
			)
