#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Linguistic Fractionalization (LF) Automated Calculator

This program automatically calculates the linguistic fractionalization 
for each subnational unit in a country, which is a variable used in the
dissertation titled Understanding the Roles of Language in Public Opinion.

Author:
    Haofeng Ma
    Ph.D. Candidate (ABD)
    Department of Political Science
    The University of Iowa
    haofeng-ma@uiowa.edu
    
Date Created:
    May 1, 2022, Central Standard Time
    
Date Last Modified:
    May 20, 2022, Central Standard Time
"""   
    

"""
Input File:
    1) A matrix of linguistic distances for all named languages in a country
    
       Source: The matrix is returned by the ASJP software.
       Name format: "LDmatrix_raw_country.csv".
       
    2) A table of the population share in each subnational unit
       for all named language in a country
    
       Source: The table is generated using information gathered from
               multiple sources.
       Name format: "LP_country.csv".

Output File:
    1) A csv file storing the linguistic fractionalization for each subnational
       unit in a country.
       
       Name format: LF_country.csv".

Note:
    1. The two files must both be put in the current working directory.
    2. The list of the languages in the two files must be exactly the same.
    3. The order of the languages in the two files must be exactly the same.
    4. The names of the languages in the two files must be exactly the same.
"""

##############################
import os
os.chdir(r"/Users/haofengma/Documents/Academic/PhD/Doctoral Dissertation/data")

country_name = input("Input the country name: ")
##############################

LD_file_root_name = "LDmatrix_raw_"
LD_file_name = LD_file_root_name + country_name + ".csv"

LP_file_root_name = "LP_"
LP_file_name = LP_file_root_name + country_name + ".csv"

LDfile = open(LD_file_name, "r")
LD_read = LDfile.readlines()
LDfile.close()

LD_matrix = []
for line in LD_read:
    line = line.strip()
    line = line.split(",")
    LD_matrix.append(line)
    
LD_dict = {}
for line in LD_matrix[1: ]:
    key_left = line[0]
    j = 1
    for i in line[1: ]:
        key = key_left + "_" + LD_matrix[0][j]
        value = i
        LD_dict.update({key: value})
        j += 1
        
LPfile = open(LP_file_name, "r")
LP_read = LPfile.readlines()
LPfile.close()

LP_matrix = []
for line in LP_read:
    line = line.strip()
    line = line.split(",")
    LP_matrix.append(line)

language_list = LP_matrix[0]

Lfrac_raw = {}    
for region in LP_matrix[1: ]:
    region_name = region[0]
    Lfrac = 0
    num_p = 1
    for p in region[1: ]:
        num_another = num_p + 1
        while num_another < len(region):
            LD_key = language_list[num_another]+ "_" + language_list[num_p]
            LD = float(LD_dict[LD_key])
            pp = float(p) * float(region[num_another])
            Lfrac += pp * LD
            # below lines are for checking the correctness of the loops
            # thisp = "P is " + str(p)
            # thisa = "A is " + str(region[num_another])
            # print(Lfrac, thisp, thisa)
            num_another += 1
        num_p += 1
    Lfrac = round(Lfrac, 2)
    Lfrac_raw.update({region_name: Lfrac})
    
#print(Lfrac_raw)

Lfrac_raw_list = []

for key in Lfrac_raw.keys():
    inner_list = [country_name, key, Lfrac_raw.get(key)]
    print(inner_list)
    Lfrac_raw_list.append(inner_list)
    
#print(Lfrac_raw_list)


#save the result to a csv file
import csv

fields = ["Country", "Region", "Lfrac_raw"]
csv_root_name = "LF_"
csv_file_name = csv_root_name + country_name + ".csv"

with open(csv_file_name, "w") as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(Lfrac_raw_list)  
