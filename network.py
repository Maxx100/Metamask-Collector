from filework import METAMASK, PASSWORD, gen_phrase, DRIVER
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
	SessionNotCreatedException, WebDriverException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from time import sleep, localtime, strftime


class Net:
	def __init__(self):
		options = webdriver.ChromeOptions()
		options.add_argument('--disable-logging')
		options.add_argument('--disable-search-engine-choice-screen')
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		options.add_argument("--headless=new")
		service = webdriver.ChromeService(executable_path=DRIVER)
		while True:
			try:
				self.driverDeBank = webdriver.Chrome(options=options, service=service)
				break
			except SessionNotCreatedException:
				sleep(1)
		self.driverDeBank.implicitly_wait(1)
		self.driverDeBank.get("https://google.com")
	
	@staticmethod
	def searcher() -> dict:
		while True:
			try:
				options = webdriver.ChromeOptions()
				options.add_argument('--disable-logging')
				options.add_argument('--disable-search-engine-choice-screen')
				options.add_experimental_option('excludeSwitches', ['enable-logging'])
				options.add_argument("--headless=new")
				options.add_extension(METAMASK)
				service = webdriver.ChromeService(executable_path=DRIVER)
				driver = webdriver.Chrome(options=options, service=service)
				driver.implicitly_wait(1)
				break
			except SessionNotCreatedException:
				print(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: SessionNotCreatedException [network -> 24]")
				sleep(1)
		# driver.get("chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html")
		while len(driver.window_handles) < 2:
			sleep(1)
		driver.close()
		driver.switch_to.window(window_name=driver.window_handles[0])
		while True:
			try:
				# CHECKBOX: Terms of use
				driver.find_element(By.ID, "onboarding__terms-checkbox").click()
				break
			except NoSuchElementException:
				print(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: NoSuchElementException [network -> 37]")
				sleep(1)
		# BUTTON: Import exists wallet
		driver.find_elements(By.CLASS_NAME, "button")[1].click()
		# BUTTON: Agreement
		driver.find_elements(By.CLASS_NAME, "button")[1].click()
		srp = gen_phrase()
		while True:
			cnt = 0
			# FIELD: Put seed phrase
			while cnt < 10 and not len(driver.find_elements(By.ID, f"import-srp__srp-word-0")):
				cnt += 1
				sleep(1)
			if cnt == 10:
				driver.quit()
				return {"error": "Metamask Error", "type": "Filling fields error"}
			for i in range(12):
				driver.find_element(By.ID, f"import-srp__srp-word-{i}").send_keys(srp[i])
			try:
				# BUTTON: If active - recovery
				driver.find_element(By.CLASS_NAME, "button").click()
				# FILED: Put password
				driver.find_elements(By.CLASS_NAME, "form-field__input")[0].send_keys(PASSWORD)
				driver.find_elements(By.CLASS_NAME, "form-field__input")[1].send_keys(PASSWORD)
				# CHECKBOX: Metamask can't recovery this password
				driver.find_element(By.CLASS_NAME, "check-box").click()
				# BUTTON: Import wallet
				driver.find_element(By.CLASS_NAME, "button").click()
				# BUTTON: Success - Understand
				driver.find_element(By.XPATH, f"/html/body/{"div/" * 7}button").click()
				# BUTTON: Install is done - Next
				driver.find_element(By.XPATH, f"/html/body/{"div/" * 7}button").click()
				# BUTTON: Complete
				driver.find_element(By.XPATH, f"/html/body/{"div/" * 7}button").click()
				cnt = 0
				while True:
					if cnt == 10:
						driver.quit()
						return {"type": "Metamask Time Out", "error": "ETH Net connect error"}
					try:
						# BUTTON: Settings
						driver.find_elements(By.XPATH, f"/html/body/{"div/" * 7}button")[1].click()
						break
					except IndexError:
						print(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: IndexError [network -> 80]")
						sleep(1)
						cnt += 1
					except ElementClickInterceptedException:
						print(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: ElementClickInterceptedException [network -> 84]")
						sleep(1)
						cnt += 1
				# BUTTON: Address
				driver.find_elements(By.XPATH, f"/html/body/{"div/" * 6}button")[1].click()
				# TEXT: Addr
				addr = driver.find_element(By.XPATH, f"/html/body/{"div/" * 3}/section/{"div/" * 6}button/span/div").text
				driver.quit()
				return {"srp": " ".join(srp), "addr": addr, "age": "None", "bal": "None"}
			except ElementClickInterceptedException:
				for i in range(12):
					driver.find_element(By.ID, f"import-srp__srp-word-{i}").send_keys(Keys.CONTROL, "a")
					driver.find_element(By.ID, f"import-srp__srp-word-{i}").send_keys(Keys.DELETE)
				srp = gen_phrase()
			except WebDriverException:
				pass
		
	def checker(self, wallet) -> dict:
		self.driverDeBank.get(f"https://debank.com/profile/{wallet["addr"]}")
		cnt = 0
		while cnt < 10:
			try:
				if "Data updated" in self.driverDeBank.find_element(By.CSS_SELECTOR, "span.UpdateButton_refresh__vkj2W").text:
					wallet["bal"] = self.driverDeBank.find_element(
						By.CSS_SELECTOR,
						"div.HeaderInfo_totalAssetInner__HyrdC").text.split("\n")[0]
					break
			except NoSuchElementException:
				cnt += 1
				print(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: NoSuchElementException [network -> 126]")
				sleep(1)
		if cnt == 20:
			return {"type": "DeBank Time out", "error": "DeBank page isn't loading"}
		try:
			wallet["age"] = self.driverDeBank.find_element(By.CSS_SELECTOR, "div.is-age").text.split("\n")[0]
		except NoSuchElementException:
			pass
		return wallet
