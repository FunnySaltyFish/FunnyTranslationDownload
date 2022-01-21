import sys
import os
import re
import requests


update_log = """v2.2.1
- 新增越南语
—— 仅部分引擎支持。插件腾讯翻译、谷歌翻译需升级至新版本
- 修复 修复Release包下自动更新无法使用问题
- 新增 插件新增配置：supportLanguages，可显式指定支持语言
- 优化 代码编辑器自动补全优化，现在内置常量将默认可被提示
—— 暂时以关键字形式提供，后续研究一下怎么改成标识符
- 限制 为避免不必要的服务器资源浪费（如某些不应该被选择的引擎参与当前翻译）限制单次可选引擎数为5个，请谅解
- 新增到一半 设置页面允许选择是否显示状态栏
—— 但重启应用后即使代码设置了也没生效
—— 这个bug暂时没修完 :(
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