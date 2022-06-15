from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from os import system as o
find_func ={"t":lambda e,p:e.find_element(By.TAG_NAME, p),
            "c":lambda e,p:e.find_element(By.CLASS_NAME, p),
            "i":lambda e,p:e.find_element(By.ID, p),
            "ts":lambda e,p:e.find_elements(By.TAG_NAME, p),
            "cs":lambda e,p:e.find_elements(By.CLASS_NAME, p)}

grade_to_gpa = {"A": 4,"A-": 3.67,"B+": 3.33,"B": 3,"B-": 2.67,"C+": 2.33,"C": 2,"C-": 1.67,"D+": 1.33,"D": 1,"D-": 0.67,"F": 0}

def gpa_to_grade(gpa):
  if gpa>=3.6: return "A"
  elif gpa>=3.3: return "B+"
  elif gpa>=3.0: return "B"
  elif gpa>=2.6: return "B-"
  elif gpa>=2.3: return "C+"
  elif gpa>=2.0: return "C"
  elif gpa>=1.6: return "C-"
  elif gpa>=1.3: return "D+"
  elif gpa>=1.0: return "D"
  elif gpa>=0.6: return "D-"
  else: return "F"

char = "\n"
mail = input("Enter your auca email\n")
password = input("Enter your password\n")
f = {"t":lambda e,p:e.find_element_by_tag_name(p),
     "c":lambda e,p:e.find_element_by_class_name(p),
     "i":lambda e,p:e.find_element_by_id(p),
     "ts":lambda e,p:e.find_elements_by_tag_name(p),
     "cs":lambda e,p:e.find_elements_by_class_name(p),
     "is":lambda e,p:e.find_elements_by_id(p)}

def grade(b):
  g = "A"
  if   b<60:g = "F"
  elif b<63:g = "D-"
  elif b<67:g = "D" 
  elif b<70:g = "D+"
  elif b<73:g = "C-"
  elif b<77:g = "C"
  elif b<80:g = "C+"
  elif b<83:g = "B-"
  elif b<87:g = "B"
  elif b<90:g = "B+"
  elif b<93:g = "A-"
  return g
def is_valid_tip(tip):
  if tip.find_element(By.XPATH,"..").get_attribute("original-title").lower().find("<br>")<0 and all(map(lambda _:_ not in "ABCDFP",tip.text)):
    return float(tip.text.split()[0])
  else: return 0
def q(current, all_path):
  if not all_path: return current
  move_type, move_direction = all_path[0].split()
  return q(find_func[move_type](current, move_direction), all_path[1:])

with open("additional\\subjects.txt", "r", encoding="utf-8") as f: data = f.read().split("\n")
credit = [(data[sub], float(data[sub+1])) for sub in range(0, len(data), 2)]
general_cred = sum([sub[1] for sub in credit])

driver = webdriver.Chrome("C:\\bin\\chromedriver.exe")
driver.get("https://tsiauca.edupage.org/login/?msg=3")
driver.minimize_window()
driver.maximize_window()
driver.find_element_by_id("login_Login_1e1").send_keys(mail)
driver.find_element_by_id("login_Login_1e2").send_keys(password+"\n")
sleep(1)
driver.get("https://tsiauca.edupage.org/znamky/?")
sleep(1)
q(driver, ["i bar_mainDiv", "c edubarMainNoSkin", "t div", "c znamkyTable", "t tbody", "c znamkyViewerLoadOlderTd"]).click()
gs = sorted([(q(elem, ['t td', 't b']).text.split("\n")[0], round(sum([0]+[is_valid_tip(tip) for tip in q(elem, ['cs znZnamka'])]), 1)) for elem in q(driver, ["i bar_mainDiv", "c edubarMainNoSkin", "t div", "c znamkyTable", "t tbody", "cs predmetRow"])[1:]], key=lambda _:_[1], reverse=True)
gs = [g for g in gs if g[1]]
# gs = [(g[0], 100) for g in gs]
gs = [(g[0], g[1], grade(g[1]), dict(credit)[g[0].strip()]) for g in gs if g[1]>0]
length = 1+len(max(gs, key=lambda _:len(_[0]))[0])
with open("additional\\temporary.txt", mode="w", encoding="utf-8") as f: f.write("\n".join([f"{g[0].strip().ljust(length)}|{str(g[1]).ljust(6)}|{g[2].ljust(3)}|{g[3]}" for g in gs])+f"\n{'GPA'.ljust(length)}|{str(round((sum([grade_to_gpa[g[2]]*g[3] for g in gs])+8)/general_cred, 2)).ljust(6)}|{str(gpa_to_grade((sum([grade_to_gpa[g[2]]*g[3] for g in gs])+8)/general_cred)).ljust(3)}|{general_cred}")
driver.close()
o("additional\\temporary.txt")