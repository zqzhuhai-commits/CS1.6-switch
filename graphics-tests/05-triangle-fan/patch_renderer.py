"""Patch only the user's identified Switch renderer, retaining its ABI and layout."""
import argparse
import hashlib
import struct
from pathlib import Path

ORIGINAL_SHA256 = '500994445d4df4cd0628ac474a9fcc49d38f9370ebe5fd1ae3a15e9e9d250de9'
OUTPUT_SHA256 = '8d2574f7b17c970cb862061ba926da9511c5b7b9fe1be498a280ed6a849564d0'
# These are file offsets, not virtual addresses. Each instruction supplies
# GL_POLYGON (9) to pglBegin in a surface/lightmap drawing function.
OFFSETS = (176448, 196108, 197296, 197444, 197892)


def patch(data):
    if hashlib.sha256(data).hexdigest() != ORIGINAL_SHA256:
        raise ValueError('Input is not the exact supported reference libref_gl.so')
    result = bytearray(data)
    for offset in OFFSETS:
        if struct.unpack_from('<I', data, offset)[0] != 0x52800120:
            raise ValueError('Unexpected original ARM64 instruction')
        struct.pack_into('<I', result, offset, 0x528000c0)  # mov w0, #6
    result = bytes(result)
    if hashlib.sha256(result).hexdigest() != OUTPUT_SHA256:
        raise ValueError('Output digest mismatch')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('original', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.original.resolve() == args.output.resolve():
        raise ValueError('Keep the original file; choose a different output path')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(patch(args.original.read_bytes()))
    print('Patched five surface primitive arguments; output SHA-256 verified')
