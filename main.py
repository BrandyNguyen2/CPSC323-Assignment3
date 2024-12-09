# Programmers: Salvador Delgado, Brandy Nguyen, Landon Patam, & Nicholas Reeves
import re, sys
# Lists of Seperators, Operators and Keywords for later reference
separators = ["(", ")", ";", "{", "}", "[", "]", ",", "@"]
operators = ["+", "-", "*", "/", "=", "==", "!=", "<", ">", ">=", "<=", "and", "or", "not"]
keywords = ["while", "if", "for", "fi", "integer", "boolean", "real", "put", "function", "return", "get", "true", "false", "else", "elif", "main"]


# CHANGE THESE 2 TO CHANGE INPUT / OUTPUT FILES
Input_file = "input.txt"
Output_file = "output.txt"


# Takes text from input file and converts into a string with no spaces
with open(Input_file, "r" ) as file:
     input = file.read()




# Removes comments from the input string
input = re.sub(r"\[\*.*?\*\]", "", input)

#print (input)


# Instantiating list for Tokens
tokens = []

# Loops through the input_nospaces and seperates each token and places them into a list
temp_token = ""
    
for j in range(len(input)):
    i = input[j]
    if temp_token in operators:
            tokens.append(temp_token)
            temp_token = ""
    if (i in separators) or (i in operators):         
        if len(temp_token) != 0:
          tokens.append(temp_token)
          temp_token = ""
        tokens.append(i)
    elif i == "\n":
         tokens.append(temp_token)
         temp_token = ""
         tokens.append("\n")
    elif i == " ":
         tokens.append(temp_token)
         temp_token = ""
    else:
        temp_token += i


# Removes spaces and empty tokens from list
tokens = [i for i in tokens if i != "" and i != " "]


# Deals with edge cases of "<" and ">" followed by "="
index = 0
while index < len(tokens):
    i = tokens[index]

    if i == "<":
        if index + 1 < len(tokens) and tokens[index + 1] == "=":
            tokens[index] = "<="
            del tokens[index + 1]

    elif i == ">":
        if index + 1 < len(tokens) and tokens[index + 1] == "=":
            tokens[index] = ">="
            del tokens[index + 1]

    elif i == "=":
        if index + 1 < len(tokens) and tokens[index + 1] == "=":
            tokens[index] = "=="
            del tokens[index + 1]
     
    elif i == "!":
         if index + 1 < len(tokens) and tokens[index + 1] == "=":
              tokens[index] = "!="
              del tokens[index + 1]

    index += 1


# Removes comments from the tokens list


first_index = None
last_index = None
for i in range(len(tokens)):
     if tokens[i] == "[" and tokens[i+1] == "*":
          #print ("Found comment" + tokens[i] + tokens[i+1] )
          first_index = i
     elif tokens[i] == "*" and tokens[i+1] == "]":
          last_index = i + 1
if first_index != None and last_index != None:
     del tokens[first_index: last_index+1]



if tokens[0] == "\n":
     del tokens[0]




#print(tokens)


# FSM for Integer
def isInteger(token):
     Integer_dictionary = {
     1 : [1, 2],
     2 : [2, 2]
     }

     state = 1
     accepting_states = [1]

     for i in token:
          if i.isdigit():
               state = Integer_dictionary[state][0]
          else:
               state = 2   
                         
               # checks if final state is in accepting state
     if state in accepting_states:
          return True
     else:
          return False
     

# FSM for Real

def isReal(token):
     real_dictionary = {
     1 : [2, 3],
     2 : [2, 4],
     3 : [3, 3],
     4 : [5, 3],
     5 : [5, 3],

     }

     state = 1
     accepting_states = [5]

     for i in token:
          if i.isdigit():
               state = real_dictionary[state][0]
          elif i == ".":
               state = real_dictionary[state][1]
          else:
               state = 3
                     
                         
               # checks if final state is in accepting state
     if state in accepting_states:
          return True
     else:
          return False


