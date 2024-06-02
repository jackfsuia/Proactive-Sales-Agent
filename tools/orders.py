import re
import datetime
def extract_order_string(text):
    pattern = r"<[^<>]+><[^<>]+><[^<>]+><[^<>]+><[^<>]+>"

    match = re.search(pattern, text)

    if match:
        return match.group(0)
    else:
        return None

def order_check(order_string):
    if order_string is None:
        return False
    info_pattern = re.compile(r'<([^<>]+)>')
    matches = info_pattern.findall(order_string)
    digit_pattern = r'\d'
    if re.search(digit_pattern, matches[2]) and re.search(digit_pattern, matches[3]) and re.search(digit_pattern, matches[4]):
        return True
    return False


def print_order(collected_messages):
    order_string = extract_order_string(collected_messages)
    if order_check(order_string):
        order_time = str(datetime.datetime.now())
        print(f"{order_time} {order_string}")
