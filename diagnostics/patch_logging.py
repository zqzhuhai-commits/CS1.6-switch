#!/usr/bin/env python3
"""Add an append-and-close log hook to one checksum-pinned Switch NRO.
The patch uses existing newlib fopen/strlen/fwrite/fclose, not engine log init.
"""
from pathlib import Path
import hashlib, struct, json, sys
SRC = Path(sys.argv[1])
DST = Path(sys.argv[2])
b = bytearray(SRC.read_bytes())
# Pin the complete executable segment, allowing NACP/icon metadata differences.
text_size = 0x731000
expected_text_sha = '89765d1c1bfed8468b9a616a2c6b347b495f6e703cd2344bb423c20612f21a22'
assert b[0x10:0x14] == b'NRO0'
assert struct.unpack_from('<IIII', b, 0x20) == (0, text_size, text_size, 0x30f000)
assert hashlib.sha256(b[:text_size]).hexdigest() == expected_text_sha, 'unexpected engine code'
site = 0x1eb4c
stub = 0x730f50
original_printlog = 0x33e00
fopen, strlen, fwrite, fclose = 0x7079a0, 0x70ff24, 0x709258, 0x706e70

def branch(pc, target, link=False):
    delta = target-pc
    assert delta % 4 == 0 and -(1<<27) <= delta < (1<<27)
    return (0x94000000 if link else 0x14000000) | ((delta//4) & 0x3ffffff)

def adr(pc, target, rd):
    delta = target-pc
    assert -(1<<20) <= delta < (1<<20)
    return 0x10000000 | ((delta & 3)<<29) | (((delta>>2)&0x7ffff)<<5) | rd

def cbz(pc, target, rt):
    delta = target-pc
    assert delta%4==0 and -(1<<20)<=delta<(1<<20)
    return 0xb4000000 | (((delta//4)&0x7ffff)<<5) | rt

# x0 = message, x19/x20 and x29/x30 saved, SP stays 16-byte aligned.
words = [
    0xa9be7bfd, # stp x29,x30,[sp,#-32]!
    0x910003fd, # mov x29,sp
    0xa90153f3, # stp x19,x20,[sp,#16]
    0xaa0003f3, # mov x19,x0
    0,          # adr x0,path
    0,          # adr x1,mode
    0,          # bl fopen
    0,          # cbz x0,done
    0xaa0003f4, # mov x20,x0
    0xaa1303e0, # mov x0,x19
    0,          # bl strlen
    0xaa0003e2, # mov x2,x0
    0xaa1303e0, # mov x0,x19
    0xd2800021, # mov x1,#1
    0xaa1403e3, # mov x3,x20
    0,          # bl fwrite
    0xaa1403e0, # mov x0,x20
    0,          # bl fclose
    0xaa1303e0, # done: mov x0,x19
    0xa94153f3, # ldp x19,x20,[sp,#16]
    0xa8c27bfd, # ldp x29,x30,[sp],#32
    0,          # b original Sys_PrintLog
]
path = b'sdmc:/CS16-debug.log\0'
mode = b'a\0'
path_addr = stub+len(words)*4
mode_addr = path_addr+len(path)
words[4]=adr(stub+4*4,path_addr,0)
words[5]=adr(stub+5*4,mode_addr,1)
words[6]=branch(stub+6*4,fopen,True)
words[7]=cbz(stub+7*4,stub+18*4,0)
words[10]=branch(stub+10*4,strlen,True)
words[15]=branch(stub+15*4,fwrite,True)
words[17]=branch(stub+17*4,fclose,True)
words[21]=branch(stub+21*4,original_printlog)
payload=struct.pack('<'+'I'*len(words),*words)+path+mode
assert stub+len(payload)<=text_size
assert not any(b[stub:stub+len(payload)]), 'code cave not empty'
original=b[site:site+4]
assert struct.unpack('<I',original)[0]==branch(site,original_printlog,True)
b[stub:stub+len(payload)]=payload
b[site:site+4]=struct.pack('<I',branch(site,stub,True))
DST.parent.mkdir(parents=True,exist_ok=True)
DST.write_bytes(b)
manifest={'input_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(b).hexdigest(),'log_path':path[:-1].decode(),'hook_site':hex(site),'hook_stub':hex(stub),'stub_size':len(payload),'original_instruction':original.hex(),'patched_instruction':b[site:site+4].hex(),'type':'diagnostic logging only, not a confirmed crash fix'}
DST.with_suffix('.patch.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(manifest,indent=2))
