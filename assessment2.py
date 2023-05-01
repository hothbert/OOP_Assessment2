""" READ ME

To use the menu:
When prompted, type '1' to do an example test or '2' to input your own expression.
If doing an example test, type one of the options from the list shown, for example; 'correctly formatted'.
The expression and results will be outputed.
To do another action type 'y', or to leave type 'n'.

"""

class binary_tree:

    class binary_tree_node:
        __slots__ = 'element', 'left', 'right'

        def __init__(self, element):
            self.element = element 
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None
    
    def add_root(self, node):
        #if a root does not exist, make the current node the root
        if self.root is None:
            self.root = node
            return True

    def create_expression(self, expr):

        if not self.match_brackets(expr):
            print('Not a valid expression, mismatched brackets')
            return
        if not self.operator_missing(expr):
            print('Not a valid expression, missing operator')
            return

        stack = []
        for el in expr: 

            if el not in '1234567890*-+/()':
                print(f'Not a valid Expression, invalid character {el}')
                return

            #creates a node for the operator since for every left bracket encountered, an operator exists
            if el == '(':
                node = self.binary_tree_node(None)
                #sets the current node to a child of the last operator node
                if not self.add_root(node): #the root cannot be a child of another node
                    top = stack[-1]
                    if top.left is None:
                        top.left = node
                    elif top.right is None:
                        top.right = node
                stack.append(node)

            #sets a value to the top operator node
            elif self.is_operator(el):
                try:
                    node = stack[-1]
                except: #if brackets are missing there is nothing in the stack list to assign a value to and an exception will occur
                    print('Not a valid expression, missing brackets')
                    return
                if node.element is not None: #if a value has already been assigned to the operator node
                    print('Not a valid expression, too many operators')
                    return
                node.element = el
                
            elif el == ')':
                stack.pop() #removes last operator node from stack since all attributes have been assigned to it
                
            #if the element is a number create a new operand node
            else:
                node = self.binary_tree_node(el)
                try:
                    top = stack[-1]
                except:
                    print('Not a valid expression, missing brackets')
                    return
                if top.left is None:
                    top.left = node
                elif top.right is None:
                    top.right = node
                else: #the operator already has both right and left children assigned
                    print('Not a valid expression, too many operands')
                    return

        if not self.operand_missing(self.root):
            print('Not a valid expression, missing operand')
            return

        self.outputs() #only prints outputs if all tests are passed
            
    def outputs(self):
        print("Result:")
        print(self.calculate_expression(self.root))
        print("Postorder:")
        self.postorder(self.root)
        print('\nPreorder:')
        self.preorder(self.root)
        print('\nBreath First:')
        self.breath_first()
        print('\nVisual of Tree:\n')
        self.print_tree(self.root)

    def calculate_expression(self, node):
        #source: www.techiedelight.com/evaluate-binary-expression-tree/ (no author mentioned)
        if node is None:
            return 0

        if self.is_leaf(node): #if the node is a leaf, convert to a number
            return float(node.element)

        #recursively finds operands
        x1 = self.calculate_expression(node.left) 
        x2 = self.calculate_expression(node.right)

        return self.maths(node.element, x1, x2) #finds answer to expression for every left and right child

    def maths(self, operator, x1, x2): #performs operation on numbers
        #source: ^
        if operator == '*':
            return x1*x2
        if operator == '+':
            return x1+x2
        if operator == '-':
            return x1-x2
        if operator == '/':
            return x1/x2
    
    def breath_first(self): #nodes are visited row by row
    # source: www.geeksforgeeks.org/level-order-tree-traversal/ (author: Nikhil Kumar Singh)
        height = self.depth(self.root)
        for i in range(1, height+1): #traverses rows
            self.print_level(self.root, i)

    def print_level(self, node, level):
    # source: ^
        if node is None: #if a node has no children nothing is printed
            return
        #recursively visits each child of a node until level reaches 1, then prints the node
        #the higher level is, the more rows it traverses through from the root to find the desired row that has not been printed yet
        elif level==1:          
            print(node.element, end = '') 
        else:
            self.print_level(node.left, level-1)
            self.print_level(node.right, level-1)

    def depth(self, node): #calculates the height of the tree
    # source: ^
    #finds the longest sequence of children and counts 1 for each visited
        if node is None:
            return 0
        leftH = self.depth(node.left)
        rightH = self.depth(node.right)
        return max(leftH, rightH) +1 #changed source code here to reduce number of lines (previously was an if statement)

    def preorder(self, node): #nodes are visited before their decendents
        if node is not None:
            print(node.element, end='')
            self.preorder(node.left)
            self.preorder(node.right)

    def postorder(self, node): #nodes are visited after their decendents
        if node is not None:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.element, end='')

    def print_tree(self, node, level=0):
        #source: stackoverflow.com/questions/34012886/print-binary-tree-level-by-level-in-python (authors: yozn and Hack5 on stackoverflow)
        if node is not None:
            self.print_tree(node.right, level+1) #changed source code here to flip left and right so tree displays the correct way round
            print(' '*5*level, f'\033[1;32m{node.element}', '\x1b[0m') #changed source code to remove arrows and make it green because that looks prettier
            self.print_tree(node.left, level+1)
        
    def is_leaf(self, node): #if a node has no children then its a leaf
        return node.left is None and node.right is None

    def is_operator(self, el):
        operators = '+-*/'
        return el in operators

    def match_brackets(self, expr):
        brackets = []
        for el in expr:
            if el == '(':
                brackets.append(el) #adds bracket to list
            if el == ')':
                if len(brackets) == 0: #if there is no corresponding left bracket return false
                    return False
                else:
                    brackets.pop() #remove from list since matching bracket found
        if len(brackets) != 0: #if there is an extra left bracket return false
            return False
        return True

    def operator_missing(self, expr):
        operator_count = 0
        bracket_count = 0
        for el in expr:
            if self.is_operator(el):
                operator_count+=1
            elif el == '(':
                bracket_count+=1
        if operator_count < bracket_count: #there should be the same number of brackets as operator symbols in a valid expression
            return False
        return True

    def operand_missing(self, node): #function could work for any missing child but operator_missing has already been executed
        if node is not None:
            if self.is_operator(node.element): #only operators need to have children
                if self.is_leaf(node):
                    return False
                else:
                    if not self.operand_missing(node.left) or not self.operand_missing(node.right): #recursively finds missing operands
                        return False
                return True
            return True

