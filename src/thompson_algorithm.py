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

from automaton import *

def thompson_union (Aut1  , Aut2):
    """    
    This function returns the union of two given automata by using 
    thompson method.
    """
    A = Aut1.clone()
    B = Aut2.clone()
    #get maximum_id from A to rename state of B
    maxi_a = A.get_maximal_id()
    B.map(lambda x : x + maxi_a + 1)
    maxi_b = B.get_maximal_id()
    a_initials = A.get_initial_states()
    a_finals = A.get_final_states()
    b_initials = B.get_initial_states()
    b_finals = B.get_final_states()
    #create an automaton union of A and B
    union_initial = -maxi_b
    union_final = maxi_b + 1
    union_aut = automaton(initials = [union_initial] , finals = [union_final] , epsilons = ['0'])
    a_transitions = A.get_transitions()
    b_transitions = B.get_transitions()
    for t in a_transitions :
        union_aut.add_transition(t)
    for t in b_transitions :
        union_aut.add_transition(t)
    for s in a_initials :
        union_aut.add_transition((union_initial , '0' , s))
    for s in a_finals :
        union_aut.add_transition((s , '0' , union_final))
    for s in b_initials :
        union_aut.add_transition((union_initial , '0' , s))
    for s in b_finals :
        union_aut.add_transition((s , '0' , union_final))
    union_aut.renumber_the_states()
    return union_aut


def thompson_concat (Aut1 , Aut2):
    """
    This function returns the concatenation of two given automata 
    by using thompson method.
    """
    A = Aut1.clone()
    B = Aut2.clone()
    maxi_a = A.get_maximal_id()
    B.map(lambda x : x + maxi_a + 1)
    a_transitions = A.get_transitions()
    b_transitions = B.get_transitions()
    a_initials = A.get_initial_states()
    a_finals = A.get_final_states()
    b_initials = B.get_initial_states()
    b_finals = B.get_final_states()
    maxi_b = B.get_maximal_id()
    concat_initial = -maxi_b
    concat_final = maxi_b + 1
    concat_aut = automaton(initials = [concat_initial] , finals = [concat_final] , epsilons = ['0'])
    for t in a_transitions :
        concat_aut.add_transition(t)
    for t in b_transitions :
        concat_aut.add_transition(t)
    for s in a_initials :
        concat_aut.add_transition((concat_initial , '0' , s))
    for s in b_finals :
        concat_aut.add_transition((s , '0' , concat_final))
    for s in a_finals :
        for t in b_initials :
            concat_aut.add_transition((s , '0' , t))
    concat_aut.renumber_the_states()
    return concat_aut


def thompson_star (Aut):
    """
    This function returns the kleene star of the given automaton by 
    using thompson method.
    """
    A = Aut.clone()
    A.renumber_the_states()
    A.map(lambda x : x - 1)
    a_transitions = A.get_transitions()
    star_finals = A.get_maximal_id() + 1
    star_initials = -star_finals
    a_initials = A.get_initial_states()
    a_finals = A.get_final_states()
    star_aut = automaton(initials = [star_initials] , finals = [star_finals] , epsilons = ['0'])
    for t in a_transitions :
        star_aut.add_transition(t)
    for s in a_initials :
        star_aut.add_transition((star_initials , '0' , s))
    for s in a_finals :
        star_aut.add_transition((s , '0' , star_finals))
    for s in a_initials :
        for t in a_finals :
            star_aut.add_transition((s , '0' , t))
    star_aut.add_transition((star_initials , '0' , star_finals))
    star_aut.renumber_the_states()
    return star_aut


def thompson_basic_automata (char):
    """
    This function returns the corresponding automaton of the given 
    basic expression.
    """     
    return automaton(initials = [0] , finals = [1] , transitions = [(0 , char , 1)])
