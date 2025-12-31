import subprocess
import os
import time
from DrissionPage import ChromiumPage, ChromiumOptions

def start_chrome_with_extension():
    """启动Chrome并直接打开扩展页面"""
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = r"D:\Users\ChromeAutomationProfile"
    target_extension_id = "jejejajkcbhejfiocemmddgbkdlhhngm"
    extension_url = f"chrome-extension://{target_extension_id}/options.html"
    
    if not os.path.exists(chrome_path):
        print(f"❌ 未找到Chrome浏览器：{chrome_path}")
        return False
    
    # 检查用户数据目录是否存在，不存在则创建
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
        print(f"✅ 创建用户数据目录：{user_data_dir}")
    
    command = [
        chrome_path,
        "--remote-debugging-port=9223",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",             # ✅ 关键：禁止首运行欢迎页
        "--no-default-browser-check", # ✅ 关键：禁止询问是否设为默认浏览器
        extension_url
    ]
    
    print(f"🚀 正在启动Chrome远程调试...")
    print(f"命令：{' '.join(command)}")
    
    try:
        # 启动Chrome进程，不等待其结束
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Chrome已启动，直接打开插件页：{extension_url}")
        print(f"✅ 远程调试端口：9223")
        print(f"✅ 用户数据目录：{user_data_dir}")
        return True
    except Exception as e:
        print(f"❌ 启动Chrome失败：{e}")
        return False

def connect_to_extension(folder_name):
    """连接到已打开的Chrome扩展页面
    
    Args:
        folder_name: 发布文件夹名称，用于动态生成文件路径
    """
    # 1. 配置连接到 9223 端口
    co = ChromiumOptions()
    co.set_local_port(9223) # 指定连接端口为 9223
    
    # 2. 初始化页面对象
    page = ChromiumPage(addr_or_opts=co)
    
    # 3. 定义目标插件信息
    target_extension_id = "jejejajkcbhejfiocemmddgbkdlhhngm"
    target_url_fragment = f"chrome-extension://{target_extension_id}"
    
    # 4. 查找插件页
    target_tab = None
    tabs = page.get_tabs()
    
    for tab in tabs:
        if target_url_fragment in tab.url:
            target_tab = tab
            print(f"✅ 在 9223 端口浏览器中找到插件页: {tab.title}")
            page.activate_tab(tab.tab_id)
            break
    
    # 5. 执行上传操作
    if target_tab:
        print("开始操作...")
        
        # 构建相对路径，查找运行的data文件夹
        script_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        base_path = os.path.join(script_dir, 'data', 'publish', folder_name)
        
        # 动态获取文件路径
        content_file = f"{base_path}/1.txt"
        
        # 查找视频文件（支持 .MOV 和 .mov 后缀）
        video_file = None
        for file in os.listdir(base_path):
            if file.endswith('.MOV') or file.endswith('.mov'):
                video_file = f"{base_path}/{file}"
                break
        
        # 如果没有找到视频文件，返回错误
        if not video_file:
            print(f"❌ 未找到视频文件，请检查 {base_path} 目录")
            return False
        
        # 封面图片路径
        cover_file = f"{base_path}/1.jpg"
        
        # 检查文件是否存在
        if not os.path.exists(content_file):
            print(f"❌ 未找到内容文件：{content_file}")
            return False
        
        if not os.path.exists(cover_file):
            print(f"❌ 未找到封面文件：{cover_file}")
            return False
        
        print(f"📁 使用文件夹：{folder_name}")
        print(f"📄 内容文件：{content_file}")
        print(f"🎬 视频文件：{video_file}")
        print(f"🖼️ 封面文件：{cover_file}")
        
        # 解析content.txt获取标题和描述
        title = ""
        desc = ""
        with open(content_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('title:'):
                    title = line[6:].strip()
                elif line.startswith('desc:'):
                    desc = line[5:].strip()
        
        print(f"📝 读取到内容：标题='{title}', 描述='{desc}'")
        
        # 填写视频标题
        print("📝 填写视频标题...")
        title_input = page.ele('css:input[placeholder="输入视频标题"]')
        title_input.input(title)
        
        # 填写视频描述
        print("📝 填写视频描述...")
        desc_textarea = page.ele('css:textarea[placeholder="输入视频描述"]')
        desc_textarea.input(desc)
        
        # 上传视频文件
        print("📤 上传视频文件...")
        video_upload_input = page.ele('css:input[type="file"][accept="video/*"]')
        video_upload_input.input(video_file)  # 在DrissionPage中，使用input()方法上传文件
        
        # 上传封面图片
        print("📤 上传封面图片...")
        cover_upload_input = page.eles('css:input[type="file"][accept="image/*"]')[1]  # 选择第二个图片输入框（竖版封面）
        cover_upload_input.input(cover_file)  # 在DrissionPage中，使用input()方法上传文件
        
        # 等待上传完成
        print("⏳ 等待文件上传完成...")
        time.sleep(5)  # 等待5秒，确保文件上传完成
        
    else:
        print("❌ 未找到插件页，请检查：\n1. 9223端口的Chrome是否已开启\n2. Chrome是否已正确打开插件页")
        return False
    
    return True

if __name__ == "__main__":
    # 启动Chrome并直接打开扩展页面
    start_chrome_with_extension()
    time.sleep(3)
    # 连接到扩展页面，默认使用文件夹"1"
    connect_to_extension("1")