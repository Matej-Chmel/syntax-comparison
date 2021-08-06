from argparse import ArgumentParser
from pathlib import Path
from platform import system
from subprocess import call
from sys import exit
from typing import Callable

class AppError(Exception):
	def __init__(self, msg: str):
		super().__init__(msg)

def args():
	parser = ArgumentParser(
		prog="RUNNER",
		description="Recognizes language and runs supplied program. "
		"Cache in \"src/out\" directory is used for repeated runs.")

	parser.add_argument("path", help="Path to one of the source files.")
	parser.add_argument(
		"-r", "--rebuild", action="store_true",
		help="Force recompilation of the program. "
		"Doesn't have any effect for interpreted languages without cache.")
	res = parser.parse_args()

	return Path(res.path).absolute(), res.rebuild

def buildNeeded(caller: Path, outFile: Path, rebuild: bool):
	return (
		rebuild or
		not outFile.exists() or
		outFile.stat().st_mtime < caller.stat().st_mtime)

def callProg(args: list, **kwargs):
	return call(map(str, args), **kwargs)

def checkBuild(outFile: Path):
	if not outFile.exists():
		raise AppError(f"Compilation failed, {outFile.name} wasn't created.")

def outDirPath():
	return Path(__file__).parent / "out"

def pythonCmd():
	return "python" if system().lower().startswith("linux") else "py"

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

@run("py")
def runPython(caller: Path, *_):
	callProg([pythonCmd(), caller])

def main():
	try:
		caller, rebuild = args()
		ext = caller.suffix.replace(".", "").lower()
		out = outDirPath()

		out.mkdir(exist_ok=True)
		runners[ext](caller, out, rebuild)

	except AppError as e:
		print(e)
		exit(1)

	except KeyError as e:
		print(f"Unsupported extension: {e.args[0]}")
		exit(1)

if __name__ == "__main__":
	main()
