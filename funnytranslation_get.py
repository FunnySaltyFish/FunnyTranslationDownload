import sys
import os
import re
from subprocess import Popen, PIPE
update_log = """v2.1.0 探索版05
软件更新啦~
- 修复 软件闪退bug
- 修复 修复顶部栏黑色的问题（现在是白色的了）
- 新增 在线插件！
—— 重磅更新？
—— 插件开发文档：https://www.yuque.com/funnysaltyfish/vzmuud/bi10ru
—— 插件投稿：暂时方式为导出后与作者私信
- 配套更新 插件编辑器
—— 入口 插件管理——右上角加号——新建文件
—— 支持插件调试、保存、导出
- 应用语言部分支持英文

上个版本闪退问题是在对不住了，修了一天总算是好了
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

    with open(apkpath,"rb") as f:
        f2 = open(f"./funnytranslation_{versionName}.apk","wb+")
        f2.write(f.read())
        f2.close()
            # os.popen(f'copy {apkpath} D:\\projects\\AppProjects\\Mine\\FunnyTranslationDownload\\funnytranslation_{versionName}.apk')

    
    

if __name__ == "__main__":
    get_apk_detail("D:\\projects\\AppProjects\\Mine\\FunnyTranslation\\translate\\release\\translate-release.apk")
