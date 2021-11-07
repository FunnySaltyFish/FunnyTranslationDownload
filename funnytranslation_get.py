import sys
import os
import re
from subprocess import Popen, PIPE
update_log = """v2.1.0 探索版03
软件更新啦~
- 新增 鸣谢页面，感谢对本项目支持的大家
—— 暂时为离线数据，之后会改成在线的
- 调整 引擎选择默认隐藏，可手动点击展开
- 修复 底部导航栏图标大小不一致的问题
- 修复 修复强行退出程序数据不会被保存的问题
- 修复 插件默认不会被启用的问题

预告更新：
 - 在线插件导入
 - 插件编辑器
 - 繁简转换（以插件形式提供） 

我的周六周日又这么过了，嘤嘤嘤
支持项目：https://afdian.net/@funnysaltyfish?tab=home，感谢啊啊啊啊！！！
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
