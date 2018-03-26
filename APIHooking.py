import utils
import sys
from pydbg import *
from pydbg.defines import *

dbg = pydbg()
find_process = False

org_pattern = "love"
rep_pattern = "hate"

process_name = "notepad.exe"


def callback_function(dbg, args):
    process_buffer = dbg.read_process_memory(args[1], args[2])

    if org_pattern in process_buffer:
        print "[APIHooking] Before : %s" % process_buffer
        process_buffer = process_buffer.replace(org_pattern, rep_pattern)
        replace = dbg.write_process_memory(args[1], process_buffer)
        print "[APIHooking] After : %s" % dbg.read_process_memory(args[1], args[2])

    return DBG_CONTINUE


for (cur_pid, cur_name) in dbg.enumerate_processes():
    if cur_name.lower() == process_name:
        find_process = True
        hooks = utils.hook_container()

        dbg.attach(cur_pid)

        print "Saves a process handle in self.h_process of pid[%d]" % cur_pid

        hookAddress = dbg.func_resolve_debuggee("kernel32.dll", "WriteFile")

        if hookAddress:
            hooks.add(dbg, hookAddress, 5, callback_function, None)
            print "sets a breakpoint at the designated address : 0x%08x" % hookAddress
            break
        else:
            print "[Error] : couldn't resolve hook address"
            sys.exit(-1)


if find_process:
    print "waiting for occurring debugger event"
    dbg.run()

else:
    print "[Error] : there is no process [%s]" % process_name
    sys.exit(-1)

