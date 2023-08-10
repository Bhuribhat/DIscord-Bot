import os
import numpy as np

TOKEN = os.environ['TOKEN']
CP_DOCS = "https://docs.google.com/document/d/1C1sF4aS6kFjqWBtU91vSYUvTSxdh9xxXhA9LeUUTbXg/edit#heading=h.8sb6c0hcl62a"

# variable
words    = ['ว่าไง', 'มา', 'เหงา', 'หิว', 'ง่วง', 'โหล', 'เอาเลย', 'ดี']
interact = ['โอ้ววว', 'ไงเงา', 'ฝันดีน้า', 'เยลโล่ว', 'อู้วววววว']

schedule = {
    "monday":       "09.00 AM - 12.00 AM : [Software Define System](https://www.mycourseville.com/?q=courseville/course/35359)\n"\
                    "01.00 PM - 04.00 PM : [Introduction to Japan Literature](https://www.mycourseville.com/?q=courseville/course/35549)",
    "tuesday":      "10.00 AM - 07.00 PM : [Capstone Chatbot](https://chula.zoom.us/j/97160899950?pwd=eW1pdm9ablcwSno3dUNtbU9ITjFNUT09)",
    "wednesday":    "10.00 AM - 07.00 PM : [Capstone Chatbot](https://chula.zoom.us/j/97160899950?pwd=eW1pdm9ablcwSno3dUNtbU9ITjFNUT09)",
    "thursday":     "01.00 PM - 04.00 PM : [Parallel and Distributed Systems](https://www.mycourseville.com/?q=courseville/course/35354)",
    "friday":       "09.00 AM - 12.00 AM : [Artificial Intelligence II](https://sites.google.com/view/ssukree/courses/2110477-artificial-intelligence-12022)",
}

# function to get min/max point
def getMinPoint(data):
    count = 0
    min_data = np.min(data["b"])
    for point in data['b']:
        if point != min_data:
            count += 1
        else:
            break
    return (count, round(min_data))


def getMaxPoint(data):
    count = 0
    max_data = np.max(data["b"])
    for point in data['b']:
        if point != max_data:
            count += 1
        else:
            break
    return (count, round(max_data))


# check if number don't have decimal
def is_integer_num(number):
    if isinstance(number, int):     # 1 = True
        return True
    if isinstance(number, float):   # 1.0 = True
        return number.is_integer()
    return False


# Convert any number (base 10) to any base
def numberToBase(number, base):
    if number == 0:
        return [0]
    digits = []
    while number:
        digits.append(int(number % base))
        number //= base
    return digits[::-1]


# convert number from any base to any another base
def numberAnyBase(number, current_base=10, result_base=2):
    base_10 = int(str(number), current_base)
    result = numberToBase(base_10, result_base)
    return "".join(str(number) for number in result)
