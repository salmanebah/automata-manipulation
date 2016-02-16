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

from  automaton import *
from thompson_algorithm import *
from infix_to_prefix_manipulation import infix_to_prefix
from infix_to_prefix_manipulation import reverse_input
# -*- coding: UTF-8 -*-
import sys


def is_complete(Aut):
    """
    This function returns True if the automaton is complete , False otherwise.
    """
    states = Aut.get_states()
    alphabet = Aut.get_alphabet()
    if not alphabet or not states :
        return False
    get_transition = Aut.delta
    for s in states :
        for a in alphabet :
            if not get_transition(a , [s]) :
                return False
    return True


 
def is_deterministic (Aut):
    """
    This function returns True if the automaton is deterministic,
    False otherwise.
    """
    if Aut.has_epsilon_characters():
        return False
    if len(Aut.get_initial_states()) != 1:
        return False
    alphabet = Aut.get_alphabet()
    states = Aut.get_states()
    for s in states:
        for a in alphabet:
            if len (Aut.delta(a , [s])) >= 2:
                return False
    return True
    
    

def completer (Aut):
    """ This function returns the complete automaton of given Automaton.
    """
    if is_complete(Aut) :
        return Aut
    A = Aut.clone()
    A.renumber_the_states()
    # well state is maximal_id of automaton + 1
    well = A.get_maximal_id() + 1
    states = A.get_states()
    alphabet = A.get_alphabet()
    # add well state
    A.add_states([well])
    for s in states :
        for a in alphabet :
            # the set is empty
            if not A.delta(a , [s]) :
                A.add_transition((s , a , well))
            A.add_transition((well , a , well))
    return A 



def miroir (Aut):
    """ 
    This function compute and returns the miror  of the given autamaton.
    """
    initials = Aut.get_initial_states()
    finals = Aut.get_final_states()
    transit = list( Aut.get_transitions())
    A = automaton(initials = finals , finals = initials)
    
    for t in transit :
        A.add_transition(tuple(reversed(t)))
    return A


def suppress_epsilon_transitions(Aut):
    """ This function returns the equivalent automaton of the given 
    one with e-move suppressed.
    """ 
    initials = Aut.get_initial_states()
    finals =  Aut.get_final_states()
    states = Aut.get_states()
    epsilon_set = Aut.get_epsilons()
    alphabet = Aut.get_alphabet()
    
    A = automaton (initials = initials , finals = finals , states = states)
    valid_alphabet = alphabet - epsilon_set
    transition_list = [list(x) for x in Aut.get_transitions()]
    # add all transitions except e-transitions 
    for l in transition_list:
        if l[1] in valid_alphabet :
            A.add_transition(tuple(l))
    
    for s in states :
        next_by_e_move = []
        for e in epsilon_set :
            item = Aut.delta(e , [s])
            item = [x for x in item]
            next_by_e_move.extend(item)
        if s in next_by_e_move:
            next_by_e_move.remove(s)
        for a in valid_alphabet :
            successor = []
            for after in next_by_e_move :
                item = Aut.delta(a , [after], ignore_epsilons = True)
                successor.extend(item)
            for succ in successor :
                A.add_transition((s , a , succ))
                if after in finals:
                    A.add_final_states([s])                      
    return A   




def  determiniser(Aut):
    """
    This function returns the equivalent deterministic automaton
    of the one given.
    """
    if is_deterministic(Aut):
        return Aut
    A = suppress_epsilon_transitions(Aut)
    initials = A.get_initial_states()
    finals = A.get_final_states()
    alphabet = A.get_alphabet()
    B = automaton()
    start = pretty_set(initials)
    B.add_initial_state(start)
    state_to_compute = [start]
    state_computed = []
    while (state_to_compute):
        state = state_to_compute[0]
        successor = {x : set() for x in alphabet}
        for substate in state :
            for a in alphabet :
                successor[a] = successor[a].union(A.delta(a , [substate]))
        for key in successor :
            successor_set  = pretty_set(successor[key])
            if successor_set not in state_computed and successor_set not in state_to_compute :
                state_to_compute.append(successor_set)
            B.add_transition((state, key , successor_set))
        state_to_compute.remove(state)
        state_computed.append(state)
    for state in state_computed :
        for substate in state :
            if substate in finals :
                B.add_final_state(state)
    return B



