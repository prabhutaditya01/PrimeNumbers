import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def getData(url):
    r=requests.get("https://hprera.nic.in/Project/ProjectRegistration/PromotorDetails_PreviewPV?qs="+url,verify=False,headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',})
    soup=BeautifulSoup(r.content,"html.parser")
    res=soup.findAll('td')
    gstin = soup.find('td', string='GSTIN No.').find_next_sibling('td').text.strip()
    name = soup.find('td', string='Name').find_next_sibling('td').text.strip()
    pan_no = soup.find('td', string='PAN No.').find_next_sibling('td').text.strip().split("\n")[0]
    address = soup.find('td', string='Permanent Address').find_next_sibling('td').text.strip().split("\n")[0]
    return {"GSTIN":gstin,"PAN":pan_no,"Name":name,"Address":address}


# Path to your chromedriver
chromedriver_path = r'C:\Users\prabh\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Setup ChromeDriver with options
options = Options()
options.headless = True  # Run in headless mode
service = ChromeService(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open the website
    url = "https://hprera.nic.in/PublicDashboard"
    driver.get(url)

    # Wait until the specific element is present
    wait = WebDriverWait(driver, 100)  # Wait for up to 0 seconds
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tab_project_main-filtered-data .form-row")))

    # Get the page source after all dynamic content has loaded
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Select the specific div that contains the data
    res=soup.findAll('a')
    qs_data=[]
    for i in res:
        if(i.get("data-qs") and i.get("title") == "View Application"):
            qs_data.append(i.get("data-qs"))
            print(i.get("data-qs"))
    
    final_data=[]
    for j in qs_data[:6]:
        final_data.append(getData(j))
    # project_div = soup.select_one("#tab_project_main-filtered-data")
    # with open("output.txt","w") as txt_file:
    #     for line in qs_data:
    #         txt_file.write(" ".join(line)+"\n")
    # if project_div:
    #     for child in project_div.children:
    #         if child.name:  # Filter out any text nodes or other non-tag elements
    #             print(child.prettify())  # Pretty print the HTML of each child element
    
    print(final_data)
    
finally:
    driver.quit()