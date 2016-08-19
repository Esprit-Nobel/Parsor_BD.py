# -*- coding: utf-8 -*-
"""
@author: Yannick NAMOUR
@date  : 04/2016

Deleting the lines of the treated file which are present in the files of
reference, writing of the duplicate entries in a file and doing some statistical
calculus on the seventh column.

IN  : >=2 file_to_filtrate first_ref  second_ref
OUT : 3 filtered_file, file with the duplicate entries and
statistics of the seventh column

COMMANDE TYPE : python Parsor_BD.py file_to_filtrate first_ref second_ref

"""
#import
from __future__ import print_function #pour assurer la compatibilité Python 2/3
import sys
import os
#
import logging
logging.basicConfig(filename='log_Parsor_BD.txt', \
    format="%(asctime)s-- %(name)s -- %(levelname)s:%(message)s'", \
    level=logging.DEBUG)
#
import argparse
PARSING = argparse.ArgumentParser(description="Deleting the lines of the \
    treated file which are present in the files of reference,writing of the \
    duplicate entries in a file and doing some statistical calculus on the \
    seventh column.", epilog="Release of 16 APR 2016")
PARSING.add_argument("initial_file", help="file to filter")
PARSING.add_argument("ref_files", nargs="+", help="reference files")
PARSING.add_argument("--version", action='version', version="%(prog)s 1.0")
ARGUMENTS = PARSING.parse_args()
#
print ("START Parsor_BD.py on", ARGUMENTS.initial_file, file=sys.stdout)
print (os.uname(), file=sys.stdout)
print ("---------------------------------------", file=sys.stdout)
logging.debug(os.uname())
logging.debug("START Parsor_BD.py on %s", ARGUMENTS.initial_file)
#
#----------------------------------------------------------------------------
#start reading initial file
with open(ARGUMENTS.initial_file, "r") as FILE_I:
    CONTENT_I = FILE_I.readlines()
#
DIC_I = {}
for NUMBER, LINE in enumerate(CONTENT_I): #dictionary with NUMBERted entries
    if not LINE.startswith("#"):
        DEC = LINE.split("\t", 2)
        HEAD = DEC[0] + DEC[1]
        DIC_I[NUMBER] = HEAD
    else:
        DIC_I[NUMBER] = LINE
    del NUMBER, LINE
print ("reading initial_file : ", ARGUMENTS.initial_file, file=sys.stdout)
logging.debug("reading initial_file : %s", ARGUMENTS.initial_file)
#
del HEAD, DEC
#end reading initial file
#----------------------------------------------------------------------------
#start reading references
print ("number of reference_file : ", len(ARGUMENTS.ref_files), file=sys.stdout)
logging.debug("number of reference_file : %s", len(ARGUMENTS.ref_files))
CONTENT_TOTAL = set() #all unique reference lines in a set
#
for elt in ARGUMENTS.ref_files: #list of reference files
    with open(elt, "r") as FI_R: #reading reference file
        CONTENT_R = FI_R.readlines()
        #
        CONTENT_TMP = [] #temporary list of conserved lines
        i = 0
        NB_L = len(CONTENT_R) #number of lines
        while i < NB_L:
            if not CONTENT_R[i].startswith("#"):
                DEC = CONTENT_R[i].split("\t", 2)
                HEAD = DEC[0] + DEC[1]
                CONTENT_TMP.append(HEAD) #list of lines with only the concatenation 
                                         #of the 2 first columns
            i += 1
        print ("reading reference_file : ", elt, file=sys.stdout)
        logging.debug("reading reference_file : %s", elt)
        #
        CONTENT_TOTAL = CONTENT_TOTAL | set(CONTENT_TMP)
        #
        del elt, i, CONTENT_R, DEC, HEAD, CONTENT_TMP, NB_L
#end reading references
#----------------------------------------------------------------------------
#start file creation
LIST_CONSERVED = [0, 1, 2, 3, 4] #list conserved entries (0-4=header)
LIST_DUPLICATE_ENTRIES = [0, 1, 2, 3, 4] #list duplicate entries (0-4=header)
#
i = 5
DIC_SIZE_INITIAL = len(DIC_I)
while i < DIC_SIZE_INITIAL:
    if DIC_I[i] in CONTENT_TOTAL:
        LIST_DUPLICATE_ENTRIES.append(i) #append to the duplicate entries
    else:
        LIST_CONSERVED.append(i) #append to the conserved entries
    i += 1
#
SET_CONSERVED = set(LIST_CONSERVED) #transform in set
SET_DUPLICATE_ENTRIES = set(LIST_DUPLICATE_ENTRIES) #transform in set
#
LIST_COL7 = [] #data of the seventh column
#
with open("Final_filtered_file.txt", "w") as res: #creation of the final file 
                                             #without the duplicate entries
    #
    for NUMBER, LINE in enumerate(CONTENT_I): #for each line of the initial file
        #
        if NUMBER in SET_CONSERVED: 
            res.write(LINE) #write unique lines
            if not LINE.startswith("#"):
                DEC = LINE.split("\t", 7)
                LIST_COL7.append(DEC[6]) #statistics column 7
#
print ("creation of : Final_filtered_file.txt", file=sys.stdout)
logging.debug("creation of : Final_filtered_file.txt")
#
with open("Duplicate_entries.txt", "w") as dou: #creation of the file of
                                                #duplicate entries
    #
    for NUMBER, LINE in enumerate(CONTENT_I): #for each line of the initial file
        #
        if NUMBER in SET_DUPLICATE_ENTRIES:
            dou.write(LINE) #write duplicate entries
#
print ("creation of : Duplicate_entries.txt", file=sys.stdout)
logging.debug("creation of : Duplicate_entries.txt")
#           
del NUMBER, LINE, DEC, DIC_I, i, SET_DUPLICATE_ENTRIES, SET_CONSERVED
del DIC_SIZE_INITIAL, LIST_CONSERVED, LIST_DUPLICATE_ENTRIES
#end file creation
#----------------------------------------------------------------------------
#start statistics file
with open("Stats.txt", "w") as stat:
    #
    N_DEL = LIST_COL7.count("DEL")
    N_INV = LIST_COL7.count("INV")
    N_ITX = LIST_COL7.count("ITX")
    N_CTX = LIST_COL7.count("CTX")
    #
    stat.write("-------------------------------------------------------------\n")
    stat.write("-----STATISTICS column 7 (file without duplicate entries)----\n")
    stat.write("-------------------------------------------------------------\n")
    stat.write("DEL \t INV \t ITX \t CTX\n")
    stat.write(str(N_DEL)+"\t"+str(N_INV)+"\t"+str(N_ITX)+"\t"+str(N_CTX)+"\n")
    stat.write("\n")
    stat.write("Nunmber of lines : "+str(len(LIST_COL7))+str("\n"))
#
print ("creation of statistics file : Stats.txt", file=sys.stdout)
logging.debug("creation of statistics file : Stats.txt")
#
del CONTENT_I, CONTENT_TOTAL, LIST_COL7, N_DEL, N_INV, N_ITX, N_CTX
#end statistics file
#----------------------------------------------------------------------------
#
print ("---------------------------------------", file=sys.stdout)
print ("END Parsor_BD.py on", ARGUMENTS.initial_file, file=sys.stdout)
logging.debug("END Parsor_BD.py on %s", ARGUMENTS.initial_file)
logging.debug("---------------------------------------")
#
#----------------------------------------------------------------------------
#
