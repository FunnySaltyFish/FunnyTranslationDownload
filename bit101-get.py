import sys
import os
import re
import requests


update_log = """v1.1
- 修复 修复图片无法上传的问题
（虽然只是一个小问题，但是竟然折腾了我好几天，啊啊啊啊啊啊啊啊啊啊啊啊啊啊）
"""
channel = "stable"
    

def add_update_version(apkpath):
    # version_code = int(form.get("version_code", 0))
    # version_name = form.get("version_name","0.0.0")
    # channel = form.get("channel", "stable")
    # update_log = form.get("update_log", "Empty Log")
    # file = request.files["apk"]
    output = os.popen(f"aapt d badging {apkpath}").read() #.decode(encoding='utf-8')
    match = re.compile(r"package: name='(\S+)' versionCode='(\d+)' versionName='(.+?)'").match(output)
    if not match:
        raise Exception("can't get packageinfo")
 
    packagename = match.group(1)
    versionCode = match.group(2)
    versionName = match.group(3)
 
    print('packagename:' + packagename)
    print('versionCode:' + versionCode)
    print('versionName:' + versionName)

    data = {
        "version_code" : int(versionCode),
        "version_name" : versionName,
        "channel" : channel,
        "update_log" : update_log,
    }

    
    files = {
        "apk" : open(apkpath, "rb")
    }

    with open(apkpath,"rb") as f:
        f2 = open(f"./bit101_{versionName}.apk","wb+")
        f2.write(f.read())
        f2.close()
    
    response = requests.post("https://api.shen2183.cn/bit101/add_new_version", data=data, files=files)
    print(response.text)

if __name__ == "__main__":
    apk_path = r"D:\projects\AppProjects\Mine\Bit101\app\release\app-release.apk"
    add_update_version(apk_path)