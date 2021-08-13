from argparse import ArgumentParser
from json import dump
from functools import partial
from pathlib import Path
from sys import exit
from typing import Callable, IO

class AppError(Exception):
	def __init__(self, msg: str):
		super().__init__(msg)

def addCompleteArg(parser: ArgumentParser):
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument(
		"-c", "--complete", action="store_true", help="Complete existing "
		f"folder structure. {mutExHelp('gen')}")
	group.add_argument(
		"-g", "--gen", action="store_false", help="Generate folder structure "
		f"for new snippet. {mutExHelp('complete')}")

def alnumOnly(s: str):
	res = "".join(filter(str.isalnum, s))

	if not res:
		raise AppError(f"{s} doesn't contain any alphanumeric characters.")
	return res

def args():
	parser = ArgumentParser(
		prog="GEN_TREE",
		description="Generates folder structure for new snippet or "
		"completes existing folder structure with missing languages.")

	addCompleteArg(parser)
	parser.add_argument(
		"nameOrPath",
		help="With --complete pass a path to any file or folder in the tree of "
		"a snippet to complete. With --gen pass a name for the new snippet.")
	res = parser.parse_args()

	if res.complete:
		return True, Path(res.nameOrPath.rstrip('"')).absolute()
	return False, str(res.nameOrPath)

def camelCase(split: list[str]):
	return "".join([
		fmtNotUpper(split[0], str.lower),
		*map(partial(fmtNotUpper, effect=str.title), split[1:])])

def capitalize(split: list[str]):
	return " ".join([fmtNotUpper(split[0], str.title), *split[1:]])

def fmtNotUpper(s: str, effect: Callable[[str], str]):
	return s if s.isupper() else effect(s)

def fopen(p: Path, mode: str = "w"):
	return p.open(mode, encoding="utf-8")

def genFile(d: Path, name: str, effect: Callable[[IO], None] = None):
	path = d / name

	with safeFOpen(path) as f:
		try:
			effect(f)
		except TypeError:
			pass
		f.write("\n")
	printGenSuccess(d, path.stem, True)

def genLangTree(progName: str, snipDir: Path, template: Path):
	langDir = snipDir / template.parent.name
	safeMkdir(langDir)
	ext = template.suffix.lower().replace(".", "")

	with fopen(langDir / "README.md") as f:
		f.write(mdShort(ext))
	with fopen(langDir / f"{progName}.{ext}") as f, fopen(template, "r") as t:
		f.write(t.read())
	printGenSuccess(langDir, "tree")

def genMetadata(snipDir: Path):
	genFile(
		snipDir, "metadata.json",
		lambda f: dump({"aliases": [""]}, f, indent=4, sort_keys=True))

def genSnipReadme(snipDir: Path):
	genFile(
		snipDir, "README.md",
		lambda f: f.write(f"# {snipDir.name}{NL}"))

def initSnipDirAndProgNameFromArgs():
	complete, nameOrPath = args()
	src = srcDir()

	if complete:
		snip = snipDirFromPath(nameOrPath, src)
		progName = camelCase(snip.name.split())
	else:
		snipNameSplit = nameOrPath.split()
		snip = snipDir(capitalize(snipNameSplit), src)
		progName = camelCase(snipNameSplit)
		safeMkdir(snip)
	return alnumOnly(progName), snip, src

def mdShort(ext: str):
	try:
		highlight = mdSyntaxHighlight[ext]
	except KeyError:
		highlight = ext
	return f"```{highlight}{NL * 2}```{NL}"

mdSyntaxHighlight = {
	"kt": "kotlin",
	"py": "python"}

def mutExHelp(otherArg: str):
	return f"Cannot be used with --{otherArg} argument."

NL = "\n"

def printGenSuccess(d: Path, itemName: str, quoted: bool = False):
	dirName = f"\"{d.name}\"" if quoted else d.name
	print(f"Generated {itemName} for {dirName}.")

def safeMkdir(p: Path):
	try:
		p.mkdir()

	except Exception:
		for _ in p.iterdir():
			raise AppError(
				f"\"{p.name}\" directory already exists and isn't empty.")

def safeFOpen(p: Path):
	if p.exists():
		raise AppError(
			f"{p.stem[0].upper() + p.stem[1:]} for \"{p.parent.name}\" "
			"already exists.")
	return fopen(p)

def snipDir(name: str, src: Path):
	return snippetsDir(src) / name

def snipDirFromPath(p: Path, src: Path):
	try:
		snippets = snippetsDir(src)
		return snippets / p.relative_to(snippets).parts[0]
	except ValueError:
		raise AppError(
			f"\"{p.name}\" doesn't reside inside a snippet directory.")

def snippetsDir(src: Path):
	return src / "snippets"

def srcDir():
	return Path(__file__).parent

def templateDir(src: Path):
	return src / "templates"

def templateFiles(templateDir: Path):
	return templateDir.rglob("template.*")

def tryCall(f, *args):
	try:
		f(*args)
	except AppError as e:
		print(e)

def main():
	try:
		progName, snip, src = initSnipDirAndProgNameFromArgs()
		tryCall(genFile, snip, "expOut.txt")
		tryCall(genMetadata, snip)
		tryCall(genSnipReadme, snip)

		for t in templateFiles(templateDir(src)):
			tryCall(genLangTree, progName, snip, t)

	except AppError as e:
		print(e)
		exit(1)

if __name__ == "__main__":
	main()
