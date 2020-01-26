#!/usr/bin/env python3

import random
import os
import argparse

#												FILE
signatures = [  b'%PDF-1.0\r\x0e',				#PDF
				b'%PDF-1.1\r\x0e',				#PDF
				b'%PDF-1.2\r\x0e',				#PDF
				b'%PDF-1.5\r\x0e',				#PDF
				b'%PDF-1.6\r\x0e',				#PDF
				b'%PDF-2.0\r\x0e',				#PDF
				b'RIFF\xff\xff\xff\xffWAVE',	#Waveform Audio
				b'RIFF\xff\xff\xff\xffAVI\x20', #AVI
				b"ID3",							#MP3
				b"ustar\x0000",					#TAR
				b"7z\xBC\xAF\x27\x1C",			#7zip
				b"SQLite format 3\x00",			#SQLite Database
				b"\xFF\xD8\xFF\xDB",			#JPEG
				b"\xFF\xD8\xFF\xE0\x00\x10\x4A\x46\x49\x46\x00\x01", #JPEG
				b"\xFF\xD8\xFF\xEE",			#JPEG
				b"\xFF\xD8\xFF\xE1\xff\xff\x45\x78\x69\x66\x00\x00", #JPEG
				b"\x89PNG\x0D\x0A\x1A\x0A"]		#PNG


def overwrite_partial(filename, sig_count, headerlength):
    length = os.stat(filename).st_size
    with open(filename, "br+", buffering=0) as file:
        print("Injecting bad magic codes into file %s" %(filename))
        print("Filesize: %d Bytes" %(length))
        print("Number of signatures: %d" %(sig_count))
        for i in range(sig_count):
            entrypoint = random.randint(0,length-1)
            entrypoint = entrypoint - (entrypoint % 4)
            signature = signatures[random.randint(0,len(signatures)-1)]
            print("\t\tInjecting signature at 0x%x + file offset" %(entrypoint))
            print("\t\t\tSignature:", end="")
            print(signature)
            file.seek(entrypoint)
            file.write(signature)
        file.seek(0)
        file.write(b"\x00" * headerlength)

def overwrite_random(filename):
    length = os.stat(filename).st_size
    print("Overwriting with random.")
    with open(filename, "br+", buffering=0) as file:
        file.seek(0)
        file.write(os.urandom(length))

def overwrite_zero(filename):
    length = os.stat(filename).st_size
    print("Overwriting with random.")
    with open(filename, "br+", buffering=0) as file:
        file.seek(0)
        file.write(b"\x00" * length)


def main():
    parser = argparse.ArgumentParser(
        description='Overwrite parts of a file with fake file signatures/magic codes.')
    parser.add_argument("file", help="File to overwrite")
    parser.add_argument("-s",type=int, help="Number of signatures to write into file.",default=20)
    parser.add_argument("--header",type=int, help="Length of header to overwrite with zeros.",default=0)
    parser.add_argument('--random', action='store_true', help="Overwrite file with random data first (not as safe as shred or srm!)")
    parser.add_argument('--zero', action='store_true', help="Overwrite file with zeros first (not as safe as shred or srm!)")
    args = parser.parse_args()
    print(args)
    if(args.zero):
        overwrite_zero(args.file)
    if(args.random):
        overwrite_random(args.file)
    overwrite_partial(args.file, args.s, args.header)


if __name__ == "__main__":
    main()
