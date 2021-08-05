from pathlib import Path
from platform import system
from subprocess import call
from sys import argv, exit
from typing import Callable

def buildNeeded(caller: Path, outFile: Path, rebuild: bool):
	return (
		rebuild or
		not outFile.exists() or
		outFile.stat().st_mtime < caller.stat().st_mtime)

def callerPath():
	try:
		return Path(argv[1]).absolute()
	except IndexError:
		raise RuntimeError("Path to program is missing.")

def callProg(args: list, **kwargs):
	return call(map(str, args), **kwargs)

def checkBuild(outFile: Path):
	if not outFile.exists():
		raise RuntimeError(
			f"Compilation failed, {outFile.name} wasn't created.")

def outDirPath():
	return Path(__file__).parent / "out"

def pythonCmd():
	return "python" if system().lower().startswith("linux") else "py"

def rebuildOpt():
	try:
		return argv[2].lower() == "true"
	except IndexError:
		return False

RunFunc = Callable[[Path, Path, bool], None]
runners: dict[str, RunFunc] = {}

def run(ext: str):
	def decorator(func: RunFunc):
		runners[ext] = func
		return func
	return decorator

@run("cpp")
def runCpp(caller: Path, out: Path, rebuild: bool):
	outFile = out / f"{caller.stem}.exe"

	if buildNeeded(caller, outFile, rebuild):
		outFile.unlink(missing_ok=True)
		srcFiles = caller.parent / "*.cpp"
		callProg(["g++", "-std=c++17", "-g", srcFiles, "-o", outFile])
		checkBuild(outFile)

	callProg([outFile])

def main():
	try:
		caller = callerPath()
		ext = caller.suffix.replace(".", "").lower()
		out = outDirPath()
		out.mkdir(exist_ok=True)
		rebuild = rebuildOpt()
		runners[ext](caller, out, rebuild)

	except KeyError as e:
		print(f"Unsupported extension: {e.args[0]}")
		exit(1)

	except RuntimeError as e:
		print(e)
		exit(1)

if __name__ == "__main__":
	main()