# FSM for Identifer
def isIdentifier(token):
     Identifier_dictionary = {
     1 : [2, 3],
     2 : [4, 5],
     3 : [3, 3],
     4 : [4, 5],
     5 : [6, 5],
     6 : [7, 5],
     7 : [6, 5]

     }

     state = 1
     accepting_states = [2,4,6,7]

     for i in token:
          if i.isalpha():
               state = Identifier_dictionary[state][0]
          elif i.isdigit():
               state = Identifier_dictionary[state][1]
          else:
               state = 3
                    
                    
          # checks if final state is in accepting state
     if state in accepting_states and token not in keywords:
          return True
     else:
          return False

# PART OF ASSIGNMENT #
declaration_type = ""
memory_tracker = 9000
temp_symbol_table = {}
symbol_table = {}
instr_table = {}
instr_table_index = 1 
change_table = True
addr = 0
jumpstack = []
op = ""
#symbol_table["max"] = {"memory_location": 9001, "type":"integer"}
#instr_table[index] = {"Op" : PUSHM, "Oprnd : 9001"}


def get_address(variable):
    return symbol_table[variable]["memory_location"]


def gen_instr(instruction, address):
    global instr_table_index
    instr_table[instr_table_index] = {"Op" : instruction,"Oprnd" : address}
    instr_table_index += 1

def back_patch(jump_addr):
    addr = jumpstack.pop()
    instr_table[addr]["Oprnd"] = jump_addr








# SYNTACTICAL ANALYZER PORTION

#print(isIdentifier("true"))


with open (Output_file, "w") as file:
       file.write(f'Output:\nToken{" "*17}{"Lexeme":<23}{"Production Rules"}\n{"-"*9}{" "*13}{"-"*8}{" "*15}{"-"*20}\n')

switch = False
AddToList = True

tokens_index = 0
line_number = 1
token = tokens[tokens_index]
rules_used = []
errors = []
save = ""

def lexer():
    global tokens_index, token, rules_used, line_number
    token_type = ""




    if token in operators:
          token_type ='Operator' 
    elif token in separators:
                token_type = 'Separator'
    elif token in keywords:
                token_type = 'Keyword'
    elif isReal(token):
                token_type = 'Real'
    elif isInteger(token):
                token_type = 'Integer'
    elif isIdentifier(token):
                token_type = 'Identifier'
    else:
                token_type = 'Unknown'

# UNCOMMENT THESE 2 LINES AND LINES 236 - 237 TO REENABLE THE PRODUCTION RULES


    with open(Output_file, "a") as file:
        if len(errors) == 0:
                file.write(f"{token_type:<22}{token:<23}{', '.join(rules_used)}\n")
                rules_used = []
                tokens_index += 1
                if tokens_index < len(tokens):
                    token = tokens[tokens_index]

        if token == "\n":
            while token == "\n":
                tokens_index += 1
                if tokens_index < len(tokens):
                    token = tokens[tokens_index]
                    line_number += 1
                else:
                    break
                    





def Error():
     with open(Output_file, "a") as file:
          file.write(f"\nERROR ON LINE {line_number} - {errors[0]}")


def Rat24F():
    if AddToList:
        rules_used.append("Rat24F")

    if switch:
          print(token + " " + "Rat24F")

    if token == "@":
        lexer()
        OptDeclarationList()
        StatementList()
        if token == "@":
            lexer()
        else:
            errors.append("EXPECTED CLOSING @")
            Error()
            sys.exit()
    else:
        errors.append("EXPECTED OPENING @")
        Error()
        sys.exit()



  

def Qualifier():
    global declaration_type, memory_tracker
    if switch:
        print(token + " " + "Qualifier")
    if AddToList:
          rules_used.append("Qualifier")
    if (token in ["integer", "boolean", "real"]):
        declaration_type = token
        lexer()

def Body():
    if switch:
        print(token + " " + "Body")
    if AddToList:
        rules_used.append("Body")

    if token == "{":
        lexer()
        StatementList()
        if token == "}":
                lexer()
        else:
            errors.append("EXPECTED }")
            Error()
            sys.exit()
    else:
        errors.append("EXPECTED {")
        Error()
        sys.exit()

