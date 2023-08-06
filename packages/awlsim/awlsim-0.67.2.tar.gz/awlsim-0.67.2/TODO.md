# Incomplete awlsim TODO list

## S7 compatibility

* Add feature: Parsing of attributes

## core

* Improve performance (cython)
* Blocks that are no longer linked to (created by) sources should be removed.
* Single download of symtab causes a redefinition error.
* Add feature: LAD (KOP) compiler

## AWL / STL optimizer

* Add optimization pass: O(UU)O(UU) -> UUOUU
* Add optimization pass: U(UU)= -> UU=  (also for other insn types)
* Add optimization pass: Reordering of TEMP variables for space packing

## GUI

* Add feature: Save window status (open MDI windows, positions, etc)
* Add feature: LAD (KOP) editor

## FBD/FUP GUI only

* Add feature: Exchange elements
* Add feature: Live view of signal states (online diagnosis)
* Add feature: Support modifying wires by clicking onto them

## FBD/FUP compiler and GUI

* Fix evaluation order in case of multiple parallel assignments and other elements
* Add feature: Add option to disable elements
* Add element: Timers
* Add element: CALL