def complement (Aut):
    """" 
    This function returns the complement of the given automaton.
    """

    if is_deterministic(Aut):
        B = completer(Aut)
    else :
        B = determiniser(Aut)
    transitions = B.get_transitions()
    initials = B.get_initial_states()
    finals = B.get_final_states()
    states = B.get_states()
    non_finals = states - finals
    return automaton(initials = initials,finals = non_finals, transitions = transitions)



def automaton_with_cartesian_product (A , B , union_or_intersect = 0):
    """ 
    This function returns the union or the intersection of two automata
    if keyword union_or_intersect = 0 , the union of returned,
    intersection is returned otherwise
    TODO: use set comprehension generation , add keyword parameter to specify 
    either union or intersection
    """

    if (A.get_alphabet() != B.get_alphabet()):
        print("/!\\Automaton don't have the same alphabet /!\\")
        sys.exit()

    if is_deterministic(A) :
        new_A = completer(A)
    else :
        new_A = determiniser(A)
    new_A.renumber_the_states()
    if is_deterministic(B) :
        new_B = completer(B)
    else :
        new_B = determiniser(B)
    new_B.renumber_the_states()
        
    states_of_A = new_A.get_states()
    initials_of_A = new_A.get_initial_states()
    finals_of_A = new_A.get_final_states()
    states_of_B = new_B.get_states()
    initials_of_B = new_B.get_initial_states();
    finals_of_B = new_B.get_final_states()
    product_aut = automaton()
    for s in states_of_A :
        for t in states_of_B :
            for a in A.get_alphabet() :
                x = list(new_A.delta(a,[s]))
                x.extend(list(new_B.delta(a,[t])))
                x_y_tuple = tuple(x)
                product_aut.add_transition(((s,t), a, x_y_tuple))
                if s in initials_of_A and t in initials_of_B :
                    product_aut.add_initial_state((s,t))                
    states_product_aut = product_aut.get_states()
    if union_or_intersect == 0 :
        for state in states_product_aut :
            if state[0] in finals_of_A or state[1] in finals_of_B :
                product_aut.add_final_state(state)
    else :
        for state in states_product_aut :
            if state[0] in finals_of_A and state[1] in finals_of_B :
                product_aut.add_final_state(state)
    return product_aut

def union (Aut1 , Aut2):
    """"
    This function returns the union of the two given automata.
    """
    return automaton_with_cartesian_product(Aut1,Aut2,0)


def intersection (Aut1 , Aut2):
    """"
    This function returns the intersection of the two given automata.
    """
    return automaton_with_cartesian_product(Aut1,Aut2,1)