def OptDeclarationList():
    global declaration_type, symbol_table, change_table
    
    if switch:
        print(token + " " + "OptDeclarationList")
    if AddToList:
         rules_used.append("OptDeclarationList")
         

         DeclarationList()
         if change_table == True:
            symbol_table = temp_symbol_table
            change_table = False
    else:
        Empty()
    

def DeclarationList():
    if switch:
        print(token + " " + "DeclarationList")
    if AddToList:
         rules_used.append("DeclarationList")
    Declaration()
    if token == ";":
        lexer()
        DeclarationList_prime()

def DeclarationList_prime():
    global symbol_table, temp_symbol_table
    if switch:
        print(token + " " + "DeclarationList_prime")
    if AddToList:
        rules_used.append("DeclarationList_prime")
        
    if token in {"integer", "boolean", "real"}:
        DeclarationList()
    else:
         Empty()
         


def Declaration():
    if switch:
        print(token + " " + "Declaration")
    if AddToList:
        rules_used.append("Declaration")
    Qualifier()
    IDs()

def IDs():
    global memory_tracker
    global declaration_type
    if switch:
        print(token + " " + "IDs")
    if AddToList:
        rules_used.append("IDs")
    if isIdentifier(token):
        if token not in temp_symbol_table:
            if change_table == True:
                temp_symbol_table[token] = {"memory_location": memory_tracker, "type": declaration_type}
                memory_tracker += 1
        lexer()
        IDs_prime()

def IDs_prime():
    if switch:
        print(token + " " + "IDs_prime")
    if AddToList:
        rules_used.append("IDs_prime")
    if token == ",":
        lexer()
        IDs()
    else:
        IDs()
    


def StatementList():
    if switch:
        print(token + " " + "StatementList")
    if AddToList:
        rules_used.append("StatementList")
    Statement()
    StatementList_prime()

def StatementList_prime():
    if switch:
        print(token + " " + "StatementList_prime")
    if AddToList:
        rules_used.append("StatementList_prime")
        if token in {"if", "return", "put", "get", "while"} or isIdentifier(token):
            StatementList()
        else:
            Empty()

def Statement():
    if switch:
        print(token + " " + "Statement")
    if AddToList:
        rules_used.append("Statement")

    if token == '{':
        Compound()
    elif token == 'if':
        If()
    elif token == 'return':
        Return()
    elif token == 'put':
        Print()
    elif token == 'get':
        Scan()
    elif token == 'while':
        While()
    elif isIdentifier(token):
        Assign()
    else:
        errors.append("MISSING STATEMENT")
        Error()
        sys.exit()
        

def Compound():
    if switch:
        print(token + " " + "Compound")
    if AddToList:
        rules_used.append("Compound")
        if token == "{":
             lexer()
             StatementList()
             if token == "}":
                  lexer()
             else:
                  errors.append("EXPECTED }")
                  Error()
                  sys.exit()
        else:
             errors.append("EXPECTED {")
             Error()
             sys.exit()

def Assign():
    global memory_tracker, save
    if switch:
        print(token + " " + "Assign")
    if AddToList:
        rules_used.append("Assign")
        
        
    if isIdentifier(token):
        if token not in symbol_table:
            errors.append("ERROR - Variable not declared")
            Error()
            sys.exit()
        save = token
        #print(save)
        lexer()
        if token == '=':
            lexer()
            Expression()
            gen_instr("POPM", get_address(save))
            if token == ';':
                lexer()
            else:
                 errors.append("EXPECTED ;")
                 Error()
                 sys.exit()
        else:
             errors.append("EXPECTED =")
             Error()
             sys.exit()

def If():
    if switch:
        print(token + " " + "If")
    if AddToList:
        rules_used.append("If")
    if token == "if":
        lexer()
        if token == "(":
            lexer()
            Condition()
            if token == ")":
                lexer()
                Statement()
                if token != "else":
                    back_patch(instr_table_index)
                else:
                    back_patch(instr_table_index+1)
                If_prime()
                gen_instr("LABEL", "nil")
            else:
                errors.append("EXPECTED )")
                Error()
                sys.exit()
        else:
            errors.append("EXPECTED ( ")
            Error()
            sys.exit()


