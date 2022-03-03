import sys
import os
import re
import requests


update_log = """v2.2.4
- 优化 状态栏沉浸！
- 优化 优化异形屏显示效果（水滴、刘海等）
- 调整 移除设置“显示状态栏”，更改为“隐藏导航栏”
- 更新 捐赠渠道新增支付宝
- 更新 新增项目源码、第三方库列表和隐私政策页面
- 优化 应用崩溃时增加捕获页面，并可提交崩溃报告至服务器
- 优化 优化在较窄屏幕横屏时（如手机横屏）的显示效果
- 优化 其他页面小细节的调整

下次更新会优化悬浮窗 @酷友 松川吖
要耗点时间
"""
channel = "stable"

def get_apk_detail(apkpath):
    # process = Popen("aapt d badging %s" % apkpath)
    # process.stdin=PIPE
    # process.stderr=PIPE
    # output , err = process.communicate()
    output = os.popen(f"aapt d badging {apkpath}").read() #.decode(encoding='utf-8')
    print(output)
    match = re.compile(r"package: name='(\S+)' versionCode='(\d+)' versionName='(.+?)'").match(output)
    if not match:
        raise Exception("can't get packageinfo")
 
    packagename = match.group(1)
    versionCode = match.group(2)
    versionName = match.group(3)
 
    print('packagename:' + packagename)
    print('versionCode:' + versionCode)
    print('versionName:' + versionName)

    global update_log
    with open("./updateLog.txt","a+",encoding="utf-8") as f:
        f.write(f"\n{update_log}")

    update_log = update_log.replace("\n","\\n")

    json_text = f"""{{
	    "versionCode":{versionCode},
	    "versionName":"{versionName}",
	    "apkUrl":"https://www.coolapk.com/apk/254263",
	    "isUpdate":true,
	    "updateLog":"{update_log}"
    }}"""

    print(json_text)
    with open("./description.json","w+",encoding="utf-8") as f:
        f.write(json_text)

    with open(apkpath,"rb") as f:
        f2 = open(f"./funnytranslation_{versionName}.apk","wb+")
        f2.write(f.read())
        f2.close()
    

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
        f2 = open(f"./funnytranslation_{versionName}.apk","wb+")
        f2.write(f.read())
        f2.close()
    
    response = requests.post("https://api.funnysaltyfish.fun/trans/v1/app_update/add_new_version", data=data, files=files)
    print(response.text)

if __name__ == "__main__":
    add_update_version("D:\\projects\\AppProjects\\Mine\\FunnyTranslation\\translate\\release\\translate-release.apk")
    get_apk_detail("D:\\projects\\AppProjects\\Mine\\FunnyTranslation\\translate\\release\\translate-release.apk")