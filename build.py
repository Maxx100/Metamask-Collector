import os

NAME = "MetamaskCollector"


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
