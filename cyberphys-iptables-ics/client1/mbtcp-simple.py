#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# read_register (Python 3 version)
# read 10 registers and print result on stdout
# you can use the tiny modbus server "mbserverd" to test this code
# mbserverd is here: https://github.com/sourceperl/mbserverd
# the command line modbus client mbtget can also be useful
# mbtget is here: https://github.com/sourceperl/mbtget
# This code was adapted from the example code for pyModbusTCP
# (https://github.com/sourceperl/pyModbusTCP)
# Specifically, write_bit.py and read_register.py
#
# Yêu cầu: pip install pyModbusTCP (bản mới, hỗ trợ Python 3)

from pyModbusTCP.client import ModbusClient
import time

SERVER_HOST = "172.25.0.3"
# SERVER_HOST = "172.17.0.2"
SERVER_PORT = 502

# Trong các phiên bản pyModbusTCP mới, host/port được truyền
# trực tiếp vào constructor thay vì gọi c.host()/c.port()
c = ModbusClient(host=SERVER_HOST, port=SERVER_PORT, auto_open=True)

# bật debug nếu cần
# c.debug = True

toggle = True

while True:
    # mở hoặc kết nối lại TCP tới server (nếu auto_open=True thì
    # pyModbusTCP sẽ tự làm việc này, nhưng ta vẫn kiểm tra để log rõ ràng)
    if not c.is_open:
        if not c.open():
            print("unable to connect to {}:{}".format(SERVER_HOST, SERVER_PORT))

    # nếu kết nối ok, đọc thanh ghi (modbus function 0x03)
    if c.is_open:
        print("")
        print("read 10 holding registers")
        print("----------")
        print("")
        # đọc 10 thanh ghi tại địa chỉ 0, lưu kết quả vào regs
        regs = c.read_holding_registers(0, 10)
        # nếu thành công thì hiển thị
        if regs:
            print("reg ad #0 to 9: {}".format(regs))
        else:
            print("unable to read holding registers")

    # nếu kết nối ok, ghi coils (modbus function 0x01)
    if c.is_open:
        print("")
        print("write bits")
        print("----------")
        print("")
        for addr in range(4):
            is_ok = c.write_single_coil(addr, toggle)
            if is_ok:
                print("bit #{}: write to {}".format(addr, toggle))
            else:
                print("bit #{}: unable to write {}".format(addr, toggle))
            time.sleep(0.5)

        time.sleep(1)

        print("")
        print("read bits")
        print("---------")
        print("")
        bits = c.read_coils(0, 4)
        if bits:
            print("bits #0 to 3: {}".format(bits))
        else:
            print("unable to read")

    toggle = not toggle
    # nghỉ 2s trước lần polling tiếp theo
    time.sleep(2)