def If_prime():
    if switch:
        print("If_prime")
    if AddToList:
        rules_used.append("If_prime")


    if token == "fi":
        lexer()
    elif token == "else":
         gen_instr("JUMPZ","nil")
         jumpstack.append(instr_table_index-1)
         lexer()
         gen_instr("LABEL", "nil")
         Statement()
         back_patch(instr_table_index)
         if token == "fi":
            lexer()
         else:
            errors.append("EXPECTED fi")
            Error()
            sys.exit()
    else:
        errors.append("EXPECTED fi")
        Error()
        sys.exit()

def Return():
    if switch:
        print("Return")
    if AddToList:
        rules_used.append("Return")
        if token == "return":
             lexer()
             Return_prime()
            

def Return_prime():
    if switch:
        print("Return_prime")
    if AddToList:
        rules_used.append("Return_prime")
    if token == ";":
         lexer()
    else:
         Expression()
         if token == ";":
            lexer()
         else:
              errors.append("EXPECTED ;")
              Error()
              sys.exit()


def Print():
    global temp_token
    if switch:
        print("Print")
    if AddToList:
        rules_used.append("Print")
    if token == "put":
        lexer()
        if token == "(":
            lexer()
            temp_token = token
            Expression()
            if token == ")":
                lexer()
                if token == ";":
                    lexer()
                    gen_instr("STDOUT", "nil")
                else:
                    errors.append("EXPECTED ;")
                    Error()
                    sys.exit()
            else:
                 errors.append("EXPECTED )")
                 Error()
                 sys.exit()
        else:
             errors.append("EXPECTED (")
             Error()
             sys.exit()
                

def Scan():
    if switch:
        print("Scan")
    if AddToList:
        rules_used.append("Scan")
    if token == "get":
         lexer()
         if token == "(":
              lexer()
              gen_instr("STDIN", "nil")
              gen_instr("POPM", get_address(token))
              IDs()
              if token == ")":
                   lexer()
                   if token == ";":
                       lexer()
                   else:
                        errors.append("EXPECTED ;")
                        Error()
                        sys.exit()
              else:
                   errors.append("EXPECTED (")
                   Error()
                   sys.exit()
         else:
             errors.append("EXPECTED (")
             Error()
             sys.exit()
             

def While():
    global addr
    if switch:
        print("While")
    if AddToList:
        rules_used.append("While")


    if token == "while":
        addr = instr_table_index
        gen_instr("LABEL", "nil")
        lexer()
        if token == "(":
            lexer()
            Condition()
            if token == ")":
                lexer()
                Statement()
                gen_instr("JUMP", addr)
                back_patch(instr_table_index)
            else:
                 errors.append("EXPECTED )")
                 Error()
                 sys.exit()
        else:
             errors.append("EXPECTED (")
             Error()
             sys.exit()

def Condition():
    global op
    if switch:
        print("Condition")
    if AddToList:
        rules_used.append("Condition")
    Expression()
    if token in ["==", "!=", "<", ">","<=", "=>"]:
        op = token
        lexer()
        Expression()
    if op == "<":
        gen_instr("LES", "nil")
        jumpstack.append(instr_table_index)
        gen_instr("JUMPZ", "nil")
    elif op == ">":
        gen_instr("GRT", "nil")
        jumpstack.append(instr_table_index)
        gen_instr("JUMPZ", "nil")
    elif op == "==":
        gen_instr("EQU", "nil")
        jumpstack.append(instr_table_index)
        gen_instr("JUMPZ", "nil")
    elif op == "!=":
        gen_instr("NEQ", "nil")
        jumpstack.append(instr_table_index)
        gen_instr("JUMPZ", "nil")
    elif op == "=>":
        gen_instr("GEQ", "nil")
        jumpstack.append(instr_table_index)
        gen_instr("JUMPZ", "nil")
    elif op == "<=":
        gen_instr("LEQ", "nil")
        jumpstack.append(instr_table_index)
        gen_instr("JUMPZ", "nil")
    Relop()
    Expression()

