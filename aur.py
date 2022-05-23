import requests


response = requests.get(
    "https://aur.archlinux.org/rpc/?v=5&type=search&arg=" + "btop"
)  # https://wiki.archlinux.org/title/Aurweb_RPC_interface

o = response.json()
bundles = []

for result in o["results"]:
    items = {}
    items["Description"] = result["Description"]
    items["FirstSubmitted"] = result["FirstSubmitted"]
    items["LastModified"] = result["LastModified"]
    items["Maintainer"] = result["Maintainer"]
    items["Name"] = result["Name"]
    items["NumVotes"] = result["NumVotes"]
    items["OutOfDate"] = result["OutOfDate"]
    items["Popularity"] = result["Popularity"]
    items["URL"] = result["URL"]
    items["Version"] = result["Version"]
    bundles.append(items)
