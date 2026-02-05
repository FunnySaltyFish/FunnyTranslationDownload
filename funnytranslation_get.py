import sys
import os
import re
import requests
from typing import Optional, Tuple

update_log = """v2.9.8
桌面端：包括从 2.8.3 到 2.9.7 的安卓端大部分更新，以及：
- 新增 桌面菜单栏与窗口导航支持
- 新增 桌面端支持图片翻译，支持拖放图片完成翻译
- 优化 输入框快捷键与焦点管理
- 优化 文本选择体验
- 优化 关闭桌面端 overscroll 效果
- 优化 右键头像刷新，而非上下滑动
- 修复 年度报告页面在桌面端崩溃

以及如下 Android 端更新内容：
- 新增 语音输入
- 新增 对话翻译支持展示思考内容
- 新增 点数查询支持展示漫画翻译计费类型
- 新增 关于页提供手机版下载入口
- 优化 播放流式音频速度（如豆包和千问）速度显著加快，点击后迅速起播
- 修复 对话翻译无法修改提示词
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
    toml_path = r"D:\projects\kotlin\Transtation\Transtation-KMP\gradle\libs.versions.toml"
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