def Relop():
    if switch:
        print("Relop")
    if AddToList:
        rules_used.append("Relop")
        if token == "==":
             lexer()
        elif token == "!=":
             lexer()
        elif token =="<":
             lexer()
        elif token == ">":
             lexer()
        elif token == "<=":
             lexer()
        elif token == "=>":
             lexer()


def Expression():
    if switch:
        print(token + " " + "Expression")
    if AddToList:
        rules_used.append("Expression")
    Term()
    ExpressionPrime()


def ExpressionPrime():
    if switch:
        print(token + " " + "ExpressionPrime")
    if AddToList:
        rules_used.append("ExpressionPrime")
    if token == "+":
         lexer()
         #gen_instr("PUSHI", token)
         Term()
         #gen_instr("PUSHI", token)
         gen_instr("ADD", "nil")
         ExpressionPrime()
    elif token == "-":
         lexer()
         #gen_instr("PUSHI", token)
         Term()
         #gen_instr("PUSHI", token)
         gen_instr("SUB", "nil")
         ExpressionPrime()
    else:
        Term()



def Term():
    if switch:
        print(token + " " + "Term")
    if AddToList:
        rules_used.append("Term")

    Factor()
    TermPrime()
    

def TermPrime():
    if switch:
        print(token + " " + "TermPrime")
    if AddToList:
        rules_used.append("TermPrime")
    if token == "*":
         lexer()
         Factor()
         gen_instr("MUL", "nil")
         TermPrime()
    elif token == "/":
         lexer()
         Factor()
         gen_instr("DIV", "nil")
         TermPrime()


def Factor():
    global save
    if switch:
        print(token + " " + "Factor")
    if AddToList:
        rules_used.append("Factor")

    #if token == "-":
    if isIdentifier(token): #and token not in keywords:
        if save != "":
            if symbol_table[token]['type'] != symbol_table[save]['type']:
                errors.append("ERROR NO TYPE CASTING ALLOWED")
                Error()
                sys.exit()
        gen_instr("PUSHM", get_address(token))

        lexer()
        Primary()
    else:
         Primary()



def Primary():
    global save
    if switch:
        print("Primary")
    if AddToList:
        rules_used.append("Primary")
        
        
    if  token == "true":
        if save != "":
            if symbol_table[save]['type'] != "boolean":
                errors.append("INVALID ASSIGNMENT")
                Error()
                sys.exit()
        lexer()
        #print(symbol_table)
    elif token == "false":
        lexer()
    elif isIdentifier(token):
         lexer()
         if token == "(":
              IDs()
              if token == ")":
                   lexer()
                   
            
    elif isInteger(token) or isReal(token):
        #print(save)
        if save != "":
            if symbol_table[save]['type'] != "integer":
                errors.append("INVALID ASSIGNMENT")
                Error()
                sys.exit()
        gen_instr("PUSHI", token)
        lexer()
    elif token == "(":
         lexer()
         Expression()
         if token == ")":
              lexer()
    elif isReal(token):
         lexer()
    #elif token == "true":
    #     lexer()
    #elif token == "false":
    #     lexer()


def Empty():
    if switch:
         print("Empty")
    if AddToList:
         rules_used.append("Empty")
        


Rat24F()




with open(Output_file, "w") as file:
        
    file.write(f"\nAssembly code listing\n----------------------\n\n")
    for i in instr_table:
        if instr_table[i]['Oprnd'] == "nil":
            instr_table[i]['Oprnd'] = ""
        file.write(f"{i:<2}  {instr_table[i]['Op']:<8}{instr_table[i]['Oprnd']}\n")
        
        
    file.write("\n")
    file.write(f"\nSymbol Table\n-----------------------\n\n{'Identifier':<15}{'Memory Location':<22}  Type\n\n")
    for i in symbol_table:
        file.write(f"{i:<15}{symbol_table[i]['memory_location']:<24}{symbol_table[i]['type']}\n")
        
        


#for key, value in instr_table.items():
#    print(f"{key}: {value}")


