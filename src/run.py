from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from platform import system
from subprocess import call
from sys import exit
from typing import Callable, Iterable

class AppError(Exception):
	def __init__(self, msg: str):
		super().__init__(msg)

def args():
	parser = ArgumentParser(
		prog="RUNNER",
		description="Recognizes language and runs supplied program. "
		"Cache in \"src/out\" directory is used for repeated runs.")

	parser.add_argument(
		"path", help="Path to one of the source files or a folder in the "
		"snippet language tree.")
	parser.add_argument(
		"-r", "--rebuild", action="store_true",
		help="Force recompilation of the program. "
		"Doesn't have any effect for interpreted languages without cache.")
	res = parser.parse_args()

	return Path(res.path.rstrip('"')).absolute(), res.rebuild

def callProg(*args, cwd: Path = None):
	return call(map(str, args), cwd=cwd, shell=cwd is not None)

@dataclass
class RunnerArgs:
	caller: Path
	rebuild: bool

	def __call__(self):
		try:
			runners[self.langDir.name.lower()](self)
		except KeyError:
			raise AppError(f"Language \"{self.langDir.name}\" isn't supported.")

	def __post_init__(self):
		if not self.caller.exists():
			raise AppError(f"\"{self.caller}\" doesn't exist.")

		src = Path(__file__).parent
		self.cwd: Path = None
		self.outDir = src / "out"
		self.outDir.mkdir(exist_ok=True)
		self.initLangDir(src)

	def buildAndCheck(self, args: Iterable):
		self.outFile.unlink(missing_ok=True)
		self.callProg(args)

		if not self.outFile.exists():
			raise AppError(
				f"Compilation failed, {self.outFile.name} wasn't created.")

	def buildAndRun(self, buildArgs: Iterable, runArgs: Iterable):
		if self.buildNeeded():
			self.buildAndCheck(buildArgs)
		self.callProg(runArgs)

	def buildNeeded(self):
		if self.rebuild or not self.outFile.exists():
			return True

		outMtime = self.outFile.stat().st_mtime
		return any(f.stat().st_mtime > outMtime for f in self.srcFiles)

	def callProg(self, args: Iterable):
		return callProg(*args, cwd=self.cwd)

	def initCompiledLang(self, langExt: str, outExt: str):
		self.srcFiles = list(self.langDir.rglob(f"*.{langExt}"))

		try:
			self.outFile = self.outDir / f"{self.srcFiles[0].stem}.{outExt}"
		except IndexError:
			raise AppError(f"No source files in \"{self.langDir}\".")

	def initLangDir(self, src: Path):
		try:
			snippets = src / "snippets"
			relParts = self.caller.relative_to(snippets).parts
			self.langDir = snippets / Path(*relParts[:2])

			if len(relParts) < 2 or not self.langDir.is_dir():
				raise ValueError

		except ValueError:
			raise AppError(f"\"{self.caller}\" is not part of a language tree.")

	def relSrcFiles(self):
		for f in self.srcFiles:
			yield f.relative_to(self.cwd)

Runner = Callable[[RunnerArgs], None]
runners: dict[str, Runner] = {}

def run(lang: str):
	def decorator(r: Runner):
		runners[lang.lower()] = r
		return r
	return decorator

@run("c++")
def runCpp(args: RunnerArgs):
	args.initCompiledLang("cpp", "exe")
	args.buildAndRun(
		["g++", "-std=c++17", "-g", *args.srcFiles, "-o", args.outFile],
		[args.outFile])

@run("javascript")
def runJS(args: RunnerArgs):
	callProg("node", args.caller)

@run("kotlin")
def runKT(args: RunnerArgs):
	args.initCompiledLang("kt", "jar")
	args.cwd = args.langDir
	args.buildAndRun(
		["kotlinc", *args.relSrcFiles(), "-include-runtime", "-d",
		args.outFile], ["java", "-jar", args.outFile])

@run("python")
def runPy(args: RunnerArgs):
	callProg(
		"python" if system().lower().startswith("linux") else "py",
		args.caller)

def main():
	try:
		RunnerArgs(*args())()
	except AppError as e:
		print(e)
		exit(1)

if __name__ == "__main__":
	main()
