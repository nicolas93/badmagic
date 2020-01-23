#!/usr/bin/env python3

import random
import os


signatures = [  b"\x25\x50\x44\x46\x2d\x31\x2e\x33\x0d\x0e",
				b"\x25\x50\x44\x46\x2d\x31\x2e\x34\x0d\x0e",
				b"\x25\x50\x44\x46\x2d\x31\x2e\x35\x0d\x0e",
				b"\x25\x50\x44\x46\x2d\x31\x2e\x36\x0d\x0e"]


def overwrite_partial(filename, sig_count):
    length = os.stat(filename).st_size
    with open(filename, "br+", buffering=0) as file:
        print("Injecting bad magic codes into file %s" %(filename))
        print("Filesize: %d Bytes" %(length))
        print("Number of signatures: %d" %(sig_count))
        for i in range(sig_count):
            entrypoint = random.randint(0,length)
            print("\t\tInjecting signature at 0x%x + file offset" %(entrypoint))
            file.seek(entrypoint)
            file.write(b"\x25\x50\x44\x46\x2d\x31\x2e\x30\x0d\x0e")
        file.seek(0)
        file.write(b"totalgarbage" *10)

overwrite_partial("/run/media/nicolas/4F7E-901C/sample.pdf", 100)