#
# Usage for the Linux kernel:
#
#   $ make [ARCH=<arch>] scriptconfig SCRIPT=/path/to/this.py

import sys
import random
hash  =   {'ANDROID': 'n', 'MMU': 'y', 'PREEMPT': 'y', 'FB': 'n'}


from kconfiglib import Kconfig, Symbol



def do_addconstraints(node):
  
    # Walk the tree of menu nodes. You can imagine this as going down/into menu
    # entries in the menuconfig interface, setting each to n (or the lowest
    # assignable value).

    while node:
        if isinstance(node.item, Symbol):
            sym = node.item

            if sym.name in hash and sym.assignable:
                val = hash[sym.name]
                if val == 'y':
                    if 2 in sym.assignable:
                        sym.set_value(2)
                    else:
                        print("Warning: " + sym.name  + "is assignable, but can't be set to 'y' ")
                if val == 'n':
                    if 0 in sym.assignable:
                        sym.set_value(0)
                        print("Warning: " +sym.name  + "is assignable, but can't be set to 'n' ")
                    else:
                        print("could not set " + sym.name)
            if sym.name in hash and not sym.assignable:
                print("Warning: " + sym.name + "is not assignable" )

        # Recursively visit children
        if node.list:
            do_addconstraints(node.list)

        node = node.next

def do_randomconfigs(node):
  
    # Walk the tree of menu nodes. You can imagine this as going down/into menu
    # entries in the menuconfig interface, setting each to n (or the lowest
    # assignable value).
   
    while node:
       
        if isinstance(node.item, Symbol):
            sym = node.item
            if sym.name in hash:
                pass
                ## verify its what we want here
            else:
                if sym.assignable:
                    val = random.choice(sym.assignable) # sym.assignable is a tuple of what we
                    sym.set_value(val)                  # can assign to this sym, so just pick a random one
        # Recursively visit children
        if node.list:
            do_randomconfigs(node.list)

        node = node.next

# Parse the Kconfig files
kconf = Kconfig(sys.argv[1])
do_addconstraints(kconf.top_node)
do_randomconfigs(kconf.top_node)


print(kconf.write_config())
