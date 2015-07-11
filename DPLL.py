from random import randint
from collections import OrderedDict
import sys, getopt


def splitting_rule(lst,res): #function to implement dpll splitting rule
    lit=res.keys()
    res1=dict(res)
    res2=dict(res)
    lst1=list(lst)
    lst2=list(lst)
    lst1.append(lit[0])
    lst2.append((lit[0]+'_'))
    res1=unit_clause(lst1,res1)
    #print "result in splitting",res1
    if (res1.has_key("all")):
        #print "splitting 2", lst2
        res2=unit_clause(lst2,res2)
        return res2
        #print "result in splitting2",res2
    else:
        return res1



def pop_helper(lst,indexList): #function to pop values from list correctly
    #print lst
    count=-1
    indexList.sort()
    for i in indexList:
        count=count+1
        lst.pop(i-count)
    #print "after pop", lst
        
    
def assign_value_dict(var,res):#function to assign vaues to literals
    if len(var) >1:
        value="false"
    else:
        value="true"
    res[var[0]]=value

def pure_symbol_new(set1,res,lst):#function to implement pure symbol rule
    indexList=[]
    if len(lst) == 0:
        return res
    for var in set1:
        indexList=is_pure(var,lst)
        if len(indexList) !=0:
            #print "enter indexlist !=0"
            for i in indexList:
                for var in lst[i]:
                    #print "lst[i]",lst[i]
                    assign_value_dict(var,res)
            pop_helper(lst,indexList)
            #print "lst pure",lst
    if is_empty_sentence(lst):
        return res
    elif is_empty_clause(lst):
        res.clear()
        res={"all":"false"}
        return res
    else:
        return res
        

def is_pure(var,lst):#function to check if literal is pure
    #print "var isp",var
    #print "lst isp",lst
    indexList=[]
    idx=-1
    flag=0
    flg=0
    checkFor=''
    if len(var)>1:
        checkFor=var[0]
    else:
        checkFor=var+"_"
    #print "checfor",checkFor
    for var1 in lst:
        if (flag):
            break
        idx=idx+1
        for item in var1:
            if (item == checkFor):
                indexList=[]
                flag=1
                break
            if (flag ==0) and item == var:
                indexList.append(idx)
            
    #print "indexist return",indexList        
    return indexList

            
def is_empty_sentence(lst):#function to check if sentence is empty
    if len(lst) == 0:
        return True
    
def is_empty_clause(lst):#function to check if any clause is empty
    for var in lst:
        if type(var) is list and len(var) ==0:
            return True

def contain_unit(lst,unit):#function to check if list contains any unit clause
    #print "passed unit",unit
    #print "passed lst", lst
    index=-1
    if type(lst) is not list:
        if lst == unit:
            return 0
        else:
            return -1
    for var in lst:
        index=index+1
        if var == unit:
            return index
    return -1


def unit_clause(lst,result):#function to implement unit clause rule
    #print "list1",lst
    #print "result1",result
    lst_temp=list(lst)
    res=''
    flag = 0
    unit=''
    if (is_empty_clause(lst)):
        #print "empty clause"
        result.clear()
        result["all"]="false"
    if (is_empty_sentence(lst)):
        return result
    for var in lst:
        #print "var",var
        if (is_unit(var)):
            #print "unit",var
            unit = var
            assign_value_dict(var,result)
            #result.append(res)
            lst.remove(var)
            lst_temp.remove(var)
            flag=1
            break
    #print "result2", result
    if flag == 0 or (flag ==1 and len(lst) == 0):
        return result
    #print "list2",lst
    index=-1
    for var in lst_temp:
        index=index+1
        #print "inloop",var
        if type(var) is list and contain_unit(var,unit)!=-1:
            #print "enter condition 1"
            for i in var:
                #print "i" ,i
                if (i==unit):
                    continue
                else:
                    assign_value_dict(i,result)
            lst.remove(var)
            index=index-1
            #print "after removal",lst
        elif len(unit)==2 and contain_unit(var,unit[0])!=-1:
            #print "enter con2"
            if type(var) is list:
                lst[index].pop(contain_unit(var,unit[0]))
            else:
                lst.pop(contain_unit(var,unit[0]))
        elif len(unit)==1 and contain_unit(var,unit[0]+'_')!=-1:
            #print "enter con3"
            if type(var) is list:
                lst[index].pop(contain_unit(var,unit[0]+'_'))
            else:
                lst.pop(contain_unit(var,unit[0]+'_'))
    return unit_clause(lst,result)
                
    
    
    
