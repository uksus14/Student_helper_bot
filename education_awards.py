from selenium import webdriver
from time import sleep
from os import system as o
char = "\n"
mail = input("Enter your auca email\n")
password = input("Enter your password\n")
f = {"t":lambda e,p:e.find_element_by_tag_name(p),
     "c":lambda e,p:e.find_element_by_class_name(p),
     "i":lambda e,p:e.find_element_by_id(p),
     "ts":lambda e,p:e.find_elements_by_tag_name(p),
     "cs":lambda e,p:e.find_elements_by_class_name(p),
     "is":lambda e,p:e.find_elements_by_id(p)}
def q(s, p):
  if not p: return s
  pt, pn = p[0].split()
  return q(f[pt](s, pn), p[1:])

driver = webdriver.Chrome("C:\\bin\\chromedriver.exe")
driver.get("https://tsiauca.edupage.org/login/?msg=3")
driver.minimize_window()
driver.maximize_window()
driver.find_element_by_id("login_Login_1e1").send_keys(mail)
driver.find_element_by_id("login_Login_1e2").send_keys(password)
sleep(1)
driver.get("https://tsiauca.edupage.org/znamky/?")
sleep(1)
q(driver, ["i bar_mainDiv", "c edubarMainNoSkin", "t div", "c znamkyTable", "t tbody", "c znamkyViewerLoadOlderTd"]).click()
gs = sorted([(q(elem, ['t td', 't b']).text.split(char)[0], round(sum([0]+[float(tip.text.split()[0]) for tip in q(elem, ['cs znZnamka'])]), 1)) for elem in q(driver, ["i bar_mainDiv", "c edubarMainNoSkin", "t div", "c znamkyTable", "t tbody", "cs predmetRow"])[1:]], key=lambda _:_[1])
with open("C:\\Users\\akylo\\Desktop\\ruslan\\phrases.txt", mode="w", encoding="utf-8") as f: f.write("\n".join([f"{g[0].strip().ljust(1+len(max(gs, key=len)))}|{g[1]}"for g in gs]))
driver.close()
# o("C:\\Users\\Akylo\\Desktop\\inokentiy\\AUCA\\grades.txt")
print(555)
