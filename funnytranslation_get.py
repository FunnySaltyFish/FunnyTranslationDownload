import sys
import os
import re
import requests
from typing import Optional, Tuple

update_log = """译站桌面端首个公开版本正式发布！

v2.8.2
全新大版本来袭！
- 【重要】大模型翻译支持实时显示结果，减少等待时间
- 【重要】2024译站年度翻译报告上线
- 新增 悬浮窗支持朗读原文本
- 新增 支持查看AI点数消耗
- 新增 AI点数长按可展示购买点数+赠送点数
- 新增 应用检测更新换成了新弹窗，更符合应用样式
- 优化 提高应用流畅度，减小安装包体积
- 优化 修复收藏夹页面无法关闭的问题，优化收藏夹使用体验
- 优化 通知不展开时默认跑马灯播放
- 优化 密码输错时会给出实时提示
- 优化 移除了选择语言页面多余的Item背景
- 优化 提高AI图片后处理可用性
- 优化 长文翻译增长上下文、支持直接复制结果文本
- 修复 修复长按朗读音频跳转时，应用崩溃的问题
- 修复 点击图片选择器崩溃的问题
- 升级 Compose至1.7.0&Kotlin至1.9.23
- 其他优化和更新
"""

channel = "common"

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
        "https://api.funnysaltyfish.fun/trans/v1/app_update/add_new_version", 
        # "http://127.0.0.1:5001/trans/v1/app_update/add_new_version",
        data=data, 
        files=files
    )
    print(response.text)

if __name__ == "__main__":
    platform = "android" if input("请输入平台，1: android, 2: desktop: ").strip() != "2" else "desktop"
    app_dir = r"D:\projects\kotlin\Transtation-KMP\composeApp"
    if platform == 'android':
        app_dir += r'\common\release'
        supported_extensions = ('.apk', '.aab')
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
        add_update_version(app_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)