from types import *
import pdb
from random import randint
from collections import OrderedDict
import sys, getopt
#pdb.set_trace()





def check_all_literal(lst):#function to check if list contains all literal types
    #print "checking:", lst
    if type(lst) is not list and len(lst) is 1:
        return True
    if type(lst) is list and is_literal(lst):
        return True
    for var in lst:
        #print "enter loop"
        if not is_literal(var):
            return False
        else:
            return True
        

def associate_helper_or(lst1,lst2):#helper function for associativity of and & or
    newList=[]
    #print "lst1",lst1
    #print "lst2",lst2
    if check_all_literal(lst1):
        #print "enter 1"
        if check_all_literal(lst2):
            temp=['or']
            temp.append(lst1)
            if type(lst2) is not list and lst1 !=lst2 :
                temp.append(lst2)
            elif type(lst2) is list and not is_literal(lst2):
                for var in lst2:
                    temp.append(var)
            elif type(lst2) is list and is_literal(lst2):
                temp.append(lst2)
            newList.append(temp)
        else:
            if lst2[0]=='or':
                #newList.append(lst1)
                for var in lst2[1:]:
                    lst1.append(var)
                newList=lst1
                #newList.insert(0,'or')
            if lst2[0]=='and':
                temp=['or']
                for var in lst2[1:]:
                    temp.append(var)
                    temp.append(lst1)
                    newList.append(temp)
                    temp=['or']
        #print "helper1", newList
        #newList.insert(0,'and')
        return newList
    elif check_all_literal(lst2):
        #print "enter 2"
        if lst1[0] == 'or':
            temp=[]
            for var in lst1[1:]:
                temp.append(var)
            temp.append(lst2)
            newList.append(temp)
        elif lst1[0] == 'and':
            temp=['or']
            for var in lst1[1:]:
                temp.append(var)
                temp.append(lst2)
                newList.append(temp)
                temp=['or']
        #print "helper2", newList
        return newList
    elif lst1[0]=='and' and lst2[0] == 'and':
        #print "enter 3"
        for var1 in lst1[1:]:
            for var2 in lst2[1:]:
                temp=['or']
                temp.append(var1)
                if var2 != var1:
                    temp.append(var2)
                    newList.append(temp)
        return newList
    elif lst1[0]=='and' and lst2[0] == 'or':
        #print "enter 4"
        for var1 in lst1[1:]:
            temp=['or']
            temp.append(var1)
            for var2 in lst2[1:]:
                if var1 != var2:
                    temp.append(var2)
            newList.append(temp)
        return newList
    elif lst1[0] == 'or' and lst2[0] == 'and':
        #print "enter 5"
        for var1 in lst2[1:]:
            temp=['or']
            temp.append(var1)
            for var2 in lst2[1:]:
                if var1 != var2:
                    temp.append(var2)
            newList.append(temp)
        return newList
    elif lst1[0] == 'or' and lst2[0] == 'or':
        #print "enter 6"
        temp=['or']
        for var in set(lst1[1:]+lst2[1:]):
            temp.append(var)
        return newList
            
            
        
def associative_or_and(lst):#Function to implement associative rule
    #print "input", lst
    prevResult=lst[1]
    newList=[]
    lstNew=[]
    flag=1
    if lst[0] == 'or':
        length = len(lst[1:])
        #print "length", length
        for i in range(1,length):
            newList=associate_helper_or(prevResult,lst[i+1])
            prevResult=newList
            lstNew=newList
            #print "lstNew", i,lstNew
            length=length-1
        if len(lstNew) is 1:
            lstNew=lstNew[0]

    if lst[0] == 'and':
        for var in lst[1:]:
            if is_literal(var):
                lstNew.append(var)
            if not is_literal(var) and var[0] == 'and':
                temp=associative_or_and(var)
                for var in temp:
                    lstNew.append(var)
            if not is_literal(var) and var[0] == 'or':
                prevRes=var[1]
                length = len(var[1:])
                for i in range(1,length):
                    newList=associate_helper_or(prevRes,var[i+1])
                    prevResult=newList
                    for v in newList:
                        lstNew.append(v)
                    #print "lstNew", i,lstNew
                    length=length-1
    for var in lstNew:
        if not is_literal(var):
            lstNew.insert(0,'and')
            flag=0
            break
    if (flag):
        #print "enter flag"
        lstNew.insert(0,'or')
    return lstNew
            

def is_literal(lst):#function to check if variable is literal
    if type (lst) is list and len(lst) is 1:
        return True
    elif type (lst) is list and len(lst) is 2:
        if type (lst[1]) is not list and len(lst[1]) is 1:
            return True
        else:
            return False
    elif type (lst) is list and len(lst) > 2:
        return False
    elif type (lst) is not list and len(lst) is 1:
        return True


