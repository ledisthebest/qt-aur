import sys
import requests
import datetime

if len(sys.argv) != 2:
    sys.exit()

response = requests.get(
    "https://aur.archlinux.org/rpc/?v=5&type=search&arg=" + sys.argv[1]
)  # https://wiki.archlinux.org/title/Aurweb_RPC_interface

o = response.json()
for result in o["results"]:
    lastmodified = datetime.datetime.fromtimestamp(result["LastModified"]) # convert unix seconds to time and date

    print(
        "软件包：" , result["Name"],
        "维护者：" , result["Maintainer"],
        "简介：" , result["Description"],
        "上次更新：" , lastmodified.strftime('%x %X'),  # print date and time based on system locale
        "版本：" , result["Version"],
        "上流链接：" , result["URL"],
        sep="\n", end="\n\n"
    )

