"""Emulate the new AArch64 hook, mocking only the four existing libc calls."""
from pathlib import Path
import sys
from unicorn import Uc, UC_ARCH_ARM64, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm64_const import *
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
b=Path(sys.argv[1]).read_bytes()
for failure in [False,True]:
    u=Uc(UC_ARCH_ARM64,UC_MODE_ARM)
    u.mem_map(0,0xb00000);u.mem_write(0,b)
    u.mem_map(0x1000000,0x20000);u.mem_map(0x2000000,0x1000)
    msg=b'CS16 logging hook test: resource lookup failed\n';msgptr=0x2000000
    u.mem_write(msgptr,msg+b'\0')
    sp=0x101f000;u.reg_write(UC_ARM64_REG_SP,sp)
    u.reg_write(UC_ARM64_REG_X0,msgptr)
    expected={UC_ARM64_REG_X19:0x12345678,UC_ARM64_REG_X20:0xabcdef01,UC_ARM64_REG_X29:0x87654321}
    for r,v in expected.items():u.reg_write(r,v)
    events=[]
    def cstring(ptr):
        x=bytearray()
        while (v:=bytes(u.mem_read(ptr+len(x),1)))!=b'\0':x.extend(v)
        return bytes(x)
    def hook(uc,address,size,unused):
        if address==0x7079a0:
            assert cstring(uc.reg_read(UC_ARM64_REG_X0))==b'sdmc:/CS16-debug.log'
            assert cstring(uc.reg_read(UC_ARM64_REG_X1))==b'a'
            events.append('fopen');uc.reg_write(UC_ARM64_REG_X0,0 if failure else 0x4000000)
        elif address==0x70ff24:
            assert cstring(uc.reg_read(UC_ARM64_REG_X0))==msg
            events.append('strlen');uc.reg_write(UC_ARM64_REG_X0,len(msg))
        elif address==0x709258:
            assert uc.reg_read(UC_ARM64_REG_X0)==msgptr
            assert uc.reg_read(UC_ARM64_REG_X1)==1
            assert uc.reg_read(UC_ARM64_REG_X2)==len(msg)
            assert uc.reg_read(UC_ARM64_REG_X3)==0x4000000
            events.append('fwrite');uc.reg_write(UC_ARM64_REG_X0,len(msg))
        elif address==0x706e70:
            assert uc.reg_read(UC_ARM64_REG_X0)==0x4000000
            events.append('fclose');uc.reg_write(UC_ARM64_REG_X0,0)
        elif address==0x33e00:
            assert uc.reg_read(UC_ARM64_REG_X0)==msgptr
            assert uc.reg_read(UC_ARM64_REG_SP)==sp
            assert uc.reg_read(UC_ARM64_REG_X30)==0x1eb50
            for r,v in expected.items():assert uc.reg_read(r)==v
            events.append('original_Sys_PrintLog');uc.emu_stop();return
        else:return
        assert uc.reg_read(UC_ARM64_REG_SP)%16==0
        uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_X30))
    u.hook_add(UC_HOOK_CODE,hook)
    u.emu_start(0x1eb4c,0x1eb50,count=200)
    assert events==(['fopen','original_Sys_PrintLog'] if failure else ['fopen','strlen','fwrite','fclose','original_Sys_PrintLog']),events
    print('PASS:', 'file-open failure safely falls back' if failure else 'append, close, preserve registers and resume original output')
for x in Cs(CS_ARCH_ARM64,CS_MODE_ARM).disasm(b[0x730f50:0x730f50+88],0x730f50):
    print(f'{x.address:08x}: {x.mnemonic} {x.op_str}')
