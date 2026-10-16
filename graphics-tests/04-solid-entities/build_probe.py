"""Build a separate BSP to isolate non-normal brush rendering; no engine edits."""
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path
from zipfile import ZipFile


def build(source):
    if struct.unpack_from('<i', source)[0] != 30:
        raise ValueError('Expected BSP version 30')
    offset, length = struct.unpack_from('<ii', source, 4)
    entities = source[offset:offset + length]
    result = bytearray(source)
    changes = []
    for entity in re.finditer(rb'\{[^{}]*\}', entities):
        fields = dict(re.findall(rb'"([^"]*)"\s*"([^"]*)"', entity[0]))
        if not fields.get(b'model', b'').startswith(b'*'):
            continue
        if fields.get(b'rendermode', b'0') == b'0':
            continue
        if float(fields.get(b'renderamt', b'0')) <= 0:
            continue  # preserve invisible brushes
        mode = re.search(rb'"rendermode"\s*"([1-5])"', entity[0])
        if mode is None:
            raise ValueError('Unexpected render mode')
        position = offset + entity.start() + mode.start(1)
        result[position] = ord('0')
        changes.append({'model': fields[b'model'].decode(),
                        'classname': fields[b'classname'].decode(),
                        'old_mode': mode[1].decode(), 'offset': position})
    output = bytes(result)
    assert len(output) == len(source)
    assert sum(a != b for a, b in zip(source, output)) == len(changes)
    assert output[:offset] == source[:offset]
    assert output[offset + length:] == source[offset + length:]
    for i in range(1, 15):
        start, size = struct.unpack_from('<ii', source, 4 + 8 * i)
        assert source[start:start + size] == output[start:start + size]
    report = {'source_sha256': hashlib.sha256(source).hexdigest(),
              'output_sha256': hashlib.sha256(output).hexdigest(),
              'changed_entity_count': len(changes), 'changes': changes,
              'validation': 'Same file size and BSP header; all 14 non-entity lumps byte-identical'}
    return output, report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('reference_zip', type=Path)
    parser.add_argument('output_directory', type=Path)
    args = parser.parse_args()
    with ZipFile(args.reference_zip) as archive:
        source = archive.read('switch/CS16/cstrike/maps/happyvalley_lt.bsp')
    output, report = build(source)
    args.output_directory.mkdir(parents=True, exist_ok=True)
    (args.output_directory / 'happyvalley_lt_solid.bsp').write_bytes(output)
    (args.output_directory / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'Built happyvalley_lt_solid.bsp; {len(report["changes"])} render-mode bytes changed')
