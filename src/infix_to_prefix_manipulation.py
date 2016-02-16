# -*- coding: utf-8 -*-
# Copyright (C) 2013 BAH Salmane, SOLLAUD Timothée, University of Bordeaux 1, France
#
#   This Library is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This Library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this Library.  If not, see <http://www.gnu.org/licenses/>.

import re

def stack_empty(stack):
    return 1 if(len(stack) == 0) else 0

def stack_top(stack):
    return stack[-1]

def push_stack(stack,ele):
    stack.append(ele)

def pop_stack(stack):
    return stack.pop()

def operand(opr):
    return 1 if(not(operator(opr)) and (opr != "(") and (opr != ")")) else 0

def operator(opr):
    return 1 if opr in ["+","*","."] else 0

def precedence(opr):
    if opr == "*" :
           return 5
    if opr == "." :
           return 4
    if opr == "+" :
           return 3
    if opr == "(" :
           return 2
    if opr == ")" :
           return 1

def infix_to_prefix(string):
    infix_expression = convert_input_to_stack(string)
    prefix_list = []
    stack = []
    lst = list(infix_expression)
    infix_expression = infix_expression[::-1]
    infix_list = list(infix_expression)
    #print(infix_list)
    for i in infix_list:
        if operand(i):
            prefix_list.append(i)
        if operator(i):
            while((not(stack_empty(stack))) and (precedence(i) <= precedence(stack_top(stack)))):
                prefix_list.append(stack_top(stack))
                pop_stack(stack)
            push_stack(stack,i)
        if(i == ")"):
            push_stack(stack,i)
        if(i == "("):
            while(stack_top(stack) != ")"):
                append_operator = pop_stack(stack)
                prefix_list.append(append_operator)
            pop_stack(stack)
    while(not(stack_empty(stack))):
        if(stack_top(stack) == ")"):
            pop_stack(stack)
        else:
            prefix_list.append(pop_stack(stack))
    #print(prefix_list)       
    prefix_expression = ''
    for val in prefix_list:
        prefix_expression += val

    return prefix_expression[::-1]


def convert_input_to_stack(string):
    """
    This function returns a list of char from the string with 
    its operations(including ".")
    """
    str_without_space = re.sub('\s{1,}' , "" , string)
    stack_input = []
    concat_prefix = [')' , '*']
    non_concat_prefix = ['(' , '.' , '+']
    has_prefix = False
    length = len(str_without_space)
    for i in range(length - 1) :
        stack_input.append(str_without_space[i])
        if str_without_space[i] in concat_prefix or (str_without_space[i] >= 'A' and str_without_space[i] <= 'z') :
            if str_without_space[i + 1] >= 'A' and str_without_space[i + 1] <= 'z' :
                stack_input.append('.')
    stack_input.append(str_without_space[length - 1])
    return stack_input


def reverse_input(prefix_string):
    """
    This function returns a reversed stack.
    """
    postfix_string = ""
    i = len(prefix_string) -1
    while i >= 0 :
        postfix_string = postfix_string + prefix_string[i]  
        i -= 1
    print(postfix_string)
    return postfix_string
