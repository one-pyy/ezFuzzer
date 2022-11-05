from typing import Dict

def header(s:str)->Dict[str,str]:
  ret: Dict[str,str]={}
  for line in s.split('\n'):
    if line:
      k,v=line.split(': ',1)
      ret[k]=v
  return ret

__all__=['header']

if __name__=='__main__':
  print(header("Content-Length: 1000\nX-Real-IP: 127.0.0.1"))
