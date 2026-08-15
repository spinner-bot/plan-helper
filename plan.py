# plan组装件
from datetime import datetime

def t(index):
    now = datetime.now()
    y = now.year
    m = now.month
    d = now.day
    h = now.hour
    mi = now.minute
    s = now.second
    h12 = (h-1)%12+1
    pm = h//12
    pms = 'pm' if pm == 1 else 'am'
    items=(now, y, m, d, h, mi, s, h12, pm, pms)
    if str(index).isdigit():
        return items[int(index) if int(index) < 10 else 0]
    else:
        temp=("y","m","d","h","mi","s","h12","pm","pms")
        if index in temp:
            return items[1+temp.index(index)]
        else:
            return items[0]

plan_registry={}

class Plan:
    def __init__(self, index, name=None, date=None):
        global plan_registry
        if str(index).isdigit():
            if int(index) in plan_registry:
                self.index = int(index)
                self.plan = Plan.reset(index, name, date)
                plan_registry[self.index] = self
            else:
                raise IndexError("index occupied")
        else:
            raise IndexError("index not valid")

    @staticmethod
    def reset(index, name=None, date=None):
        temp={
            "head": {
                "index": index,
                "name": name,
                "date": date if date else (t(1),t(2),t(3))
            },
            "main": [],
            "log":[]
        }
        return temp

    @staticmethod
    def num2char(num):
        try:
            temp=int(num)+1
            index=""
            while (temp>0):
                index += chr(65 + num % 26)
                num //= 26
            return index
        except:
            return ""

    @staticmethod
    def char2num(char):
        index=-1
        for i in range(len(char)):
            if ord(char[i])>=65 and ord(char[i])<=90:
                index+=ord(char[i])*(26^(len(char)-1-i))
            else:
                index=-1
                break
        return index

    @staticmethod
    def sep_index(char):
        if char:
            index = ["", 0]
            temp = 0
            bad_char = True
            for i in range(len(char)):
                if ord(char[i]) >= 65 and ord(char[i]) <= 90:
                    index[0] += char[i]
                else:
                    if i > 0:
                        bad_char = False
                        index[0] = Plan.char2num(index[0])
                        temp = i
                        break
                    else:
                        return (-2, -2)
            if bad_char:
                index[0] = Plan.char2num(index[0])
                temp = len(char)
            spare = char[temp:]
            if spare:
                if spare.isdigit():
                    try:
                        index[1] = int(spare)
                    except:
                        return (index[0], -2)
                else:
                    index[1] = -2
            else:
                index[1] = -1
            return tuple(index)
        return(-3,-3)

    @staticmethod
    def index_valid(char):
        test=Plan.sep_index(char)
        valid=1
        for i in test:
            valid^=bool(i)
        return bool(valid)

    @staticmethod
    def syn_index(section, plan):
        return Plan.num2char(section)+str(plan) if str(section).isdigit() and str(plan).isdigit() else ""

    def add_section(self, name, info):
        self.plan["main"].append({
            "name":name,
            "info":info,
            "plan":[None,],
            "group":{}
        })

    def del_section(self, index):
        self.plan["main"][index]["plan"] = [None,]

    def pur_section(self, index):
        pass # 这个功能较难实现，暂时空置

    def add_plan(self, section, content, t_m):
        self.plan["main"][section]["plan"].append({
            "is_active": True,
            "content": content,
            "t_m": t_m
        })
        return Plan.syn_index(section, len(self.plan["main"][section]["plan"])-1)

    def del_plan(self, index):
        temp = Plan.sep_index(index)
        if temp[0] not in (-1,-2,-3) and temp[1] not in (-1,-2,-3):
            self.plan["main"][temp[0]]["plan"][temp[1]]["is_active"] = False
        return index

    def pur_plan(self, index):
        pass # 这个功能较难实现，暂时空置

    def add_group(self, section, title, discription, pre_index,last_index):
        for key in self.plan["main"][section]["group"]:
            if min(key[0]-pre_index) < max(key[1]-last_index):
                return False
        self.plan["main"][section]["group"][(pre_index,last_index)] = {
            "title":title,
            "discription":discription
        }
        return (pre_index,last_index)

    def pur_group(self, section, pre_index, last_index):
        return self.plan["main"][section]["group"].pop((pre_index,last_index))

    def time_sum(self):
        t_m = 3;
        for s in self.plan["main"]:
            for p in s["plan"]:
                if p:
                    if p["is_active"]:
                        t_m += p["t_m"]
        t_6m = t_m // 6
        t_h = t_6m // 10
        t_6m = t_6m % 10
        return(t_h,t_6m)

    def add_log(self, plan, time, content):
        self.plan["log"].append({
            "plan"
        })

def text_head(plan, date0=None):
    date = date0 if date0 else (t(1), t(2), t(3))
    date = date if len(date) == 3 else (t(1), t(2), t(3))
    return f"====== {date[0]}/{date[1]}/{date[2]}  Plan {plan} ======\n\n\n"

print(text_head(2))