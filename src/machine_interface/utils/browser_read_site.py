from human_interface import BrowserHandler

def run(browser: BrowserHandler) -> str:
    try:
        return browser.extract_html()
    except Exception as err:
        return f"Error occured when trying to launch browser: {err}"