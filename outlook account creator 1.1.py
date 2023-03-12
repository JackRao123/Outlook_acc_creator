from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import csv
from faker import Faker
from faker.providers import person
import random
import string
from time import sleep as wait
import sys
#from pyvirtualdisplay import Display
import json
from urllib.request import urlretrieve
import requests
 
import time
import os
import zipfile




class GenerateRandom:
    def random_char(self, y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))

    def nonce(self, length=4):
        return ''.join([str(random.randint(0, 9)) for i in range(length)])


class Register:
    def __init__(self, password):
        try:
            with open(r'C:\Users\raoj6\Desktop\Python projects\Outlook Account Creator\create_acc_config.json') as json_data_file:
                config = json.load(json_data_file)
                self.proxy_file =  config['create_proxy_file']
                #self.api_key = config['captcha_api_key']
                self.headless = config['headless']
                self.account_index = config['index']
                self.user_password = password
        except FileNotFoundError:
            print("No config.json found")
        self.outlook_url = "https://outlook.live.com/owa/?nlp=1&signup=1"
        self.chrome_options = Options()
        if sys.platform == "linux" or sys.platform == "linux2":
            self.exe_path =# put path to chromedriver.exe here
            self.chrome_options.add_argument('--no-sandbox')
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--disable-gpu')


            display = Display(visible=0, size=(800, 800))
            display.start()
        else:
            self.exe_path = "drivers/chromedriver.exe"

        self.chrome_options.add_argument('--disable-web-security')
        self.chrome_options.add_argument('--disable-site-isolation-trials')
        self.chrome_options.add_argument('--disable-application-cache')

        self.chrome_options.add_argument("--window-size=1920x1080")
        if self.headless ==  True :
            self.chrome_options.add_argument('--headless')


        proxy_string = self.get_proxy_from_file()
        self.chrome_options = self.attach_proxy_to_options(self.chrome_options, proxy_string )


        self.fake = Faker("en_US")
        self.gen = GenerateRandom()

    def is_visible(self, locator, timeout=30):
        try:
            ui.WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((By.ID, locator)))
            return True
        except TimeoutException:
            return False

    def attach_proxy_to_options(self, chrome_options, proxy_string):  # proxy strign is user:pass@host:port
        # takes a chrome_options (webdriver.ChromeOptions()) and adds a proxy to it.
        user_password, host_port = proxy_string.split("@")
        user, password = user_password.split(":")
        host, port = host_port.split(":")

        

        PROXY_HOST = host  # rotating proxy or host
        PROXY_PORT = port  # port
        PROXY_USER = user  # username
        PROXY_PASS = password  # password

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        pluginfile = r'C:\Users\raoj6\Desktop\Python projects\Outlook Account Creator\proxy_auth_plugin.crx'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        chrome_options.add_extension(pluginfile)



        return chrome_options

    def get_proxy_from_file(self):
        with open(self.proxy_file, "r") as json_file:
            json_data = json.load(json_file)


        proxy_list = []
        proxies = json_data['proxies']
        for key, value in proxies.items():
            if value['active'] == True:
                proxy_list.append(value['proxy'])

        chosen_proxy = random.choice(proxy_list)
        print(f"Chosen Proxy = {chosen_proxy}")
        return chosen_proxy

    def page_has_loaded(self):
        page_state = self.driver.execute_script('return document.readyState;')
        return True
    def solve_captcha(self, public_key, service_url, site_url):
        api_key = self.api_key
        api_send_url = r'http://2captcha.com/in.php'
        api_receive_url = r'http://2captcha.com/res.php'
        method = 'funcaptcha'

        #debug
        print(public_key)
        print(service_url)
        print(site_url)




        try:
            req = requests.get(f"{api_send_url}?key={api_key}&method={method}&publickey={public_key}&surl={service_url}&pageurl={site_url}")
            request_id = req.text.replace("OK|","").replace(" ","").replace("\n","")

            while "NOT" in requests.get(f"{api_receive_url}?key={api_key}&action=get&id={request_id}").text:  #"CAPCHA_NOT_READY" while its not ready
                time.sleep(4)
                print(f"Result not ready...")

            result = requests.get(f"{api_receive_url}?key={api_key}&action=get&id={request_id}").text
            result = result[3:] #gets fir do the "OK|" at the front
            print(f"Result = {result}")

        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)







    def make_outlook(self):

        try:
            print("Generating new account...")
            proxy_string = self.get_proxy_from_file()

            chrome_opts = Options()
            chrome_opts  = self.attach_proxy_to_options( Options(), proxy_string    )
            self.driver = webdriver.Chrome(chrome_options = chrome_opts, executable_path=self.exe_path)

            self.driver.get(self.outlook_url)



            if self.page_has_loaded() is True:
                if self.is_visible("CredentialsPageTitle") is True:
                    pass
                    print('Page Loaded')
            first, last = self.fake.first_name().rstrip(), self.fake.last_name().rstrip()
            #username = first + last + str(self.gen.nonce(5))
            username = f"ttdogacc{self.account_index}"
            password_input = self.user_password

            self.driver.find_element(By.ID, "MemberName").send_keys(username)



            if self.is_visible("iSignupAction") is True:
                pass
            wait(0.5)
            self.driver.find_element(By.ID,"iSignupAction").click()
            wait(2)

            while self.is_visible("MemberNameError",4) == True:
                self.account_index = self.account_index +  1
                username = # change this to whatever naming scheme you want, e.g michaelstevenson1, michaelstevenson2....
                self.driver.find_element(By.ID, "MemberName").clear()
                self.driver.find_element(By.ID, "MemberName").send_keys(username)
                self.driver.find_element(By.ID, "iSignupAction").click()



            if self.is_visible("PasswordInput") is True:
                    pass
            self.driver.find_element(By.ID,"PasswordInput").send_keys(password_input)
            if self.is_visible("iSignupAction") is True:
                    pass
            wait(0.5)
            self.driver.find_element(By.ID,"iSignupAction").click()
            wait(1)
            if self.is_visible("FirstName") is True:
                    pass
            self.driver.find_element(By.ID,"FirstName").send_keys(first)
            self.driver.find_element(By.ID,"LastName").send_keys(last)
            if self.is_visible("iSignupAction") is True:
                    pass
            wait(0.5)
            self.driver.find_element(By.ID,"iSignupAction").click()
            wait(1)
            if self.is_visible("Country") is True:
                    pass
            country = "Australia" #requests.get('https://ipapi.co/country_name/', proxies={"http": "socks://" + proxy_string}).text
            #countrygeo = Select(self.driver.find_element(By.ID,"Country"))
            #countrygeo.select_by_visible_text(str(country))
            indexm = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
            indexd = random.randint(1, 28)
            indexy = random.randint(1980, 2000)
            birthM = Select(self.driver.find_element(By.ID,"BirthMonth"))
            birthM.select_by_visible_text(random.choice(indexm))
            birthD = Select(self.driver.find_element(By.ID,"BirthDay"))
            birthD.select_by_visible_text(str(indexd))
            birthY = self.driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div/div[1]/div[3]/div/div[1]/div[5]/div/div/form/div/div[4]/div[3]/div[3]/input")
            birthY.send_keys(indexy)
            self.driver.find_element(By.ID,"iSignupAction").click()



            if self.is_visible("enforcementFrame") is True:
                pass


            #there are three iframes
            #enforcementFrame
                #->fc-iframe-wrap
                    #->CaptchaFrame
            f1 = self.driver.find_element(By.ID, "enforcementFrame")
            self.driver.switch_to.frame(f1)
            time.sleep(500)
            f_1 = self.driver.find_element(By.ID, '//*[@id="arkose"]/div/iframe')
            self.driver.switch_to.frame(f_1)

            f2 = self.driver.find_element(By.ID, '//*[@id="fc-iframe-wrap"]')
            self.driver.switch_to.frame(f2)
            f3 = self.driver.find_element(By.ID, '//*[@id="CaptchaFrame"]')
            self.driver.switch_to.frame(f3)

