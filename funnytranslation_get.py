import sys
import os
import re
update_log = """v2.0.0 beta-6：
◆你不一定关注的更新
—修复 修复了翻译时进度滞后的问题
—优化 代码编辑器未保存时，退出时需要二次确认
—修复 插件管理无法删除的问题
—修复 翻译时概率出现的闪退问题（部分）

另：新插件【谷歌翻译十次】
链接：https://pan.baidu.com/s/1Btm3UkINxXA1UMqh0csCQg 
提取码：ffff
"""
def get_apk_detail(apkpath):
    output = os.popen("aapt d badging %s" % apkpath).read()
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
    with open("D:\\projects\\AppProjects\\Mine\\FunnyTranslationDownload\\updateLog.txt","a+",encoding="utf-8") as f:
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
    with open("D:\\projects\\AppProjects\\Mine\\FunnyTranslationDownload\\description.json","w+",encoding="utf-8") as f:
        f.write(json_text)

    os.popen(f'copy {apkpath} D:\\projects\\AppProjects\\Mine\\FunnyTranslationDownload\\funnytranslation_{versionName}.apk')

    
    

if __name__ == "__main__":
    get_apk_detail("D:\\projects\\AppProjects\\Mine\\FunnyTranslation\\app\\release\\app-release.apk")
