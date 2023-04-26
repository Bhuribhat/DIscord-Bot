import os

TOKEN = os.environ['TOKEN']

# variable
words    = ['ว่าไง', 'มา', 'เหงา', 'หิว', 'ง่วง', 'โหล', 'เอาเลย', 'ดี']
interact = ['โอ้ววว', 'ไงเงา', 'ฝันดีน้า', 'เยลโล่ว', 'อู้วววววว']

schedule = {
    "monday":    "13.00 - 16.00 PM : [Computer Vision](https://www.mycourseville.com/?q=courseville/course/32214)\n"\
                 "13.00 - 16.00 PM : [Neural Network](https://sites.google.com/view/ssukree/courses/2110571-neural-network-22022?authuser=0)",
    "tuesday":   "08.00 - 09.30 AM : [Software Eng II](https://www.mycourseville.com/?q=courseville/course/32207)\n"\
                 "09.30 - 12.30 AM : [OS Sys Prog](https://www.mycourseville.com/?q=courseville/course/32203)\n"\
                 "13.00 - 16.00 PM : [Data Sci/Eng](https://www.mycourseville.com/?q=courseville/course/32215)",
    "wednesday": "09.00 - 12.00 AM : [Comp Network I](https://www.mycourseville.com/?q=courseville/course/32216)",
    "thursday":  "08.00 - 09.30 AM : [Software Eng II](https://www.mycourseville.com/?q=courseville/course/32207)",
    "friday":    "09.00 - 12.00 AM : [Tech Writing Eng](https://sites.google.com/view/5500308-s12-s2-22/home)"
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
