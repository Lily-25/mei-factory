from playwright.sync_api import sync_playwright
import time
import os


def deepseek_login_and_analyze():
    # 配置信息（替换成你自己的）
    DEEPSEEK_USERNAME = "lily02062303@gmail.com"
    DEEPSEEK_PASSWORD = "Lily2026"
    UPLOAD_FILE_PATH = os.path.abspath("./Paper/Burmeister_2016_Knowledgeretentionfromolderworkers_WORKAR.pdf")  # 替换成你的文档路径
    # 支持的文档格式：pdf、docx、txt、md 等

    with sync_playwright() as p:
        # 1. 启动浏览器，配置防检测参数
        browser = p.chromium.launch(
            headless=False,  # 显示浏览器，方便调试
            slow_mo=200,  # 慢动作执行，模拟真人操作
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--start-maximized"  # 最大化窗口
            ]
        )

        # 2. 配置上下文，伪装真人环境
        context = browser.new_context(
            viewport=None,  # 跟随窗口大小
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="zh-CN",
            timezone_id="Asia/Shanghai"
        )

        # 3. 移除Playwright自动化标识（核心防检测）
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh'] });
            window.chrome = { runtime: {} };
        """)

        page = context.new_page()

        try:
            # ====================== 第一步：访问DeepSeek并登录 ======================
            print("正在打开DeepSeek官网...")
            page.goto("https://chat.deepseek.com/sign_in", timeout=30000)
            time.sleep(3)  # 等待页面完全加载

            # 点击登录按钮
            """print("点击登录按钮...")
            login_btn = page.locator('//button[contains(text(), "登录") or contains(@class, "login")]')
            login_btn.wait_for(state="visible", timeout=10000)
            login_btn.click()
            time.sleep(2)"""

            # 定位账号输入框（兼容DeepSeek的输入框封装）
            print("输入账号...")
            account_input = page.locator(
                '//div[contains(@class, "input-wrap") and .//label[contains(text(), "账号")]]//input')
            if not account_input.is_visible():
                account_input = page.locator('//input[@placeholder="请输入手机号/邮箱"]')

            # 模拟真人输入账号
            account_input.click()
            time.sleep(0.5)
            page.keyboard.press("ctrl+a")
            page.keyboard.press("backspace")
            for char in DEEPSEEK_USERNAME:
                page.keyboard.type(char)
                time.sleep(0.1)

            # 定位密码输入框并输入
            print("输入密码...")
            pwd_input = page.locator(
                '//div[contains(@class, "input-wrap") and .//label[contains(text(), "密码")]]//input')
            if not pwd_input.is_visible():
                pwd_input = page.locator('//input[@placeholder="请输入密码"]')

            pwd_input.click()
            time.sleep(0.5)
            page.keyboard.press("ctrl+a")
            page.keyboard.press("backspace")
            for char in DEEPSEEK_PASSWORD:
                page.keyboard.type(char)
                time.sleep(0.1)

            # 点击登录确认按钮
            print("提交登录...")
            submit_btn = page.locator('//button[@type="submit" and contains(text(), "登录")]')
            submit_btn.click()
            time.sleep(5)  # 等待登录跳转

            # 验证登录是否成功
            if "登录" not in page.content():
                print("✅ 登录成功！")
            else:
                raise Exception("❌ 登录失败，请检查账号密码！")

            # ====================== 第二步：上传文档并分析 ======================
            print("准备上传文档...")
            # 点击上传文件按钮（DeepSeek的上传入口）
            upload_btn = page.locator('//button[contains(@class, "upload-btn") or .//svg[@aria-label="上传"]]')
            if not upload_btn.is_visible():
                upload_btn = page.locator('//div[contains(text(), "上传文件") or contains(@class, "upload")]')

            upload_btn.click()
            time.sleep(2)

            # 定位文件上传输入框并上传
            file_input = page.locator('//input[@type="file"]')
            if not os.path.exists(UPLOAD_FILE_PATH):
                raise Exception(f"❌ 文件不存在：{UPLOAD_FILE_PATH}")

            file_input.set_input_files(UPLOAD_FILE_PATH)
            print(f"📤 正在上传文件：{UPLOAD_FILE_PATH}")
            time.sleep(5)  # 等待文件上传完成

            # 发送分析指令（让DeepSeek分析文档）
            print("📝 发送分析指令...")
            chat_input = page.locator('//textarea[@placeholder="输入你的问题..." or @role="textbox"]')
            chat_input.click()
            chat_input.type("请详细分析这份文档的核心内容、关键观点和潜在结论，输出结构化的分析报告")
            time.sleep(1)

            # 点击发送按钮
            send_btn = page.locator('//button[@type="submit" or .//svg[@aria-label="发送"]]')
            send_btn.click()
            time.sleep(10)  # 等待分析结果返回

            # 等待分析完成（监测回复区域加载完成）
            print("⌛ 等待分析完成...")
            page.wait_for_selector('//div[contains(@class, "message-content") and not(contains(@class, "loading"))]',
                                   timeout=60000)
            print("✅ 文档分析完成！")

            # 保存分析结果截图
            page.screenshot(path="deepseek_analysis_result.png")
            print("📸 分析结果已保存为：deepseek_analysis_result.png")

        except Exception as e:
            print(f"❌ 执行出错：{str(e)}")
            # 出错时保存截图，方便排查
            page.screenshot(path="deepseek_error.png")
        finally:
            # 可选：停留10秒查看结果，再关闭浏览器
            print("⏳ 10秒后关闭浏览器...")
            time.sleep(10)
            browser.close()


if __name__ == "__main__":
    # 运行主函数
    deepseek_login_and_analyze()