def or_conversion(lst):#function to implement or connective functionality
    newList=[]
    result=[]
    for var in lst[1:]:
        #print "var in or",var
        if is_literal(var):
            result.append(var)
            #print "result in or", result
        if var[0] == 'implies':
            newList=convert(var)
            result.append(newList)
        if var[0] == 'iff':
            newList=convert(var)
            result.append(newList)
        if var[0] == 'and':
            newList=convert(var)
            result.append(newList)
        if var[0] == 'not' and not is_literal(var):
            newList=convert(var)
            result.append(newList)
            #print "result in or not", result
    #print "before , insert" , result
    result.insert(0,'or')
    #print "result final",result
    return result


def bi_implication_removal(lst):#function to implement biconditional removal 
    result_op_prim="and"
    result_op_sec_1="implies"
    #result_op_sec_2="not"
    sub_clause_1=lst[1]
    sub_clause_2=lst[2]
    newList=[]
    sub_list_1=convert(sub_clause_1)
    sub_list_2=convert(sub_clause_2)
    temp=[result_op_sec_1,sub_list_1,sub_list_2]
    newList.append(result_op_prim)
    newList.append(temp)
    temp=[result_op_sec_1,sub_list_2,sub_list_1]
    newList.append(temp)
    newList=convert(newList)
    #print newList
    return newList


def implication_removal(lst):#function to implement implication removal
    #print "enter impli",lst
    newList=[]
    result_op_prim="or"
    #result_op_sec="not"
    sub_clause_1=lst[1]
    #print "sub1",sub_clause_1
    sub_clause_2=lst[2]
    #print "sub2",sub_clause_2
    sub_list_1=clause_negation(convert(sub_clause_1))
    newList.append(result_op_prim)
    if is_literal(sub_list_1[0]):
        newList.append(sub_list_1[0])
    else:
        newList.append(sub_list_1)
    newList.append(convert(sub_clause_2))
    #print newList
    return newList
    

def and_conversion(lst):#function to implement and connective functionality
    newList=[]
    result=[]
    for var in lst[1:]:
        if is_literal(var):
            result.append(var)
        if var[0] == 'implies':
            newList=convert(var)
            result.append(newList)
        if var[0] == 'iff':
            newList=convert(var)
            result.append(newList)
        if var[0] == 'and':
            newList=convert(var)
            result.append(newList)
        if var[0] == 'not'and not is_literal(var):
            newList=convert(var)
            result.append(newList)
        if var[0] == 'or':
            newList=convert(var)
            result.append(newList)
    result.insert(0,'and')
    #print "result and",result
    return result
    


def clause_negation(lst):#fnction to negate a clause
    newList=[]
    #print lst
    for var in lst:
        #print "negation:", var
        if type (var) is list and is_literal(var):
            newList.append(var[1])
        if type (var) is list and not is_literal(var):
            newList.append(clause_negation(var))
        if type (var) is not list and is_literal(var):
            temp=['not',var]
            newList.append(temp)
        if var == 'and':
            newList.append('or')
        if var == 'or':
            newList.append('and')
    #print "newList"+str(newList)
    return newList
            
def negation(lst): # function to implement not functionality
    if is_literal(lst):
        return lst
    if type(lst) is list and lst[0] is 'not' and lst[1][0] is 'not':
        return convert(lst[1][1])
    if type(lst) is list and lst[0] is 'not' and lst[1][0] is 'implies':
        return clause_negation(convert(lst[1]))

    
def convert(lst):#driver function to convert to CNF
    if is_literal(lst):
        return lst
    if lst[0] == 'not':
        return negation(lst)
    if lst[0] == 'implies':
        return implication_removal(lst)
    if lst[0] == 'or':
        return or_conversion(lst)
    if lst[0] == 'and':
        return and_conversion(lst)
    if lst[0] == 'iff':
        return bi_implication_removal(lst)

        
def main(argv):#main function for input and output
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print "error in reading commandlin arguments"
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            inputfile=arg
    f = open(inputfile)
    i = int(f.readline())
    f1=open("sentences_CNF.txt","w+")
    result=[]
    lstNew=[]
    while i is not 0:
        sen1 = f.readline()
        lst=eval(str(sen1))
        lstNew=convert(lst)
        if is_literal(lstNew):
            if type(lstNew) is not list:
                result=[lstNew]
            else:
                result=lstNew
        else:
            result=associative_or_and(lstNew)
        f1.write(str(result))
        f1.write("\n")
        i=i-1
        
if __name__=="__main__":

    main(sys.argv[1:])
