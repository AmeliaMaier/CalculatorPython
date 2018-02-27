'''
Created on Oct 10, 2017

@author: Lia
'''

import parser
from tkinter import *
from tkinter import Tk, Label, Button, Entry
from turtledemo.__main__ import getExampleEntries

'''
formula = ''
result_list = []
print ('Enter Formula:')
while(formula != 'exit'):
    if(formula == 'help'):
        print('help file to be written')
    elif(formula == 'clear'):
        result_list.clear()
    elif(formula != 'exit'):
        formula = input()
        code = parser.expr(formula).compile()
        result_list.append(eval(code))
        print (eval(code))
'''

def solve():
    raw_user_input = equation_input.get()
    equations_values_list.append(raw_user_input)    
    parsed_answer = parser.expr(raw_user_input).compile()
    answers_values_list.append(parsed_answer)
    x.append(parsed_answer)    
    reset_Equation_List()
    reset_Answer_List()
    reset_X_List()
    equation_input.delete(0, END)
    
def clear():
    equation_input.delete(0, END)
    variable_names_values.delete(0, END)
    x.delete(0, END)
    answers_values.delete(0, END)
    equations_values.delete(0, END)
    
def reset_Equation_List():
    y = 0
    equations_values.delete(0, END)
    for equation in equations_values_list:
        equations_values.insert(y, equation)
        y = y + 1
        
def reset_Answer_List():
    y = 0
    answers_values_list.delete(0, END)
    for answer in answers_values_list:
        answers_values.insert(y, answer)
        y = y + 1
        
def reset_X_List():
    y = 0
    variable_names_values.delete(0, END)
    for variable_Value in x:
        variable_names_values.insert(y, ("x["+ y + "]"))
        y = y + 1
    
root = Tk() 
root.title("Parsing Calculator")

x = []
equations_values_list = []
answers_values_list = []

equations_label = Label(text = "Equations").grid(row=0, column=0)
equations_values = Listbox().grid(row=1, column=0)
answers_label = Label(text = "Answers").grid(row=0, column=1)
answers_values = Text().grid(row=1, column=1)
variable_names_label = Label(text = "Variable Names").grid(row=0, column=2)
variable_names_values = Text().grid(row=1, column=2)
equation_input_label = Label(text = "Enter Equation:").grid(row=2)
equation_input = Entry().grid(row=3)
solve_button = Button(text = "Solve", command = solve).grid(row=4)
clear_button = Button(text = "Clear", command = clear).grid(row=5)
root.bind('<Return>', solve)
    
mainloop()