def menu():
    answer = input('\nWould you like to perform a test or input your own expression? [enter 1 or 2]\n')
    while answer != '1' and answer != '2': #input validation
        answer = input('Please enter only "1" or "2".\n')

    tests = ['correctly formatted', 'mismatched brackets', 'invalid character', 'missing operator', 'too many operators', 'missing operand', 'too many operands', 'missing brackets']
    expressions = ['((((5+2)*(2-1))/((2+9)+((7-2)-1)))*8)', '((3+5)', '(3+g)', '(((2+3)*(4*5))+(1(2+3)))', '(1+2+)', '((1+)*(1-5))', '(1+23)', '(4*2)/(3-9)']

    if answer == '1':
        test_type = input(f'Which test would you like to perform?\n{", ".join(tests)}\n') # .join gets rid of brackets and quotes on list
        while test_type not in tests: #input validation
            test_type = input('That is not a valid test type, try again.\n')
        for i in range(0, 8): #loops through tests list to find a match
            if test_type == tests[i]:
                print('\nExpression:', expressions[i])
                tree = binary_tree() #creates a tree
                tree.create_expression(expressions[i])

    if answer == '2':
        user_test = input('Please enter an expression formatted like (X?Y).\n')
        tree = binary_tree()
        tree.create_expression(user_test)

    user_input = input('\nWould you like to perform another action? [y/n]\n') #lets the user do another test or input
    while user_input != 'y' and user_input != 'n':
        user_input = input('Please enter only "y" or "n".\n')
    if user_input == 'y':
        menu()
    else:
        print('\033[1;32mgoodbye :( \x1b[0m')

print('\033[1;32mWELCOME! :) \x1b[0m')
menu()