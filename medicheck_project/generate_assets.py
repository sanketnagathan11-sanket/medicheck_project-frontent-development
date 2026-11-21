import base64
import requests
import os
from playwright.sync_api import sync_playwright

def get_er_diagram():
    print("Generating ER diagram...")
    mermaid_code = """erDiagram
      PATIENT ||--o{ BOOKING : places
      BOOKING }o--|{ TEST : includes
      STAFF ||--o{ BOOKING : manages
      PATIENT {
        int patient_id
        string full_name
        string phone
        string membership_tier
      }
      BOOKING {
        int booking_id
        string status
        date booking_date
        float total_amount
      }
      TEST {
        int test_id
        string test_name
        float price
      }
      STAFF {
        int staff_id
        string role
      }
    """
    # Use mermaid.ink API
    b64 = base64.urlsafe_b64encode(mermaid_code.encode()).decode()
    url = f"https://mermaid.ink/img/{b64}"
    
    r = requests.get(url)
    if r.status_code == 200:
        with open("er_diagram.png", "wb") as f:
            f.write(r.content)
        print("ER diagram saved.")
    else:
        print("Failed to fetch ER diagram.", r.status_code)

def get_screenshots():
    print("Generating Screenshots...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            
            # Load index.html
            file_url = f"file:///{os.path.abspath('index.html').replace(chr(92), '/')}"
            print(f"Loading {file_url}")
            page.goto(file_url, wait_until="networkidle")
            
            # Home page screenshot
            page.screenshot(path="screenshot_home.png")
            print("Home screenshot saved.")
            
            # Navigate to staff portal (Admin)
            page.evaluate("showPage('admin')")
            page.wait_for_timeout(1000)
            page.screenshot(path="screenshot_admin.png")
            print("Admin screenshot saved.")
            
            browser.close()
    except Exception as e:
        print("Playwright failed:", e)

if __name__ == "__main__":
    get_er_diagram()
    get_screenshots()
