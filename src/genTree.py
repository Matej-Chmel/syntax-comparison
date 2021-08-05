from json import dump
from pathlib import Path
from sys import argv, exit
from typing import Callable

def camelCase(split: list[str]):
	return "".join([
		fmtFirstWord(split[0], str.lower),
		*map(str.title, split[1:])])

def capitalize(split: list[str]):
	return " ".join([fmtFirstWord(split[0], str.title), *split[1:]])

def fmtFirstWord(s: str, effect: Callable[[str], str]):
	return s if s.isupper() else effect(s)

def fopen(p: Path, mode: str = "w"):
	return p.open(mode, encoding="utf-8")

def genLangTree(progName: str, snipDir: Path, template: Path):
	ext = template.suffix.lower().replace(".", "")
	langDir = snipDir / template.parent.name

	genMetadata(snipDir)
	langDir.mkdir()

	with fopen(langDir / "README.md") as f:
		f.write(mdShort(ext))
	with fopen(langDir / f'{progName}.{ext}') as f, fopen(template, "r") as t:
		f.write(t.read())

def genMetadata(snipDir: Path):
	with fopen(snipDir / "metadata.json") as f:
		dump({"aliases": []}, f, indent=4, sort_keys=True)
		f.write("\n")

def mdShort(ext: str):
	try:
		highlight = mdSyntaxHighlight[ext]
	except KeyError:
		highlight = ext
	return f'```{highlight}{NEWLINE * 2}```{NEWLINE}'

mdSyntaxHighlight = {
	"py": "python"
}
NEWLINE = '\n'

def safeMkdir(snipDir: Path):
	try:
		snipDir.mkdir()

	except Exception:
		for _ in snipDir.iterdir():
			raise RuntimeError(
				f"\"{snipDir.name}\" directory already exists and isn't empty.")

def snipDir(name: str, src: Path):
	return src / "snippets" / name

def snipNameArg():
	try:
		return argv[1].strip()
	except IndexError:
		raise RuntimeError("No snippet name given.")

def srcDir():
	return Path(__file__).parent

def templateDir(src: Path):
	return src / "templates"

def templateFiles(templateDir: Path):
	return templateDir.rglob("template.*")

def main():
	try:
		src = srcDir()
		snipNameSplit = snipNameArg().split()
		snip = snipDir(capitalize(snipNameSplit), src)

		safeMkdir(snip)
		progName = camelCase(snipNameSplit)

		for t in templateFiles(templateDir(src)):
			genLangTree(progName, snip, t)

	except RuntimeError as e:
		print(e)
		exit(1)

if __name__ == "__main__":
	main()
