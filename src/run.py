from argparse import ArgumentParser
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from platform import system
from subprocess import call, check_output
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
	parser.add_argument(
		"-t", "--test", action="store_true",
		help="Compare standard output of the program with the expected output "
		f"in {EXP_OUT} from its snippet directory.")
	res = parser.parse_args()

	return Path(res.path.rstrip('"')).absolute(), res.rebuild, res.test

def compare(
	actual: str, expected: str, lineIdx: int = None, itemName: str = None
):
	if actual == expected:
		return

	itemStr = "" if itemName is None else f" {itemName}"
	lineStr = "" if lineIdx is None else f"Line: {lineIdx+1}{NL}"

	raise AppError(
		f"""TEST FAILED
{lineStr}{"Actual:":<10}{actual}{itemStr}
{"Expected:":<10}{expected}{itemStr}
{"Repr actual:":<15}{repr(actual)}
{"Repr expected:":<15}{repr(expected)}
""")

EXP_OUT = "expOut.txt"
NL = "\n"

@dataclass
class RunnerArgs:
	caller: Path
	rebuild: bool
	test: bool

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

	def _callProg(self, args: Iterable, func: Callable):
		return func(map(str, args), cwd=self.cwd, shell=self.cwd is not None)

	def build(self, *args):
		if not self.buildNeeded():
			return

		self.outFile.unlink(missing_ok=True)
		self.callProg(args)

		if not self.outFile.exists():
			raise AppError(
				f"Compilation failed, {self.outFile.name} wasn't created.")

	def buildNeeded(self):
		if self.rebuild or not self.outFile.exists():
			return True

		outMtime = self.outFile.stat().st_mtime
		return any(f.stat().st_mtime > outMtime for f in self.srcFiles)

	def callerRelParts(self, d: Path):
		return self.caller.relative_to(d).parts

	def callProg(self, args: Iterable) -> int:
		return self._callProg(args, call)

	def checkOutput(self, args: Iterable) -> str:
		return self._callProg(args, check_output).decode("utf-8").replace(
			"\r", "").rstrip("\n")

	@cached_property
	def implDir(self):
		try:
			nextDir = self.langDir / Path(self.callerRelParts(self.langDir)[0])

			if nextDir.is_dir():
				return nextDir
		except IndexError:
			pass
		return self.langDirIfSingleImpl()

	def initCompiledLang(self, langExt: str, outExt: str):
		self.srcFiles = list(self.implDir.rglob(f"*.{langExt}"))

		try:
			self.outFile = self.outDir / f"{self.srcFiles[0].stem}.{outExt}"
		except IndexError:
			raise AppError(f"No source files in \"{self.implDir}\".")

	def initLangDir(self, src: Path):
		try:
			snippets = src / "snippets"
			relParts = self.callerRelParts(snippets)
			self.langDir = snippets / Path(*relParts[:2])

			if len(relParts) < 2 or not self.langDir.is_dir():
				raise ValueError

		except ValueError:
			raise AppError(f"\"{self.caller}\" is not part of a language tree.")

	def langDirIfSingleImpl(self):
		try:
			next(d for d in self.langDir.iterdir() if d.is_dir())
			raise AppError(
				f"Multiple implementations exist for {self.langDir.name} "
				"but none was chosen.")
		except StopIteration:
			return self.langDir

	def mainFile(self, ext: str):
		if self.caller.suffix.replace(".", "") == ext:
			return self.caller

		try:
			return next(self.implDir.glob(f"*.{ext}"))
		except StopIteration:
			raise AppError(
				f"No file with extension \"{ext}\" in \"{self.implDir}\".")

	def relSrcFiles(self):
		return (f.relative_to(self.cwd) for f in self.srcFiles)

	def run(self, *args):
		if self.test:
			expOut = self.langDir.parent / EXP_OUT

			if not expOut.exists():
				raise AppError(
					f"{EXP_OUT} for \"{self.langDir.parent}\" doesn't exist.")
			self.runTest(args, expOut)
		else:
			self.callProg(args)

	def runTest(self, args: Iterable, expOut: Path):
		with expOut.open("r", encoding="utf-8") as f:
			actualLines = self.checkOutput(args).split("\n")
			expectedLines = f.readlines()

			for i, (actual, expected) in enumerate(zip(
				actualLines, expectedLines)
			):
				compare(actual, expected.rstrip("\n"), i)

			compare(len(actualLines), len(expectedLines), itemName="lines")
			print("TEST PASSED")

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
	args.build("g++", "-std=c++17", "-g", *args.srcFiles, "-o", args.outFile)
	args.run(args.outFile)

@run("javascript")
def runJS(args: RunnerArgs):
	args.run("node", args.mainFile("js"))

@run("kotlin")
def runKT(args: RunnerArgs):
	args.initCompiledLang("kt", "jar")
	args.cwd = args.implDir
	args.build(
		"kotlinc", *args.relSrcFiles(), "-include-runtime", "-d", args.outFile)
	args.run("java", "-jar", args.outFile)

@run("python")
def runPy(args: RunnerArgs):
	args.run(
		"python" if system().lower().startswith("linux") else "py",
		args.mainFile("py"))

def main():
	try:
		RunnerArgs(*args())()
	except AppError as e:
		print(e)
		exit(1)

if __name__ == "__main__":
	main()
