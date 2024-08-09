from filework import METAMASK, PASSWORD, gen_phrase
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, \
	SessionNotCreatedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from time import sleep, localtime, strftime


def searcher() -> dict:
	while True:
		try:
			options = webdriver.ChromeOptions()
			options.add_argument("--headless=new")
			options.add_extension(METAMASK)
			driver = webdriver.Chrome(options=options)
			driver.implicitly_wait(10)
			break
		except SessionNotCreatedException:
			print(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: SessionNotCreatedException [network -> 20]")
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
			print(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: NoSuchElementException [network -> 33]")
			sleep(1)
	# BUTTON: Import exists wallet
	driver.find_elements(By.CLASS_NAME, "button")[1].click()
	# BUTTON: Agreement
	driver.find_elements(By.CLASS_NAME, "button")[1].click()
	while True:
		srp = gen_phrase()
		# FIELD: Put seed phrase
		while not len(driver.find_elements(By.ID, f"import-srp__srp-word-0")):
			sleep(1)
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
			while True:
				try:
					# BUTTON: Settings
					driver.find_elements(By.XPATH, f"/html/body/{"div/" * 7}button")[1].click()
					break
				except IndexError:
					print(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: IndexError [network -> 66]")
					sleep(1)
				except ElementClickInterceptedException:
					print(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: ElementClickInterceptedException [network -> 69]")
					sleep(1)
			# BUTTON: Address
			driver.find_elements(By.XPATH, f"/html/body/{"div/" * 6}button")[1].click()
			# TEXT: Addr
			addr = driver.find_element(By.XPATH, f"/html/body/{"div/" * 3}/section/{"div/" * 6}button/span/div").text
			return {"srp": " ".join(srp), "addr": addr, "age": "None", "bal": "None"}
		except ElementClickInterceptedException:
			for i in range(12):
				driver.find_element(By.ID, f"import-srp__srp-word-{i}").send_keys(Keys.CONTROL, "a")
				driver.find_element(By.ID, f"import-srp__srp-word-{i}").send_keys(Keys.DELETE)


def checker(wallet) -> dict:
	options = webdriver.ChromeOptions()
	options.add_argument("--headless=new")
	driver = webdriver.Chrome(options=options)
	driver.implicitly_wait(3)
	# try:
	driver.get(f"https://debank.com/profile/{wallet["addr"]}")
	# except Exception as e:
	# 	return {"type": "None", "error": e}
	while True:
		try:
			wallet["bal"] = driver.find_element(By.CSS_SELECTOR, "div.HeaderInfo_totalAssetInner__HyrdC").text.split("\n")[0]
			break
		except NoSuchElementException:
			print(f"{strftime("%H:%M:%S %d/%m/%y", localtime())} LOG: NoSuchElementException [network -> 96]")
			sleep(1)
	try:
		wallet["age"] = driver.find_element(By.CSS_SELECTOR, "div.is-age").text.split("\n")[0]
	except NoSuchElementException:
		pass
	return wallet
