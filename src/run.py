from pathlib import Path
from platform import system
from subprocess import call
from sys import argv, exit
from typing import Callable

def callerPath():
	try:
		return Path(argv[1]).absolute()
	except IndexError:
		raise RuntimeError("Path to program is missing.")

def callProg(args: list, **kwargs):
	return call(map(str, args), **kwargs)

def checkCompiled(exeFile: Path):
	if not exeFile.exists():
		raise RuntimeError(
			f"Compilation failed, {exeFile.name} wasn't created.")

def outDirPath():
	return Path(__file__).parent / "out"

def pythonCmd():
	return "python" if system().lower().startswith("linux") else "py"

RunFunc = Callable[[Path, Path], None]
runners: dict[str, RunFunc] = {}

def run(ext: str):
	def decorator(func: RunFunc):
		runners[ext] = func
		return func
	return decorator

@run("cpp")
def runCpp(caller: Path, out: Path):
	exeFile = out / f"{caller.stem}.exe"
	exeFile.unlink(missing_ok=True)
	srcFiles = caller.parent / "*.cpp"
	callProg(["g++", "-std=c++17", "-g", srcFiles, "-o", exeFile])
	checkCompiled(exeFile)
	callProg([exeFile])

def main():
	try:
		caller = callerPath()
		ext = caller.suffix.replace(".", "").lower()
		out = outDirPath()
		out.mkdir(exist_ok=True)
		runners[ext](caller, out)

	except KeyError as e:
		print(f"Unsupported extension: {e.args[0]}")
		exit(1)

	except RuntimeError as e:
		print(e)
		exit(1)

if __name__ == "__main__":
	main()
