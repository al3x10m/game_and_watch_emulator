from .unicorn import *
from .mmu import hook_mem_read, hook_mem_write
from .hexfile_loader import read_hexfile
from sys import argv
import struct
import threading
from .gui import GUIThread
from queue import Queue

message_input_queue = Queue()
message_output_queue = Queue()

gui_thread = threading.Thread(target=GUIThread, args=(message_input_queue, message_output_queue))
gui_thread.start()

if len(argv) == 1:
    exit(1)

mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)

# peripherals
mu.mem_map(0x4001_0000, 0x8000)
mu.mem_map(0x4002_0000, 0x3400)
mu.mem_map(0x4004_0000, 0x4_0000)
mu.mem_map(0x4802_0000, 0x3000)
mu.mem_map(0x5000_1000, 0x3000)
mu.mem_map(0x5200_0000, 0xF000)
mu.mem_map(0x5800_0000, 0x7400)
mu.mem_map(0x5802_0000, 0x5C00)

# RAM
mu.mem_map(0x2400_0000, 0x10_0000)
mu.mem_map(0x3000_0000, 0x2_0000)
mu.mem_map(0x3800_0000, 0x1_0000)
mu.mem_map(0x0000_0000, 0x1_0000)
mu.mem_map(0x2000_0000, 0x2_0000)

# Flash
mu.mem_map(0x0800_0000, 0x2_0000)
mu.mem_map(0x1FF0_0000, 0x2_0000, perms=UC_PROT_READ)
mu.mem_map(0x9000_0000, 0x10_0000)

# Debug
mu.mem_map(0xE000_0000, 0x1_0000)

mu.hook_add(UC_HOOK_MEM_READ, hook_mem_read)
mu.hook_add(UC_HOOK_MEM_WRITE, hook_mem_write)

data = read_hexfile(argv[1])

for k, v in data.items():
    mu.mem_write(k, bytes(v))

mu.reg_write(arm_const.UC_ARM_REG_SP, struct.unpack("<l", data[0x0800_0000][0:4])[0])
try:
    mu.emu_start(struct.unpack("<l", data[0x0800_0000][4:8])[0], 0xFFFF_FFFF)
except Exception as e:
    print(e)
    print(f'PC: 0x{mu.reg_read(arm_const.UC_ARM_REG_PC):08X}')
    exit(0)