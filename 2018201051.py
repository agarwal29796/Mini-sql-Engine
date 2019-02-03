# -*- coding: utf-8 -*-
import sys
import csv

special_case = False
sc_index2 = -1
sc_index1 = -1
dicto = None

def load_data_meta(dictionary):
    fi = open("metadata.txt", "r")
    check  = False
    current_table = None
    for x in fi:
        x = x.strip()
        if check == False and x == "<begin_table>" :
            check = True
        elif check == True :
            dictionary[x.lower()] = {'attr' : [] , 'data':[], 'oattr' :[], 'oname' : x}
            current_table = x.lower()
            check = False
        elif check == False and x != "<begin_table>" and x != "<end_table>":
            dictionary[current_table]['attr'].append(x.lower())
            dictionary[current_table]['oattr'].append(x)
            
        elif x == "<end_table>":
            current_table = None
        else :
            sys.exit("Proper format required in metadata.txt\n")
            
def read_csv(dictionary):
    for table in dictionary.keys():
        with open(table+".csv") as f :
            for row in csv.reader(f):
                row = list(map(int , row))
                dictionary[table]['data'].append(row)
            
        
def cross_product(dictionary , query_from):
    merged_data_attr  = []
    merged_data = []
    try :
        for table in query_from:
            for attr in  dictionary[table]['attr']:
                merged_data_attr.append(table + "." +attr)
    except :
        sys.exit("error : in accessing the table.")
        
    try :
        temp_data = []
        for table in query_from:
            if len(merged_data) == 0:
                merged_data = dictionary[table]['data']
            else:
                temp_data = []
                for row1 in merged_data:
                    for row2 in dictionary[table]['data']:
                        temp_data.append(row1 + row2)
                merged_data = temp_data
    except :
        sys.exit("error : in accessing table .")

        
    return merged_data_attr , merged_data 
    
def is_true_cond(cond ,attr,attr_splitted, row):
    try :
        col1 = cond[0]
        col2 = cond[2]
        col1_index = None
        col2_index = None
        op = cond[1]
        col2_is_num = False
        
        if col1 in attr :
            col1_index = attr.index(col1)
        elif col1 in attr_splitted and attr_splitted.count(col1) == 1:
            col1_index = attr_splitted.index(col1)
        else:
            sys.exit("error : " + col1 + " is causing issue.")
            
        if col2 in attr :
            col2_index = attr.index(col2)
        elif col2 in attr_splitted :
            if attr_splitted.count(col2) == 1 :
                col2_index = attr_splitted.index(col2)
        else:
            if col2.lstrip("-").isdigit() == True:
                col2_is_num = True
            else:
                sys.exit("error : " + col2 + " is causing issue.")
                
        if col2_is_num == False :
            if op == "=" :
                global special_case
                global sc_index1
                global sc_index2
                special_case = True
                sc_index1 = col1_index
                sc_index2 = col2_index
                return row[col1_index] == row[col2_index]
            elif op == "<=" : return row[col1_index] <= row[col2_index]
            elif op == "<" : return row[col1_index] < row[col2_index]
            elif op == ">=" : return row[col1_index] >= row[col2_index]
            elif op == ">" : return row[col1_index] > row[col2_index]
        elif col2_is_num == True :
            col2 = int(col2)
            if op == "=" :return row[col1_index] == col2
            elif op == "<=" : return row[col1_index] <= col2
            elif op == "<" : return row[col1_index] < col2
            elif op == ">=" : return row[col1_index] >= col2
            elif op == ">" : return row[col1_index] > col2
        else:
            sys.exit("error : in " + str(col2)) 
                        
        
    except :
        sys.exit("error : error in conditional part")
            

def print_header(attr):
    final = []
    for row in attr :
        row = row.split(".")
        table_name = row[0]
        table_attr = row[1]
        for ele in dicto[table_name]['oattr'] :
            if ele.lower() == table_attr :
                final.append(dicto[table_name]['oname'] + "." + ele)
                break
    return ",".join(final)
     
    
def coditional_selection(attr , data , conditions):
    cond1 = conditions
    cond2 = None
    is_many_cond  = False
    refined_data = []
    attr_splitted =  []
    
    for ele in attr :
        attr_splitted.append(ele.split(".")[1].lower())
    try :
        if "and" in conditions:
            cond1 = conditions[0:conditions.index("and")]
            cond2 = conditions[conditions.index("and") + 1 :]
            is_many_cond = True
                               
        elif "or" in conditions:
            cond1 = conditions[0:conditions.index("or")]
            cond2 = conditions[conditions.index("or") + 1 :]
            is_many_cond = True
    except:
        sys.exit("error : Not a proper sql statement")
    
    if is_many_cond == False :
        for row in data :
            if is_true_cond(cond1 ,attr , attr_splitted, row) == True:
                refined_data.append(row)
    else:
        if "and" in conditions :
            for row in data :
                if is_true_cond(cond1 ,attr,attr_splitted, row) == True and is_true_cond(cond2,attr,attr_splitted, row) == True:
                    refined_data.append(row)
        elif "or" in conditions :
            for row in data :
                if is_true_cond(cond1 ,attr, attr_splitted, row) == True or is_true_cond(cond2 ,attr,attr_splitted,  row)== True:
                    refined_data.append(row)
    return refined_data
                   
            
