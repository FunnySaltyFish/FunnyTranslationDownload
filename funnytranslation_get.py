import sys
import os
import re
import requests
from typing import Optional, Tuple

update_log = """v2.9.5
大更新，建议升级。新更新弹窗的用户建议使用“浏览器下载”来更新.
更新亮点：大模型语音翻译 | 全新引擎选择对话框 | 引擎预设 | 全新悬浮窗 | 剪切板提示 | 回弹&模糊

- 新增 语音识别翻译功能 | 欢迎尝试
  —— 基于大模型流式语音识别，支持多语言混合转录，超高准确度
  —— 实时翻译可自由搭配大模型，支持边翻译边纠错（推荐模型：混元 turbos、GLM-4.5-AirX）
  —— 开始翻译前可添加上下文、关键词，提升识别准确度
  —— 使用AI点数计费，转录每小时消耗10点，翻译按Token数计费
  —— 支持对不满意的结果重新翻译，支持对转录出的结果智能优化

- 新增 使用Compose重写悬浮窗
  —— 统一风格，支持主题切换
  —— 支持直接更改翻译引擎
  —— 支持大模型流式翻译

- 新增 剪切板内容提示功能
  —— 当剪切板有内容时在主页显示小提示条
  —— 点击可快速输入或直接翻译（可在设置中配置行为）

- 新增 预设功能
  —— 预设包含一组引擎，通过切换预设，可适应不同场景的翻译需要

- 新增 引擎选择新UI界面
  —— 全新的引擎选择对话框设计，支持筛选、搜索、排序

- 新增 注册登录页面自动填充支持
- 优化 消耗为0的费用显示为“免费”
- 优化 初次显示AI计费时会显示详细，指引新用户
- 优化 App更新弹窗支持中途停止下载，支持复制文本，修复安装唤不起来的问题
- 优化 为部分页面新增越界回弹效果
- 优化 侧滑抽屉实时模糊效果（Android 12+）
- 优化 当选择引擎数目超出限制时，提示在选择阶段就会出现
- 优化 插件编写页面，修复无法打开文件的问题
- 优化 多处UI布局和交互
  —— 改进对话框内边距和布局调整
  —— 优化图片翻译页面布局
  —— 改进AI聊天页面键盘行为

- 修复 长按悬浮球截图的崩溃问题
- 修复 深色模式下模型管理页面文本颜色显示问题
- 升级 Kotlin至2.2.0，Compose至1.8.2
---

此次更新感谢以下内测群群友的建议和反馈（排名不分先后）：
@追赶山边的风 @松川 @MUK @Moon @螃蟹胡顿254 @Forever @清影 @　 
"""

channel = "common"
# base_url = "http://127.0.0.1:5001"
base_url = "https://api.funnysaltyfish.fun"

def get_file_info(filepath: str) -> Tuple[Optional[int], Optional[str], str]:
    """
    Get version information from different file types
    Returns: (version_code, version_name, platform)
    """
    file_ext = os.path.splitext(filepath)[1].lower()
    
    if file_ext in ['.apk', '.aab']:
        # Use existing AAPT logic for Android
        output = os.popen(f"aapt d badging {filepath}").read()
        match = re.compile(r"package: name='(\S+)' versionCode='(\d+)' versionName='(.+?)'").match(output)
        if not match:
            raise Exception("can't get packageinfo")
        return int(match.group(2)), match.group(3), "android"
    
    # For other platforms, try to extract version from filename
    toml_path = r"D:\projects\kotlin\Transtation-KMP\gradle\libs.versions.toml"
    import toml
    with open(toml_path, "r") as f:
        data = toml.load(f)
    versions = data["versions"]
    version_code = versions["project-versionCode"]
    version_name = versions["project-versionName"]
    platform = "desktop"
    return version_code, version_name, platform

def add_update_version(filepath: str):
    version_code, version_name, platform = get_file_info(filepath)
    file_extension = os.path.splitext(filepath)[1][1:]  # Remove the dot
    
    print(f'Platform: {platform}')
    print(f'Version Code: {version_code}')
    print(f'Version Name: {version_name}')
    
    data = {
        "version_code": version_code,
        "version_name": version_name,
        "channel": channel,
        "update_log": update_log,
        "platform": platform,
        "file_extension": file_extension
    }
    
    files = {
        "apk": open(filepath, "rb")
    }
    
    # Save a copy locally
    with open(filepath, "rb") as f:
        output_filename = f"./funnytranslation_{version_name}_{channel}_{platform}.{file_extension}"
        with open(output_filename, "wb+") as f2:
            f2.write(f.read())
    
    response = requests.post(
        f"{base_url}/trans/v1/app_update/add_new_version", 
        data=data, 
        files=files
    )
    print(response.text)

if __name__ == "__main__":
    platform = "android" if input("请输入平台，1: android, 2: desktop: ").strip() != "2" else "desktop"
    app_dir = r"D:\projects\kotlin\Transtation\Transtation-KMP\composeApp"
    if platform == 'android':
        app_dir += r'\common\release'
        supported_extensions = ('.apk', '.aab', ".APK")
    else:
        app_dir += r'\release\main'
        supported_extensions = ('.msi', '.zip', '.dmg', '.exe')

    app_path = ""

    import os
    from pathlib import Path
    p = Path(app_dir)

    def iter_multiple_files():
        for ext in supported_extensions:
            for each in p.glob("**/*" + ext):
                yield each

    last_modify_time = 0
    for filepath in iter_multiple_files():
        mtime = os.path.getctime(filepath)
        print(filepath, mtime)
        if mtime > last_modify_time:
            last_modify_time = mtime
            app_path = filepath
            
    if not os.path.exists(app_path):
        print(f"No supported application file found in: {app_dir}")
        sys.exit(0)
        
    print(f"Found application file: {app_path}")
    input("Press Enter to continue...")
    
    try:
        # print(get_file_info(app_path))
        add_update_version(str(app_path))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)