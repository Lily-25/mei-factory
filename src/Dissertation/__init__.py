from playwright.sync_api import sync_playwright
import time

# 配置项（需根据目标网页修改！！！）
TARGET_URL = "https://chat.deepseek.com/"  # 报告提交页面URL
FILE_UPLOAD_XPATH = "/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div[1]/div[1]"   # 文件上传input标签的XPath
PROMPT_XPATH = "/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div/div[1]/textarea"# 报告描述文本框XPath
SUBMIT_BTN_XPATH = "/html/body/div[1]/div/div/div[2]/div[3]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/div/div[2]/svg"# 提交按钮XPath
LOCAL_FILE_PATH = "./Paper/Burmeister_2016_Knowledgeretentionfromolderworkers_WORKAR.pdf" # 本地要上传的文件路径
SUCCESS_TEXT = "提交成功" # 提交成功的页面提示文本（用于验证）

def auto_submit_report():
    with sync_playwright() as p:
        # 1. 启动Chrome浏览器（无头模式：headless=True，可视化：headless=False）
        browser = p.chromium.launch(
            headless=False,  # 可视化操作，方便调试；上线可改为True
            args=["--start-maximized"]  # 浏览器窗口最大化
        )
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        page.goto(TARGET_URL)  # 打开目标页面
        time.sleep(2)  # 等待页面加载（可替换为更智能的wait_for_selector）

        try:
            # 2. 定位文件上传框，上传本地文件（核心：set_input_files）
            page.wait_for_selector(FILE_UPLOAD_XPATH, timeout=10000)  # 等待元素加载，超时10s
            page.locator(FILE_UPLOAD_XPATH).set_input_files(LOCAL_FILE_PATH)
            print("✅ 文件上传成功")
            time.sleep(3)  # 等待文件上传/解析（根据文件大小调整）

            # 3. 填写报告表单
            page.locator(PROMPT_XPATH).fill("Please extract the challenges the paper researched")  # 填写描述
            print("✅ 报告表单填写完成")
            time.sleep(1)

            # 4. 点击提交按钮，等待页面跳转
            page.locator(SUBMIT_BTN_XPATH).click()
            page.wait_for_navigation(wait_until="load")  # 等待提交后页面加载完成
            print("✅ 点击提交按钮成功")

            # 5. 验证提交是否成功（检查页面是否出现成功提示）
            if page.locator(f"//*[contains(text(), '{SUCCESS_TEXT}')]").is_visible():
                print("🎉 报告提交并上传文件，全程自动化完成！")
            else:
                print("❌ 提交失败，未检测到成功提示")

        except Exception as e:
            print(f"❌ 操作失败：{str(e)}")
        finally:
            # 6. 关闭浏览器（如需保留窗口，注释掉即可）
            time.sleep(5)
            browser.close()

if __name__ == "__main__":

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # ======================
        # 1. 登录
        # ======================
        login_url = "https://chat.deepseek.com/sign_in"
        page.goto(login_url)

        account_input = page.locator('//html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div[1]/div/input')
        password_input = page.locator(
            '//html/body/div[1]/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/div/input')

        # 等待输入框可点击（确保元素加载完成）
        account_input.wait_for(state="editable", timeout=5000)
        # 输入账号密码（用type模拟真实输入，比fill更适配特殊输入框）
        account_input.type("lily02062303@gmail.com")
        password_input.type("Lily2026")

        # 点击登录按钮（优先用文字定位，更稳定）
        login_btn = page.locator('button:has-text("Log in")')
        login_btn.click()

        # 等待登录成功跳转
        page.wait_for_url("https://chat.deepseek.com/", timeout=10000)
        print("登录成功")

        auto_submit_report()