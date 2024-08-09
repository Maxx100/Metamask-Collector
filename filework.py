import sys
from os import path
from openpyxl import Workbook, load_workbook
from random import randint

PASSWORD = "password"

try:
	WORDS = [x.strip() for x in open("data/bip39.txt").readlines()]
	METAMASK = "data/MetaMask-Chrome.crx"
except FileNotFoundError:
	bundle_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
	WORDS = [x.strip() for x in open(path.abspath(path.join(bundle_dir, "data/bip39.txt"))).readlines()]
	METAMASK = path.abspath(path.join(bundle_dir, "data/MetaMask-Chrome.crx"))

try:
	WB = load_workbook('found.xlsx')
except FileNotFoundError:
	WB = Workbook()
WS = WB.active


def gen_phrase(length: int = 12) -> list:
	return [WORDS[randint(0, 2047)] for _ in range(length)]


def saver(wallet: dict):
	WS.append([wallet["addr"], wallet["age"], wallet["bal"], wallet["srp"]])
	WB.save("found.xlsx")
