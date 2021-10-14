import sys
import os
import re
from subprocess import Popen, PIPE
update_log = """v2.1.0 探索版01
全新版本，欢迎体验。
功能性稍欠缺，美观度提升、动效提升。
新版本开源，地址：https://github.com/FunnySaltyFish/FunnyTranslation/,期待着您的贡献
"""
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

    os.popen(f'copy {apkpath} D:\\projects\\AppProjects\\Mine\\FunnyTranslationDownload\\funnytranslation_{versionName}.apk')

    
    

if __name__ == "__main__":
    get_apk_detail("D:\\projects\\AppProjects\\Mine\\FunnyTranslation\\translate\\release\\translate-release.apk")
