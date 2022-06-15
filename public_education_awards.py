import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from time import sleep
bot = telebot.TeleBot("1978560750:AAGtA3SO8yh64VjS4hmVu23o_nNrRdSzj7A")
find_func ={"t":lambda e,p:e.find_element(By.TAG_NAME, p),
            "c":lambda e,p:e.find_element(By.CLASS_NAME, p),
            "i":lambda e,p:e.find_element(By.ID, p),
            "ts":lambda e,p:e.find_elements(By.TAG_NAME, p),
            "cs":lambda e,p:e.find_elements(By.CLASS_NAME, p)}
saturday = {"8:00":"8:00","9:20":"9:15","9:30":"9:25","10:50":"10:40","11:40":"10:50","13:00":"12:05","13.10":"12:45","14.30":"14:00","14.40":"14:10","16.00":"15:25","16.10":"15:35","17.30":"16:50","17.40":"17:00","19.00":"18:15","Пусто":"Пусто"}
def q(current, all_path):
  if not all_path: return current
  move_type, move_direction = all_path[0].split()
  return q(find_func[move_type](current, move_direction), all_path[1:])

def is_valid_tip(tip):
  if tip.find_element(By.XPATH,"..").get_attribute("original-title").lower().find("<br>")<0 and all(map(lambda _:_ not in "ABCDFP",tip.text)):
    return float(tip.text.split()[0])
  else: return 0
def answer(m,t):
  print(t)
  bot.send_message(m.chat.id, t)

grade_to_gpa = {"A": 4,"A-": 3.67,"B+": 3.33,"B": 3,"B-": 2.67,"C+": 2.33,"C": 2,"C-": 1.67,"D+": 1.33,"D": 1,"D-": 0.67,"F": 0}
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

def show(m, s, d):
  ss = "а"
  if float(dict(credit)[s]) == 1: ss = ""
  elif float(dict(credit)[s]) >= 5: ss = "ов"
  answer(m, f"Предмет \"{s.lower()}\" стоит {dict(credit)[s]} кредит{ss}. Вот за что тут можно получить баллы:")
  for p in d:
    a = p.split()
    a, b = " ".join(a[:-1]), a[-1]
    bot.send_message(m.chat.id, f"{a}:  {b}")

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

def check_sub(u):
  if u: return u[0]!="-"
  else: return False
with open("additional\\subjects.txt", "r", encoding="utf-8") as f: data = f.read().split("\n")
credit = [(data[sub], float(data[sub+1])) for sub in range(0, len(data), 2)]
general_cred = sum([sub[1] for sub in credit])
run = False


@bot.message_handler(commands=["start"])
def start(m):
  bot.send_message(m.chat.id, "Введите свою почту и пароль через пробел чтобы начать")

@bot.message_handler(commands=["i"])
def info(m):
  t = m.text[2:].strip()
  sub = [sub[0] for sub in credit]
  if t:
    if not t.isdigit(): answer(m, "Нормально введи")
    else:
      t = sub[int(t)-1]
      with open(f"additional\\{t}.txt", "r", encoding="utf-8") as f: show(m, t, f.read().split("\n"))
  else: bot.send_message(m.chat.id, "\n".join([f"{str(_+1)}) {sub[_]}" for _ in range(len(sub))]) + "\n(Например: /i 12)")

@bot.message_handler(content_types="document")
def gpa_from_document(m):
  if not m.document.file_name.lower().endswith(".txt"):
    answer(m, "введите txt файл")
    return 0
  with open("test.txt", "wb") as f: f.write(bot.download_file(bot.get_file(m.document.file_id).file_path))
  sleep(1)
  with open("test.txt", "r", encoding="utf-8") as f: data = f.read()
  data = [[d.strip() for d in sub.split("|")] for sub in data.split("\n")[:-1]]
  data = [(grade(float(sub[1])), float(sub[3])) for sub in data]
  answer(m, f"GPA: {round((sum([grade_to_gpa[sub[0]]*sub[1] for sub in data])+8)/general_cred, 2)}")

