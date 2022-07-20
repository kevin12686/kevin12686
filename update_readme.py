import pathlib
import httpx
import re
import os

root = pathlib.Path(__file__).parent.resolve()
TOKEN = os.environ.get("GH_TOKEN", "")

spotify_url = "https://gist.githubusercontent.com/kevin12686/091278d57232ae0ac0fbbc74b6a8cbbb/raw/"
early_brid_url = "https://gist.githubusercontent.com/kevin12686/e81c734140d5e860feb3aec007be3177/raw"
code_time_url = "https://gist.githubusercontent.com/kevin12686/0b22d1886d3af2e8e235b3c46e768064/raw/"
codestats_url = "https://gist.githubusercontent.com/kevin12686/98d3939c7c75faeaceec1881dc77c16d/raw/"


def replace_chunk(content, marker, chunk, inline=False):
    r = re.compile(
        rf"<!\-\- {marker} start \-\->.*<!\-\- {marker} end \-\->",
        re.DOTALL,
    )
    if not inline:
        chunk = f"\n{chunk}\n"
    chunk = f"<!-- {marker} start -->{chunk}<!-- {marker} end -->"
    return r.sub(chunk, content)


def httpx_get(url):
    return httpx.get(url)


if __name__ == "__main__":
    readme = root / "readme.md"
    readme_contents = readme.open(encoding="utf8").read()

    spotify_text = f"\n```text\n{httpx_get(spotify_url).text}\n```\n"
    readme_contents = replace_chunk(readme_contents, "spotify", spotify_text)
    
    early_brid_text = f"\n```text\n{httpx_get(early_brid_url).text}\n```\n"
    readme_contents = replace_chunk(readme_contents, "early_bird", early_brid_text)
    
    code_time_text = f"\n```text\n{httpx_get(code_time_url).text}\n```\n"
    readme_contents = replace_chunk(readme_contents, "code_time", code_time_text)

    codestats_text = f"\n```text\n{httpx_get(codestats_url).text}\n```\n"
    readme_contents = replace_chunk(readme_contents, "codestats", codestats_text)
    
    readme.open("w", encoding="utf8").write(readme_contents)
