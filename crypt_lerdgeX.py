#!/usr/bin/env python3
import argparse
import os
import struct

def lerdge_encrypt_byte(byte):
    byte = 0xFF & ((byte << 6) | (byte >> 2))
    i = 0x58 + byte
    j = 0x05 + byte + (i >> 8)
    byte = (0xF8 & i) | (0x07 & j)
    return byte

def lerdge_encrypt(source, output_directory, target):
    firmware = open(source, "rb")
    update = open(output_directory + target, "wb")
 
    input = bytearray(firmware.read())
    for i in range(len(input)):
        b = input[i]
        b = lerdge_encrypt_byte(b)
        input[i] = b

    update.write(input)
    firmware.close()
    update.close()


sourceFile = "klipper/out/klipper.bin"
outputDirectory = "."

print ("Encrypt " + sourceFile + " " + "to " + outputDirectory)
lerdge_encrypt(sourceFile, outputDirectory, '/Lerdge_X_firmware_force.bin')