@bot.message_handler(content_types="text")
def e(m):
  global run
  print(m.text)
  t = m.text.strip()
  if run:
    answer(m, "Сейчас выполняется запрос другого человека, подождите и повторите попытку")
    return 0
  run = True
  try: name, password = t.split()
  except:
    answer(m, "Имя пользователя и пароль должны быть разделены пробелом")
    run = False
    return 0
  if name[:-8]=="@auca.kg": name = name[:-8]
  driver = webdriver.Chrome(service=Service("C:\\bin\\chromedriver.exe"), options=webdriver.ChromeOptions())
  driver.get("https://tsiauca.edupage.org/login/?msg=3")
  driver.minimize_window()
  driver.maximize_window()
  driver.find_element(By.ID, "login_Login_1e1").send_keys(f"{name}@auca.kg")
  driver.find_element(By.ID, "login_Login_1e2").send_keys(f"{password.strip()}\n")
  sleep(1)
  if q(driver, ["cs skgdFormInput"]):
    answer(m, "Неверно введён логин или пароль")
    driver.close()
    driver = []
    run = False
    return 0
  driver.get("https://tsiauca.edupage.org/dashboard/")
  sleep(1)
  tt_formated = "Расписание на сегодня:\n"
  for day in range(2):
    time_format = lambda time: f"{time[0]}-{time[1]}"
    if q(driver, ["c dashboard-header", "c header", "t span"]).text.split(",")[0].lower() == "сб":
      time_format = lambda time: f"{saturday[time[0]]}-{saturday[time[1]]}"
    timetable = q(driver, ["c dashboard-lessons", "ts div"])
    for tts in timetable:
      if not tts.get_attribute("class"):
        info = [(q(tts, ["cs pn"]), lambda string: f"{string}) " if string else ""),
        (q(tts, ["cs time"]), lambda string: f"({time_format(string.split())}) " if string else ""),
        (q(tts, ["cs subjects"]), lambda string: f"{string}, " if string else ""),
        (q(tts, ["cs classrooms"]), lambda string: f"Кабинет: {string}" if string else "")]
        for infos in info:
          if infos[0]:
            tt_formated += infos[1](infos[0][0].text.strip())
          else:
            tt_formated += infos[1]("")
        tt_formated += "\n"
    bot.send_message(m.chat.id, tt_formated)
    tt_formated = "Расписание на завтра:\n"
    if not day: q(driver, ["c next"]).click()
    sleep(0.5)
  driver.get("https://tsiauca.edupage.org/znamky/?")
  sleep(3)
  q(driver, ["i bar_mainDiv", "c edubarMainNoSkin", "t div", "c znamkyTable", "t tbody", "c znamkyViewerLoadOlderTd"]).click()
  gs = sorted([(q(elem, ['t td', 't b']).text.split("\n")[0], round(sum([0]+[float(tip.text.split()[0]) for tip in q(elem, ['cs znZnamka'])]), 1)) for elem in q(driver, ["i bar_mainDiv", "c edubarMainNoSkin", "t div", "c znamkyTable", "t tbody", "cs predmetRow"])[1:]], key=lambda _:_[1], reverse=True)
  gs = [g for g in gs if g[1]]
  # gs = [(g[0], 100) for g in gs]
  gs = [(g[0], g[1], grade(g[1]), dict(credit)[g[0].strip()]) for g in gs if g[1]>0]
  length = 1+len(max(gs, key=lambda _:len(_[0]))[0])
  with open(f"additional\\temporary.txt", mode="w", encoding="utf-8") as f: f.write("\n".join([f"{g[0].strip().ljust(length)}|{str(g[1]).ljust(6)}|{g[2].ljust(3)}|{g[3]}" for g in gs])+f"\n{'GPA'.ljust(length)}|{str(round((sum([grade_to_gpa[g[2]]*g[3] for g in gs])+8)/general_cred, 2)).ljust(6)}|{str(gpa_to_grade((sum([grade_to_gpa[g[2]]*g[3] for g in gs])+8)/general_cred)).ljust(3)}|{general_cred}")
  with open(f"additional\\temporary.txt", "rb") as f: bot.send_document(m.chat.id, f.read(), visible_file_name="grades.txt")
  with open(f"additional\\temporary.txt", mode="w", encoding="utf-8") as f:pass
  driver.close()
  driver = []
  run = False

bot.infinity_polling()