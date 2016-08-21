import time
import random

__POSSIBLE_CHARS_IN_RANDOM_STR = "abcdefghijklmnopqrstuvwxyz0123456789"

def GetRandomStr(in_len, in_possible_chars = __POSSIBLE_CHARS_IN_RANDOM_STR):
  "@return A random string that is limited to 'in_possible_chars' of length 'in_len'."
  random.seed(time.time())
  randomStr = ""
  while len(randomStr) < in_len:
    randomStr += in_possible_chars[random.randint(0,len(in_possible_chars)-1)]
  return randomStr

if __name__ == "__main__":
  assert GetRandomStr(500,'a') == 'a'*500
  assert GetRandomStr(5000,__POSSIBLE_CHARS_IN_RANDOM_STR[:-1]).find('9') == -1
