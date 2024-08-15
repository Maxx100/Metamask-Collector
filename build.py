import os

NAME = "MetamaskCollector"

COUNT = 5


def rdir(path):
	for i in os.listdir(path):
		if os.path.isfile(f"{path}/{i}"):
			os.remove(f"{path}/{i}")
		else:
			rdir(f"{path}/{i}")
	os.rmdir(path)


if os.path.exists("dist"):
	rdir("dist")
os.system(
	"pyinstaller "
	"--onefile "
	"--icon=data/metamask.ico "
	f"-n {NAME} "
	"--add-data \"data:data\" "
	"main.py"
)
if os.path.exists(f"{NAME}.spec"):
	os.remove(f"{NAME}.spec")
if os.path.exists("build"):
	rdir("build")

if COUNT > 1:
	for i in range(1, 6):
		os.mkdir(f"dist/Collector{i}")
		os.system(f"copy dist/MetamaskCollector.exe dist/Collector{i}/MetamaskCollector{i}.exe")