def is_unit(var): #function to check if var is unit clause
    if type(var) is not list and (len(var) ==1 or len(var) ==2):
        #print "is_unit 1"
        return True
    elif type(var) is list and (len(var) ==1):
        #print "is_unit 2"
        return True

def is_literal_helper(lst):#helper function to check if variable is literal
    if type (lst) is list and len(lst) is 1:
        return True
    elif type (lst) is list and len(lst) is 2:
        if type (lst[1]) is not list and len(lst[1]) is 1 and lst[0] == 'not':
            return True
        else:
            return False
    elif type (lst) is list and len(lst) > 2:
        return False
    elif type (lst) is not list and len(lst) is 1:
        return True


def remove_connectives(lst):#function to convert list to internal implementation for processing
    newList=[]
    res=[]
    flag=0
    for var in lst:
        if flag == 1:
            newList.append(var+'_')
            flag=0
        elif var == 'not':
            flag=1
            continue
        elif is_literal_helper(var) and flag ==0:
            #print "enter 1"
            if len(var) > 1:
                #print "enter 11"
                newList.append(var[1]+'_')
            else:
                #print "enter 12"
                newList.append(var)
        elif not is_literal_helper(var) and var !='and' and var !='or':
            #print "enter 2"
            newList.append(remove_connectives(var))
    return newList



def contain_oppo(lst):#helper function to check if list contains literal and its compliment 
    for var1 in lst:
        if len(var1) ==1:
            oppo=var1+'_'
        else:
            oppo=var1[0]
        for var2 in lst:
            if oppo==var2:
                return True
    return False



def create_result(res_dict): #function to create result array from result dictionary
    result=[]
    if res_dict.has_key("all"):
        result=["false"]
        return result
    else:
        result.append("true")
        for key, value in res_dict.iteritems():
            result.append("{0}={1}".format(key,value))
    return result

def sat_solver(lst,s,res):#function to implement DPLL
    flag=0
    result=[]
    if(check_list(lst)):
        if len(lst) ==1:
            if (len(lst[0])==2):
                result=["true", "{0}=false".format(lst[0][0])]
            else:
                result=["true", "{0}=true".format(lst[0])]
            return result
        for var in lst:
            if (contain_oppo(lst)):
                result=["false"]
                return result
            else:
                flag=1
    res=unit_clause(lst,res)
    #print "lst in sat", lst
    if (flag==1):
        return create_result(res)
    res=pure_symbol_new(s,res,lst)
    #print "lst in sat 2",lst
    if (is_empty_clause(lst)):
        res.clear()
        res['all']="false"
    res=splitting_rule(lst,res)
    return create_result(res)    
    
def check_list(lst):#function to check if all literals are in one list
    for var in lst:
        if type(var) is list:
            return False
    return True

def create_set(lst):#create set of unique literals
    newList=[]
    for var in lst:
        if type(var) is not list:
            newList.append(var)
        elif type(var) is list:
            for item in var:
                newList.append(item)
    s = set(); filter(lambda i: not i in s and not s.add(i), newList)
    #print "set is",s
    return s

def create_assign(lst):#create dictionary for value assignment of literals
    newList=[]
    for var in lst:
        if type(var) is not list:
            newList.append(var[0])
        elif type(var) is list:
            for item in var:
                newList.append(item[0])
    assn_dict={}
    assn_dict= OrderedDict.fromkeys(newList)
    #print "Assignment Dict",assn_dict
    return assn_dict
    
def main(argv):#main function to read and output files
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print "error in reading commandlin arguments"
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-i":
            inputfile=arg
    res={}
    s= set()
    f = open(inputfile)
    i = int(f.readline())
    result=[]
    f1=open("CNF_satisfiability.txt","w+")
    while i is not 0:
        sen1 = f.readline()
        lst=remove_connectives(eval(str(sen1)))
        s=create_set(lst)
        res=create_assign(lst)
        result=sat_solver(lst,s,res)
        f1.write(str(result))
        f1.write("\n")
        i=i-1
        

if __name__=="__main__":
    
     main(sys.argv[1:])
