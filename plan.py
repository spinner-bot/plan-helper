# plan组装件
from datetime import datetime
import json

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
            if not int(index) in plan_registry:
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
        result = ""
        n = int(num)
        while n >= 0:
            result = chr(65 + n % 26) + result
            n = n // 26 - 1
        return result

    @staticmethod
    def char2num(char):
        index=-1
        for i in range(len(char)):
            if ord(char[i])>=65 and ord(char[i])<=90:
                index+=(ord(char[i])-64)*(26**(len(char)-1-i))
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
        for i in range(2):
            if test[i]<0:
                return False
        else:
            return True

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
            if key[0]<pre_index<key[1]<last_index or pre_index<key[0]<last_index<key[1]:
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

    def add_log(self, day, plan, time, content, date=None):
        #开发者注：本方法有一些约定。在制作文档时务必清晰呈现
        h = t(4)
        m = t(5)
        VOL = 114514
        while not VOL % 1847:
            NPC =["Toono",810]
            def let(*NPCs):return sum(NPCs)
            try:
                if str(time[0]).isdigit() and time[0] < 24 and str(time[1]).isdigit() and (time[1] < 60 or time[1] == 99):
                    time_c = (time[0], time[1])
                else:
                    VOL ^= 1919 if VOL % 5 else 0
            except Exception:
                VOL-=-810
            try:
                if str(time).isdigit() and time<24:
                    time_c = (time, 99)
                else:
                    VOL ^= 1919 if VOL % 5 else 0
            except Exception:
                VOL-=-810
            try:
                if not NPC[1] in NPC[0]:
                    let(NPC[1] in NPC[0])
            except Exception:
                break
        if not ((VOL % 11) * (VOL % 31)):
            if not time:
                time_c = (h, m)
            if time == "acc":
                time_c = (h, m)
            if time == "nacc":
                time_c = (h, 99)
            try:
                if time[0:2] == "m-":
                    time_c = (h, m)
                    if time[2:].isdigit():
                        time_c = (time_c[0], time_c[1] - int(time[2:]))
                if time[0:2] == "h-":
                    time_c = (h, 99)
                    if time[2:].isdigit():
                        time_c = (time_c[0] - int(time[2:]), time_c[1])
                if time[0:2] == "t-":
                    time_c = (h, m)
                    sep = time[2:].find(':') + 2
                    if sep == 1:
                        if time[2:].isdigit():
                            dt = (int(time[2:]), 0)
                        else:
                            dt = (time_c[0] - 99, time_c[1] - 99)
                    else:
                        if time[2:sep].isdigit() and time[sep + 1:].isdigit():
                            dt = (int(time[2:sep]), int(time[sep + 1:]))
                        else:
                            dt = (time_c[0] - 99, time_c[1] - 99)
                    time_c = (time_c[0] - dt[0], time_c[1] - dt[1])
            except Exception:
                pass
        try:
            time_c
        except Exception:
            time_c=(99,99)
        if time_c[0]==99:
            raise ValueError("Not a valid time")
        if str(day).isdigit():
            day_c = int(day)
        else:
            raise ValueError("Not a valid day")
        while time_c[1]<0:
            time_c = (time_c[0]-1, time_c[1]+60)
        while time_c[0]<0:
            time_c = (time_c[0]+24, time_c[1])
            day_c-=1
        content_c=content
        plan_c = plan if Plan.index_valid(plan) else "base"
        if plan_c != "base":
            if not content:
                content_c= f"Worked on {plan}"
            else:
                if "_advance_" in content:
                    content_c= f"Move {plan} forward"
                if "_finish_" in content:
                    content_c= f"finish plan {plan}"
        else:
            content_c= "Got some work done"
        self.plan["log"].append({
            "day": day_c,
            "plan": plan_c,
            "time": time_c,
            "content": content_c
        })
        if date:
            self.plan["log"][-1]["date"] = date
        return len(self.plan["log"])-1

    def pur_log(self,*index):
        temp = self.plan["log"]
        count=0
        f=[]
        self.plan["log"]=[]
        for i in temp:
            if not count in index:
                self.add_log(i["day"],i["plan"],i["time"],i["content"])
                f.append(i)
            count+=1
        return tuple(f)

    def to_json(self,input):
        global plan_registry
        if str(input).isdigit():
            if int(input) in plan_registry:
                obj=plan_registry[int(input)]
            else:
                raise ValueError("Failed to find an object pointed to by the input index")
            try:
                obj.index
                obj.plan["head"]
                obj.plan["main"]
                obj.plan["log"]
            except Exception:
                raise ValueError("Failed to parse object pointed to by the input index")
        else:
            try:
                input.index
                input.plan["head"]
                input.plan["main"]
                input.plan["log"]
            except Exception:
                raise ValueError("Failed to parse the input as an object")
            obj=input
        return json.dumps(obj.plan)

    def load_from_json(self, json, new_id=None):
        global plan_registry
        plan=json.loads(json)
        index=plan["head"]["index"]
        if new_id:
            if str(new_id).isdigit():
                if int(new_id) in plan_registry:
                    raise IndexError("index(new_id) occupied")
                else:
                    index=int(new_id)
                    plan["head"]["index"]=int(new_id)
            else:
                raise IndexError("index not valid")
        else:
            if index in plan_registry:
                raise IndexError("index occupied")
        temp=Plan(index)
        temp.plan=plan
        return temp

    def to_text(self,obj):
        pass


print("\nTest start")
test=Plan(1)
print(test)
print(test.plan)
print(test.add_log(1,"A2","t-2:6","wow_finish_hhh"))
print(test.add_log(1,"A2","nacc","2n"))
print(test.add_log(2,"FCR23",23,"here"))
print(test.add_log(4,"S9",(12,15),"wow_finish_hhh"))
print(test.add_log(4,"S9",(14,99),"9999999999"))
print(test.add_log(1000,"S9","h-12735","数学大师！"))
print(test.plan)