def print_final_result(attr, data, query_items):
    try :
        if(len(query_items) < 1): sys.exit("error : incomplete sql query")
        attr_splitted = []
        for ele in attr :
            attr_splitted.append(ele.split("."))
        #=======================================================    
        if len(query_items) == 1 and query_items[0] == "*":
            if special_case == True:
                del attr[sc_index2]
            print(print_header(attr))
            for row in data :
                if special_case == True:
                    del row[sc_index2]
                print(",".join(map(str,row)))
            return
       #=======================================================
        elif  len(query_items) == 1 and query_items[0].find("(") != -1 and query_items[0].find(")") != -1  :
            op = query_items[0].split("(")[0]
            col_name = query_items[0].split("(")[1].split(")")[0]
            col_index = None

            
            if col_name in attr :
                col_index = attr.index(col_name)
            else :
                for i in range(len(attr_splitted)):
                    li  = attr_splitted[i]
                    if li[1] == col_name:
                        col_name = ".".join(li)
                        col_index = i
                        break
            if col_index == None :
                sys.exit("column " + col_name + " not found.")
                
            col_arr = [row[col_index] for row in data]
            
            print(op + "("+ print_header([col_name]) + ")")
            if op == "sum" :
                print(sum(col_arr))
            elif op == "max":
                print(max(col_arr))
            elif op == "min":
                print(min(col_arr))
            elif op == "average" :
                print(float(sum(col_arr))/len(col_arr))
            else : 
                sys.exit()
            return
    #===================================================
        elif len(query_items) >= 1 :
            cols = query_items
            distinct = False
            if query_items[0] == "distinct":
                cols = query_items[1:]
                distinct = True
            attr_name =  []
            indexs = []
            for col_name in cols :
                col_index =  None
                if col_name in attr :
                    col_index = attr.index(col_name)
                else :
                    repeat = False

                    for i in range(len(attr_splitted)):
                        li  = attr_splitted[i]
                        if li[1] == col_name:
                            if repeat == True:sys.exit()
                            temp_name = ".".join(li)
                            col_index = i
                            repeat = True
                    col_name = temp_name
                    if col_index == None :
                        sys.exit("column " + col_name + " not found.")
                attr_name.append(col_name)
                indexs.append(col_index)
            
            temp_index =  -1    
            if special_case == True :
                if attr[sc_index1] in attr_name and attr[sc_index2] in attr_name:
                    temp_index = attr_name.index(attr[sc_index2])
                    del indexs[temp_index]
                    del attr_name[temp_index]
                    
            print(print_header(attr_name))
            
            final_array = []
            for row in data:
                temp  = [row[index] for index in indexs]
                temp =  ",".join(map(str,temp))
                final_array.append(temp)
            if distinct == True : final_array = list(set(final_array))
            for row in final_array :
            	# row = map(str, row)
                print(row)
        else:
            sys.exit()          

    except :
        sys.exit("error : in selection. ")
                    
                
def process_query(string , dictionary):
    string = str(string).lower()
    
    if string[-1] != ";":
        sys.exit("error : not a proper sql format")
    
    string = string[:-1]
    string = string.replace(",", " ")
    tokens  = string.split(" ")
    query_items = None
    query_from = None
    query_cond = None
    condition =  False
    
    if tokens[0].lower() != "select" :
        sys.exit("error : not a proper sql statement")
    if "from" not in tokens :
        sys.exit("error : not a proper sql statement")
    
    query_items = tokens[1:tokens.index("from")]
    
    if "where" in tokens:
         query_from  = tokens[tokens.index("from") + 1:tokens.index("where")]
         query_cond = tokens[tokens.index("where")+1:]
         condition = True
    else:
        query_from = tokens[tokens.index("from")+1:]
    
    joint_data_attr , joint_data = cross_product(dictionary, query_from)
    if condition == True :
        joint_data = coditional_selection(joint_data_attr , joint_data, query_cond)
    print_final_result(joint_data_attr ,joint_data , query_items)        

    
def main():
    dictionary = {}
    load_data_meta(dictionary)
    global dicto
    dicto = dictionary
    if len(sys.argv) > 2:
        sys.exit("given arguments length exceeds than requirment")
    read_csv(dictionary)
    
    process_query(sys.argv[1] , dictionary)
    
if __name__ == "__main__":
    main()