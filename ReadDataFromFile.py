# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 16:25:23 2022

@author: rsp97
"""

file = open("F_High_Score.txt", "r")

high_score=file.read()
print(type(int(high_score)))

#input text
#highest_points = points  
#score_collision = points
#store high_score value in file

 
#add variable
#file.write(str(highest_points))
 
#close file
file.close()
flag_high_score=False
#flag_display_high_score=True