#              #getting data for the solve captcha
# ##            fc_token = self.driver.find_element(By.ID, 'FunCaptcha-Token').get_attri    bute('value') #have to put it here because its in enforcementFrame, not the other frames.
# ##            fc_token_arr = fc_token.split("|")
# ##            print(fc_token_arr)
# ##            public_key = ""
# ##            service_url = ""
# ##            site_url = self.driver.current_url
# ##
# ##            for section in fc_token_arr:
# ##                if "pk=" in section:
# ##                    public_key = section.replace("pk=","")
# ##                if "surl=" in section:
# ##                    service_url = section.replace("surl=","")
# ##            print(public_key, service_url, site_url)


            self.driver.find_element(By.XPATH, '//*[@id="home_children_button"]').click() #this is the 'Next' Button (opens the Captcha)

#             #now we have to solve the captcha
	      solve_captcha(self,  public_key, service_url, site_url):
              self.solve_captcha(public_key, service_url, site_url)
#              
#
#
            if self.is_visible("idSIButton9",1000) is True: #wait until we manually do the captcha
                print("Captcha done.")
                pass

            self.account_index = self.account_index + 1
            with open(r"C:\Users\Jack\Desktop\Python projects\Outlook Account Creator\create_acc_config.json", "r+") as file:
                data = json.load(file)
                data['index'] = self.account_index
                file.seek(0)
                json.dump(data, file, indent = 4)
                file.truncate()


        except Exception as e:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)




if __name__ == "__main__":
    threads = []

    password = input("Enter master password: ")
    os.system('cls')

    print("Outlook Creator")
    accounts_to_create = int(input("How many accounts would you like to create?" + "\n"))




    regBot = Register(password)
    for i in range(accounts_to_create):
        regBot.make_outlook()




    print("Finished.")
