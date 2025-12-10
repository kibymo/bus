from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
import os

def send_telegram(message):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("[WARN] TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set in environment.")
        print("       Skipping Telegram notification.")
        return
    
    # Using curl as requested, but using --data-urlencode for safety with special chars/newlines
    cmd = [
        "/usr/bin/curl", "-s", "-X", "POST",
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        "-d", f"chat_id={chat_id}",
        "--data-urlencode", f"text={message}"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"Telegram response: {result.stdout}")
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    
    chrome_service = Service()
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10785"
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    
    # Define targets
    # (selector_for_rows, list_of_stop_names_to_find, route_label)
    targets = [
        ("tr.ttego1, tr.ttego2", ["介壽國中", "聯合二村", "民生社區活動中心"], "Go Route (往民生社區)"),
        ("tr.tteback1, tr.tteback2", ["三民路", "三民健康路口(西松高中)", "健康新城"], "Return Route (往大鵬新城)")
    ]

    message_lines = []

    try:
        # Wait for at least one of the tables (Go route default usually loads)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ttego1")))
        
        # Compact format
        # Time: ~5 chars, Stop: ~14 chars, Bus: ~8 chars
        header = f"{'Time':<5} {'Stop Name':<14} {'Bus No.':<8} {'Status'}"
        print(header)
        print("-" * 40)
        
        message_lines.append(header)
        message_lines.append("-" * 40)

        for selector, stop_names, route_label in targets:
            
            rows = driver.find_elements(By.CSS_SELECTOR, selector)
            
            for row in rows:
                try:
                    stop_name_element = row.find_element(By.TAG_NAME, "a")
                    current_stop_name = stop_name_element.text.strip()
                    
                    if current_stop_name in stop_names:
                         # Found a target stop, extract details
                        time_cell = row.find_elements(By.TAG_NAME, "td")[1]
                        full_text = time_cell.text.strip()
                        arrival_time = full_text.split('\n')[0]
                        if not arrival_time:
                             arrival_time = full_text
                        
                        bus_number = ""
                        try:
                            font_elem = time_cell.find_element(By.TAG_NAME, "font")
                            bus_number = font_elem.text.strip()
                        except:
                            pass
                        
                        crowd_status = ""
                        try:
                            imgs = time_cell.find_elements(By.TAG_NAME, "img")
                            for img in imgs:
                                src = img.get_attribute("src")
                                if "crowd0.gif" in src:
                                    crowd_status = "舒適"
                                elif "crowd1.gif" in src:
                                    crowd_status = "中等"
                                elif "crowd2.gif" in src:
                                    crowd_status = "擁擠"
                        except:
                            pass
                        
                        line_output = f"{arrival_time:<5} {current_stop_name:<14} {bus_number:<8} {crowd_status}"
                        print(line_output)
                        message_lines.append(line_output)

                except Exception as e:
                    continue

    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        if message_lines:
            full_message = "\n".join(message_lines)
            send_telegram(full_message)

if __name__ == "__main__":
    main()