def minimiser_moore (Aut) :
    """"
    This function returns the minimize automaton of the given one by using 
    moore algorithm.
    """
    if is_deterministic(Aut) :
        B = completer(Aut)
    else :
        B = determiniser(Aut)
    B.renumber_the_states()
    B.map(lambda x : x - 1)
    alphabet = B.get_alphabet()
    card_alphabet = len(alphabet)
    states = B.get_states()
    maxi = B.get_maximal_id()
    states_list = [x for x in range(maxi + 1)]
    destination_reference = [[] for _ in range(len(alphabet))]
    i = 0
    for a in alphabet :
        destination_reference[i] = []
        for s in states_list :
                l = B.delta(a,[s])
                l = [x for x in l][0]
                destination_reference[i].append(l)
        i += 1
    equivalence_classes = [0 for x in states]
    for i in range(maxi + 1) :
        if B.state_is_final(i) :
            equivalence_classes[i] = 1
    pre_equivalence_classes = []
    while (pre_equivalence_classes != equivalence_classes) :
        class_number = 0
        mark_array = [False for _ in range(maxi + 1)]
        pre_equivalence_classes = [x for x in equivalence_classes]
        # going through the states
        for i in range(maxi + 1) :
            if mark_array[i] == True :
                continue
            eq_per_loop = [i]
            list_tuple = [pre_equivalence_classes[i]]
            #going through the alphabet
            for j in range(card_alphabet) :
                # first get the successor of i by j and then compute his equivalence_class
                list_tuple.append(pre_equivalence_classes[destination_reference[j][i]])
            # check if other states have the same list , if so then the two are in same eq_class
            for k in range(i + 1 , maxi + 1) :
                inner_list_tuple = [pre_equivalence_classes[k]]
                # going again through the alphabet
                for l in range(card_alphabet) :
                    inner_list_tuple.append(pre_equivalence_classes[destination_reference[l][k]])
                    # same class
                if list_tuple == inner_list_tuple :
                    eq_per_loop.append(k)
            # update the equivalence_classes
            for s in eq_per_loop :
                mark_array[s] = True
                equivalence_classes[s] = class_number
            class_number += 1
    mini_state = {x for x in equivalence_classes}
    mini_state = [x for x in mini_state]
    #initial state of the original automaton
    initials = [x for x in B.get_initial_states()]
    #final state of the original automaton
    finals = [x for x in B.get_final_states()]
    mini_initial = equivalence_classes[initials[0]]
    mini_final = []
    for s in finals:
        mini_final.append(equivalence_classes[s])
    minimal_aut = automaton(states = mini_state , initials = [mini_initial],
                            finals = mini_final , alphabet = alphabet)
    for s in states_list:
        eq_s = equivalence_classes[s]
        i = 0
        for a in alphabet :
            successor_by_a = equivalence_classes[destination_reference[i][s]]
            minimal_aut.add_transition((eq_s, a , successor_by_a))
            i += 1
    return minimal_aut



def minimiser_brzozowski(Aut):
    """
    This function returns the minimized automaton of the given one by using
    brzozowski algorithm.
    """
    aut_min = determiniser(miroir(determiniser(miroir(Aut))))
    aut_min.renumber_the_states()
    return aut_min
    

def minimiser (Aut , algo = "moore") :
    """
    This function returns the minimized automaton of  the given one depending 
    on the given algorithm, by defaut the algorithm used is moore 
    (can pass the brzozowski string too)
    """
    if algo == "moore" :
        return minimiser_moore(Aut)
    else :
        return minimiser_brzozowski(Aut)

def expression_vers_automate(e):
    """
    This function converts a regular expression given in a list to an  automaton
    using the thompson algorithm.
    """
    operation = e[0]
    if operation == '*' :
        return thompson_star(expression_vers_automate(e[1]))
    elif operation == '+' :
        return thompson_union(expression_vers_automate(e[1]) , expression_vers_automate(e[2]))
    elif operation == '.' :
        return thompson_concat(expression_vers_automate(e[1]) , expression_vers_automate(e[2]))
    #necessarily a basic operation
    else :
        return thompson_basic_automata(operation) 
                               
def regex_to_list_aux (postfix_string):
    output_stack = []
    operators = ['+', '*', '.']
    for c in postfix_string:
        if c not in operators:
            output_stack.append([c])
        elif c == '+' or c == '.':
            a = output_stack.pop()
            b = output_stack.pop()
            output_stack.append([c, a, b])
        else:
            a = output_stack.pop()
            output_stack.append([c, a])
    return output_stack[0]
    
def regex_to_list(string):
    prefix_string = infix_to_prefix(string)
    return regex_to_list_aux(reverse_input(prefix_string))
