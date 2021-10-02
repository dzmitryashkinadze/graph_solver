# Library for float division
from __future__ import division
# OS path library
import os
# Regular expression library
import re
# Library used for scientific calculations (wolfram alpha in python)
import sympy as sy
# Library used for numeric transformation (sorting)
import numpy as np
# Library used for unit interconversions
import pint
# Library for graphs
import networkx as nx
# Library that allowed to make deepcopies
from copy import deepcopy


class GraphSolver():
    # Initialization of the graph either through the
    # name of the model or though the saved object
    def __init__(self, Name = None, Graph = None,
                 Model = None, Trace = False,
                 Debug = False):
        # create a registry object for calculations with units
        self.ureg = pint.UnitRegistry()
        # if both model name and graph object given return an exception
        if Model and Graph:
            raise Exception('Please, initialize the model either \
                             with an existing graph or with a template model!')
        # if neither model name nor a graph object given return an exception
        elif not Model and not Graph:
            raise Exception('Please, initialize the model either \
                             with an existing graph or with a template model!')
        # initialize model with its name
        elif Model:
            self.Path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', Model + '.graphml')
            self.G = nx.read_graphml(self.Path)
            self.G = self.PrepareGAfterImport(self.G)
        # initialize model with premade object
        elif Graph:
            self.G = Graph
            self.G = self.PrepareGAfterImport(self.G)
        # add a name to the graphsover object
        if Name:
            self.G.graph['name'] = Name
        # set the global variables according to the input
        self.Initialized_G_eq = False
        self.Trace = Trace
        self.Debug = Debug
        self.SymmetryCount = 0
        self.error = {}


    # Import of solution to the graph through API
    def Import_Solution(self, VarName, Value, Unit):
        VarNode = self.Find_Node_By_Var_Name(VarName)
        base_unit = 1*self.ureg[Unit].to_base_units()
        base_unit_factor = base_unit.magnitude
        # Check the unit
        if base_unit.units != self.G.nodes[VarNode]['unit'].units:
            raise Exception('Wrong Import: variable unit', VarName, Value, Unit)
        self.G.nodes[VarNode]['ExpectedValue'] = float(Value) * base_unit_factor


    # Import of data to the graph through API
    def Import(self, VarName, Value, Unit):
        VarNode = self.Find_Node_By_Var_Name(VarName)
        base_unit = 1*self.ureg[Unit].to_base_units()
        base_unit_factor = base_unit.magnitude
        # Check the unit
        if base_unit.units != self.G.nodes[VarNode]['unit'].units:
            raise Exception('Wrong Import: variable unit', VarName, Value, Unit)
        self.G.nodes[VarNode]['value'] = float(Value) * base_unit_factor
        self.G.nodes[VarNode]['known'] = True


    def CheckVarCalc(self, id, result, value):
        validity = True
        error = {}
        if result['status'] != 'solved':
            validity = False
            error = {
                'message': 'Graph was not solved',
                'node_id': None,
                'type': None
            }
        elif round(result['value'],2) != value:
            validity = False
            error = {
                'message': 'Wrong variable value',
                'node_id': id,
                'type': result['Value']
            }
        return validity, error


    # Check incoming graph from the front end
    def Check(self):
        # Find all variables and equations to be Found
        VariablesToBeFound = {}
        EquationsToBeParsed = {}
        result = {'solved': True}
        for i in self.G.nodes():
            if 'ExpectedValue' in self.G.nodes[i]:
                VariablesToBeFound[i] = self.G.nodes[i]['ExpectedValue']
            if 'ExpectedParsing' in self.G.nodes[i]:
                EquationsToBeParsed[i] = self.G.nodes[i]['ExpectedParsing']
        SolvedCorrect = True
        for i in VariablesToBeFound.keys():
            if result['solved']:
                VarSolution = self.Interactive_Solving_Hidden(VarNode=i)
                if self.error == {}:
                    CheckResult = self.CheckVarCalc(i,VarSolution,float(VariablesToBeFound[i]))
                    if not CheckResult[0]:
                        result['solved'] = False
                        result['error'] = CheckResult[1]
                else:
                    result['solved'] = False
                    result['error'] = self.error
        for i in EquationsToBeParsed.keys():
            if result['solved']:
                parsing = str(self.Parse_Eq(i,Ignore_List=[])[0])
                # Remove white spaces
                parsing = ''.join(parsing.split())
                if self.error == {}:
                    if parsing != EquationsToBeParsed[i]:
                        result['solved'] = False
                        result['error'] = {
                            'message': 'Wrong equation parsing',
                            'node_id': i,
                            'type': parsing
                        }
                else:
                    result['solved'] = False
                    result['error'] = self.error
        return result


    # Figure out the base for power gate
    def preparePG(self, Node, Graph):
        #power = Graph.nodes[Node]['power']
        for i in Graph.in_edges(Node):
            if 'PI' in Graph.edges[i]:
                Graph.nodes[Node]['power'] = i[0]
            else:
                Graph.nodes[Node]['base'] = i[0]
        return Graph


    # Prepare the graph after import from graphml
    def PrepareGAfterImport(self, Graph):
        # PowerGates to be corrected
        PGcontainer = []
        # Remapping to change node names from str to int
        Remaping = {}
        for i in range(len(Graph)):
            Remaping[str(i)] = i
        Graph = nx.relabel_nodes(Graph, Remaping)
        # Container for variable names
        VarNameContainer = []
        # Add the default attributes to the variable and
        # functionalize the string attributes such as unit and SY_Var
        for i in Graph.nodes(data = 'type'):
            if i[1] == 'PG':
                PGcontainer.append(i[0])
            if i[1] == 'V':
                unit_text = Graph.nodes[i[0]]['unit']
                base_unit = 1*self.ureg[unit_text].to_base_units()
                base_unit_text = str(base_unit.units)
                base_unit_factor = base_unit.magnitude
                Graph.nodes[i[0]]['unit'] = 1*self.ureg[base_unit_text]
                if 'ExpectedValue' in Graph.nodes[i[0]]:
                    value = float(Graph.nodes[i[0]]['ExpectedValue'])
                    Graph.nodes[i[0]]['ExpectedValue'] = value * base_unit_factor
                if ('known' in Graph.nodes[i[0]]) and Graph.nodes[i[0]]['known']:
                    value = float(Graph.nodes[i[0]]['value'])
                    Graph.nodes[i[0]]['value'] = value * base_unit_factor
                else:
                    Graph.nodes[i[0]]['known'] = False
                SY_Var_text = Graph.nodes[i[0]]['SY_Var']
                while SY_Var_text in VarNameContainer:
                    SY_Var_text += '*'
                Graph.nodes[i[0]]['SY_Var'] = sy.Symbol(SY_Var_text)
                VarNameContainer.append(SY_Var_text)
            if i[1] == 'C':
                unit_text = Graph.nodes[i[0]]['unit']
                base_unit = 1*self.ureg[unit_text].to_base_units()
                base_unit_text = str(base_unit.units)
                base_unit_factor = base_unit.magnitude
                Graph.nodes[i[0]]['unit'] = 1*self.ureg[base_unit_text]
                value = float(Graph.nodes[i[0]]['value'])
                Graph.nodes[i[0]]['value'] = value * base_unit_factor
        for i in PGcontainer:
            Graph = self.preparePG(i, Graph)
        return Graph



    # Initialization of G_eq():
    def Make_G_Eq(self):
        self.G_eq = nx.Graph()
        # Add all of the nodes
        for i in self.G.nodes(data = 'type'):
            if (i[1] == 'E') or ((i[1] == 'V') and not self.G.nodes[i[0]]['known']):
                self.G_eq.add_node(i[0], type = i[1])
        # Add the edges
        for i in self.G_eq.nodes(data = 'type'):
            if i[1] == 'V':
                Eq_List = self.Get_Connected_Eq(i[0],
                                                i[0],
                                                Ignore_List=[],
                                                Eq_List=[])
                for j in Eq_List:
                    self.G_eq.add_edge(i[0],j)



    #Find the node by name
    def Find_Node_By_Var_Name(self, VarName):
        VarNode = None
        # Iterate through the variables to find the variable with particular name
        for (i, j) in self.G.nodes(data='type'):
            if (VarNode == None) and \
               (j == 'V') and \
               (self.G.nodes[i]['SY_Var'].name == VarName):
                VarNode = i
        return VarNode



    # Evaluation of the node
    def Evaluate(self, NodeNum, Ignore_List = []):
        # Parse the equation and evaluate it
        Value = self.Parse_Eq(NodeNum, Ignore_List)[0]
        # If equation can be evaluated to integer then return true
        if isinstance(Value, int):
            return Value, True
        else:
            return Value, False



    # RECURRENT FUNCTION!
    # Check for the zero equation (equation with only one branch)
    # The idea is to represent equation as 0 = (a1^p1)*(a2^p2)*(a3^p3)...
    # In case if the whole equation is determined and
    # only one power value is positive then the base corresponding to
    # the positive power must be 0
    # a and p values with be stored in the list of tupels [(a1,p1),...]
    # called Multiplication_List
    def Zero_Equation(self, Start, NodeNum, Ignore_List = [],
                      Multiplication_List = [], Power = 1):
        AllowedTypes = ['MG','ABS','SIN','COS']
        Ignore_List.append(NodeNum)
        Determined = True
        # If 0 = a ^ b, then evaluate b and add it to the multiplication list
        if self.G.nodes[NodeNum]['type'] == 'PG':
            if not (self.G.nodes[NodeNum]['base'] in Ignore_List):
                LocalPower = self.Evaluate(self.G.nodes[NodeNum]['power'],
                                           Ignore_List = [NodeNum])
                if LocalPower[1]:
                    PowerEdge = self.G.edges[self.G.nodes[NodeNum]['power'],NodeNum]
                    TruePower = LocalPower[0] * PowerEdge['weight']
                    Multiplication_List = self.Zero_Equation(Start,
                                                             self.G.nodes[NodeNum]['base'],
                                                             Ignore_List,
                                                             Multiplication_List,
                                                             Power*TruePower)
                else: Determined = False
        elif self.G.nodes[NodeNum]['type'] in AllowedTypes:
            for i in self.G.predecessors(NodeNum):
                if not i in Ignore_List:
                    Multiplication_List = self.Zero_Equation(Start, i,
                                                             Ignore_List,
                                                             Multiplication_List,
                                                             Power)
        elif (self.G.nodes[NodeNum]['type'] == 'V') and \
             (self.G.nodes[NodeNum]['known'] == False):
            Multiplication_List.append([NodeNum, Power])
        if (NodeNum == Start) and Determined:
            Order = 0
            ZeroNode = 0
            for i in Multiplication_List:
                if i[1]>0:
                    Order += 1
                    ZeroNode = i[0]
            if Order == 1:
                if self.Debug:
                    print('Set the node', ZeroNode, \
                          'to 0 due to the zero equaiton', Start)
                self.Update_Var_Solution(ZeroNode, 0, 0)
        return Multiplication_List



    # Looping through the nodes to trigger the zero_import
    # function upon imported zero variables.
    def Zero_Import_Wrapper(self):
        NodeList = []
        for i in self.G:
            if (self.G.nodes[i]['type'] == 'V') and self.G.nodes[i]['known'] and \
               (self.G.nodes[i]['value'] == 0):
               NodeList.append(i)
        for i in NodeList:
            if self.Debug:
                print('Initialized the zero import algorithm for the node', i)
            self.Zero_Import(i, i, Ignore_List = [], Remove_List = [])



    # RECURRENT FUNCTION!
    # Dealing with importing of a zero to avoid problems with division through
    # zero and autofilling of zero variables that can be implied by imported zero variable
    # Instruction 1: At start -> look for all of the neighbors of the zero node
    # Instruction 2: At multiplication gates and abs gates -> look at the node
    # in the direction of the equation (specified as 'eqNode')
    # Instruction 3: At power gate (if zero came from the base) -> look at the
    # node in the direction of the equation (specified as 'eqNode')
    # Instruction 4: At power gate (if zero came from the power) -> replace
    # the node by the constant 1 (node 0 in all of the models)
    # Instruction 5: At equations -> delete the edge connecting the equation to the zero node
    def Zero_Import(self, Start, NodeNum,
                    Ignore_List = [], Remove_List = []):
        AllowedTypes = ['MG','ABS','SIN']
        Ignore_List.append(NodeNum)
        SuccList = []
        if NodeNum == Start:
            for i in self.G.successors(NodeNum):
                SuccList.append(i)
            for i in SuccList:
                self.Zero_Import(Start, i, Ignore_List, Remove_List)
        elif self.G.nodes[NodeNum]['type'] in AllowedTypes:
            #if self.G.has_edge(NodeNum, self.G.nodes[NodeNum]['eqNode']):
            for i in self.G.successors(NodeNum):
                self.Zero_Import(Start,
                                 i,#self.G.nodes[NodeNum]['eqNode'],
                                 Ignore_List,
                                 Remove_List)
            del Ignore_List[-1]
        elif self.G.nodes[NodeNum]['type'] == 'PG':
            # Check if the zero is in the base (0 ** x) then
            # propagate the zero import
            if Ignore_List[-2] == self.G.nodes[NodeNum]['base']:
                for i in self.G.successors(NodeNum):
                    self.Zero_Import(Start,i,
                                     Ignore_List,
                                     Remove_List)
            # In case the zero is in the power (x ** 0) then
            # substitute the node by the one with appropriate weight
            else:
                # Determine the weight of the connection between
                # power gate and next node in the direction of the
                # equation ('eqNode')
                OutNode = list(self.G.successors(NodeNum))[0]
                Weight_Of_Connection = self.G.edges[NodeNum,OutNode]['weight']
                # Replace the power gate by the node of constant 1 (node 0)
                self.G.add_weighted_edges_from([(0, OutNode,
                                                 Weight_Of_Connection)])
                self.G.remove_node(NodeNum)
            del Ignore_List[-1]
        elif self.G.nodes[NodeNum]['type'] == 'COS':
            # Determine the weight of the connection between
            # cosinus (cos(0)) node and next node in the
            # direction of the equation ('eqNode')
            OutNode = list(self.G.successors(NodeNum))[0]
            Weight_Of_Connection = self.G.edges[NodeNum,OutNode]['weight']
            if self.Debug:
                print('Set the node', NodeNum, \
                      'to a constant 1 as it is equal to cos(0)')
            # Replace the COS gate by the node of constant 1
            self.G.nodes[NodeNum]['type'] = 'I'
            self.G.nodes[NodeNum]['value'] = 1
            # Remove all of the incomming edges
            outEdges = []
            for i in self.G.out_edges(NodeNum):
                outEdges.append(i)
            for i in outEdges:
                self.G.remove_edge(*i)
        elif self.G.nodes[NodeNum]['type'] == 'E':
            Remove_List.append([Ignore_List[-2],NodeNum])
            del Ignore_List[-1]
        # Finishing procedure
        if NodeNum == Start:
            for i in Remove_List:
                if self.Debug:
                    print('Removed the edge from G during Zero Import check (', \
                          i[0], '<->', i[1], ')')
                self.G.remove_edge(i[0],i[1])
                # If the equation that was disconnected from
                # zero variable has only one connection more
                # then check whether this connection can be set to 0
                if self.G.degree(i[1]) == 1:
                    # Zero element of is the only neighbor of zero equation
                    ZeroElement = [n for n in self.G.predecessors(i[1])][0]
                    if self.Debug:
                        print('Initialized the zero function algorithm for the node', \
                              ZeroElement)
                    self.Zero_Equation(ZeroElement,
                                       ZeroElement,
                                       Ignore_List = [i[0]],
                                       Multiplication_List = [],
                                       Power = 1)



    # Update the variable
    def Update_Var_Solution(self, VarNode, Value, Symb_Solution):
        G_eq_changed = False
        if Value == 0:
            if self.Debug:
                print('Initialized the zero import algorithm for the node', \
                      VarNode)
            self.Zero_Import(VarNode, VarNode, Ignore_List=[], Remove_List=[])
            G_eq_changed = True
        if G_eq_changed:
            # REDO the implementation of G_eq
            self.Make_G_Eq()
        self.G.nodes[VarNode]['known'] = True
        self.G.nodes[VarNode]['value'] = Value
        self.G.nodes[VarNode]['SymbRepr'] = Symb_Solution
        if self.Debug:
            print('The node', VarNode, \
                  'was set to the following value:', Value, \
                  'and with following symbolic representation:', Symb_Solution)
        # Upade G_eq
        self.G_eq.remove_node(VarNode)



    # Update the variable
    def Update_Var_Import(self, VarNode, Value):
        self.G.nodes[VarNode]['known'] = True
        self.G.nodes[VarNode]['value'] = Value
        self.G.nodes[VarNode]['SymbRepr'] = self.G.nodes[VarNode]['SY_Var']
        if self.Debug:
            print('The node', VarNode, \
                  'was set to the following value:', Value)



    # RECURRENT FUNCTION!
    # Function that gathers the equations connected to the discovered variable
    # Instruction 1: Each sampled equation is saved to Eq_List
    # Instruction 2: Stop algorithm on variables, that are not the discovered one
    # (saved under start input variable) and stop it at constants
    # Instruciton 3: On structural nodes look in the direction of the equation ('eqNode')
    # Ignore list is the list of nodes that were inspected before (to stop the algorithm to go back)
    # Start is a saved position of the first variable (it will allow to iterate through the variable)
    def Get_Connected_Eq(self, Start, NodeNum, Ignore_List=[], Eq_List = []):
        Ignore_List.append(NodeNum)
        AllowedTypes = ['MG','ABS','PG','SIN','COS']
        # Look around in the beginning
        if NodeNum == Start:
            for i in self.G.successors(NodeNum):
                if not (i in Ignore_List):
                    Eq_List = self.Get_Connected_Eq(Start, i,
                                                    Ignore_List,
                                                    Eq_List)
        # If the node is an equation:
        elif self.G.nodes[NodeNum]['type'] == 'E':
            Eq_List.append(NodeNum)
        # If the node is structural then go in the direction equation:
        elif (self.G.nodes[NodeNum]['type'] in AllowedTypes):
            OutNode = list(self.G.successors(NodeNum))
            if len(OutNode) == 1:
                Eq_List = self.Get_Connected_Eq(Start, OutNode[0], Ignore_List, Eq_List)
        return Eq_List



    # RECURENT IMPLEMENTATION
    # Function that gets a number of unknown variable of equation with UO = 1
    # (WILL WORK INPROPER ON EQ WITH UO != 1)
    # Instruction 1: Var_Node_Number = sum of var_node_number of connected nodes for not variables
    # Instruction 2: Var_node_number = None if the variable is known and its node number if the variable is known
    # Instruction 3: Stop the algorithm at constants (equations are allowed cause
    # no 2 equations are connected with each other without the variable inbetween)
    # Ignore list is the list of nodes that were inspected before (to stop the algorithm to go back)
    def Find_Var_Node(self, NodeNum, Ignore_List=[]):
        Ignore_List.append(NodeNum)
        Var_Node = None # number of the variable node
        AllowedTypes = ['MG','ABS','PG','E','SIN','COS']
        # If the node is an unknown variable:
        if self.G.nodes[NodeNum]['type'] == 'V':
            if self.G.nodes[NodeNum]['known'] == False:
                return NodeNum
        # Otherwise:
        elif (self.G.nodes[NodeNum]['type'] in AllowedTypes):
            # Look for neighbors
            for i in self.G.predecessors(NodeNum):
                # That were not sampled (when the var node is still unknown)
                if not (i in Ignore_List) and not Var_Node:
                    Var_Node = self.Find_Var_Node(i,Ignore_List)
        return Var_Node



    # RECURENT IMPLEMENTATION
    # Parsing of the equation on the node number E_number (recurrent implementation)
    # Instruction 1: Equation(equation node which is not a variable) = Sum (w_i * Equation_i),
    # where i are the neighbours
    # Instruction 2: Equation(known variable) is its value
    # Instruction 3: Equation(not known variable) is the variable itself
    # Instruction 4: Equation(Multiplication gate) = Product of w_i f_i,
    # where i are the neighbours
    # Instruction 5: Equation(Power gate) = w_1 f_1 ** (w_2 f_2),
    # where 1 and 2 are the neighbours, number of the base is located in the power gate atribute 'base'
    # Instruction 6: Equation(ABS gate) = abs(neighbour)
    # Ignore list is the list of nodes that were inspected before (to stop the algorithm to go back)
    def Parse_Eq(self, NodeNum, Ignore_List=[]):
        Ignore_List.append(NodeNum)
        ConstantNodes = ['C','I']
        # If the node is a variable:
        if self.G.nodes[NodeNum]['type'] == 'V':
            Symbolic_Eq = self.G.nodes[NodeNum]['SY_Var']
            Unit = self.G.nodes[NodeNum]['unit']
            if self.G.nodes[NodeNum]['known'] == False:
                Numeric_Eq = self.G.nodes[NodeNum]['SY_Var']
                Symbolic_Repr = self.G.nodes[NodeNum]['SY_Var']
            else:
                Numeric_Eq = self.G.nodes[NodeNum]['value']
                Symbolic_Repr = self.G.nodes[NodeNum]['SY_Var']
        # If the node is a constant:
        elif self.G.nodes[NodeNum]['type'] == 'C':
            Numeric_Eq = self.G.nodes[NodeNum]['value']
            Symbolic_Eq = self.G.nodes[NodeNum]['value']
            Symbolic_Repr = self.G.nodes[NodeNum]['value']
            Unit = self.G.nodes[NodeNum]['unit']
        # If the node is a constant one:
        elif self.G.nodes[NodeNum]['type'] == 'I':
            Numeric_Eq = self.G.nodes[NodeNum]['value']
            Symbolic_Eq = self.G.nodes[NodeNum]['value']
            Symbolic_Repr = self.G.nodes[NodeNum]['value']
            Unit = self.ureg['dimensionless']
        # If the node is a sinus:
        elif self.G.nodes[NodeNum]['type'] == 'SIN':
            for i in self.G.in_edges(NodeNum):
                for j in i:
                    if not (j in Ignore_List):
                        PartialEquation = self.Parse_Eq(j, Ignore_List)
                        Numeric_Eq = sy.sin(PartialEquation[0])
                        Symbolic_Eq = sy.sin(PartialEquation[1])
                        Symbolic_Repr = sy.sin(PartialEquation[2])
                        Unit = PartialEquation[3]
                        if (str(Unit.units) != 'dimensionless') and (str(Unit.units) != 'radian'):
                            self.error = {
                                'message': 'Non zero SIN unit',
                                'node_id': NodeNum,
                                'type': None
                            }
        # If the node is a cosinus:
        elif self.G.nodes[NodeNum]['type'] == 'COS':
            for i in self.G.in_edges(NodeNum):
                for j in i:
                    if not (j in Ignore_List):
                        PartialEquation = self.Parse_Eq(j, Ignore_List)
                        Numeric_Eq = sy.cos(PartialEquation[0])
                        Symbolic_Eq = sy.cos(PartialEquation[1])
                        Symbolic_Repr = sy.cos(PartialEquation[2])
                        Unit = PartialEquation[3]
                        if (str(Unit.units) != 'dimensionless') and (str(Unit.units) != 'radian'):
                            self.error = {
                                'message': 'Non zero COS unit',
                                'node_id': NodeNum,
                                'type': None
                            }
        elif self.G.nodes[NodeNum]['type'] == 'ABS':
            for i in self.G.in_edges(NodeNum):
                for j in i:
                    if not (j in Ignore_List):
                        PartialEquation = self.Parse_Eq(j, Ignore_List)
                        Numeric_Eq = abs(PartialEquation[0])
                        Symbolic_Eq = abs(PartialEquation[1])
                        Symbolic_Repr = abs(PartialEquation[2])
                        Unit = PartialEquation[3]
        # If the node is an equation:
        elif self.G.nodes[NodeNum]['type'] == 'E':
            Numeric_Eq = 0
            Symbolic_Eq = 0
            Symbolic_Repr = 0
            MasterUnit = None
            for i in self.G.in_edges(NodeNum):
                for j in i:
                    if not (j in Ignore_List):
                        Ignore_List = [NodeNum]
                        PartialEquation = self.Parse_Eq(j, Ignore_List)
                        Numeric_Eq += self.G.edges[i]['weight'] * PartialEquation[0]
                        Symbolic_Eq += self.G.edges[i]['weight'] * PartialEquation[1]
                        Symbolic_Repr += self.G.edges[i]['weight'] * PartialEquation[2]
                        Unit = PartialEquation[3]
                        if MasterUnit == None:
                            MasterUnit = Unit
                        elif Unit != None:
                            if MasterUnit != Unit:
                                self.error = {
                                    'message': 'Equation unit clash',
                                    'node_id': NodeNum,
                                    'type': None
                                }
        # If the node is a multiplication gate:
        elif self.G.nodes[NodeNum]['type'] == 'MG':
            Numeric_Eq = 1
            Symbolic_Eq = 1
            Symbolic_Repr = 1
            Unit = self.ureg['dimensionless']
            for (j,i) in self.G.in_edges(NodeNum):
                if not (j in Ignore_List):
                    PartialEquation = self.Parse_Eq(j, Ignore_List)
                    Numeric_Eq *= self.G.edges[j,i]['weight'] * PartialEquation[0]
                    Symbolic_Eq *= self.G.edges[j,i]['weight'] * PartialEquation[1]
                    Symbolic_Repr *= self.G.edges[j,i]['weight'] * PartialEquation[2]
                    LocalUnit = PartialEquation[3]
                    if (LocalUnit != None) and (Unit != None):
                        Unit *= LocalUnit
                    else:
                        Unit = None
        # If the node is a summation gate:
        elif self.G.nodes[NodeNum]['type'] == 'SG':
            Numeric_Eq = 0
            Symbolic_Eq = 0
            Symbolic_Repr = 0
            MasterUnit = None
            for (j,i) in self.G.in_edges(NodeNum):
                if not (j in Ignore_List):
                    PartialEquation = self.Parse_Eq(j, Ignore_List)
                    Numeric_Eq += self.G.edges[j,i]['weight'] * PartialEquation[0]
                    Symbolic_Eq += self.G.edges[j,i]['weight'] * PartialEquation[1]
                    Symbolic_Repr += self.G.edges[j,i]['weight'] * PartialEquation[2]
                    Unit = PartialEquation[3]
                    if MasterUnit == None:
                        MasterUnit = Unit
                    elif Unit != None:
                        if MasterUnit != Unit:
                            self.error = {
                                'message': 'Summation unit clash',
                                'node_id': NodeNum,
                                'type': None
                            }
        # If the node is a power gate:
        elif self.G.nodes[NodeNum]['type'] == 'PG':
            base = self.G.nodes[NodeNum]['base']
            power = self.G.nodes[NodeNum]['power']
            PartialEquationBase = self.Parse_Eq(base, Ignore_List)
            PartialEquationPower = self.Parse_Eq(power, Ignore_List)
            Numeric_Eq = (self.G.edges[base,NodeNum]['weight'] * PartialEquationBase[0]) ** \
                         (self.G.edges[power, NodeNum]['weight'] * PartialEquationPower[0])
            Symbolic_Eq = (self.G.edges[base,NodeNum]['weight'] * PartialEquationBase[1]) ** \
                          (self.G.edges[power, NodeNum]['weight'] * PartialEquationPower[1])
            Symbolic_Repr = (self.G.edges[base,NodeNum]['weight'] * PartialEquationBase[2]) ** \
                            (self.G.edges[power, NodeNum]['weight'] * PartialEquationPower[2])
            # Check if power can be evaluated
            BaseUnit = PartialEquationBase[3]
            Power = self.G.edges[power, NodeNum]['weight'] * PartialEquationPower[0]
            if isinstance(Power, float) and (BaseUnit != None):
                Unit = BaseUnit ** Power
            else:
                Unit = None
        return Numeric_Eq, Symbolic_Eq, Symbolic_Repr, Unit



    # Solver for the parsed equation (based on sympy)
    def Solve_Eq(self, Eq_Node, Var_Node):
        (Numeric_Eq, Symbolic_Eq, Symbolic_Repr, Unit) = self.Parse_Eq(Eq_Node, Ignore_List=[])
        if self.Trace or self.Debug: print('Equation: ',Symbolic_Eq, '= 0')
        # Solve the equation
        Solution = sy.solvers.solve(Numeric_Eq,self.G.nodes[Var_Node]['SY_Var'])
        Symb_Solution = sy.solvers.solve(Symbolic_Repr,self.G.nodes[Var_Node]['SY_Var'])
        # If the variable node is non negative delete all negative solutions
        if 'positive' in self.G.nodes[Var_Node]:
            Solution = [i for i in Solution if i>0]
        Symb_Solution = sy.simplify(Symb_Solution[0])
        if len(Solution) > 1:
            self.error = {
                'message': 'Ambigues equation solution',
                'node_id': Eq_Node,
                'type': None
            }
            #raise Exception('Ambiguous solution! Multiple solutions detected')
        if len(Solution) == 0:
            self.error = {
                'message': 'All solutions of given equation ignored',
                'node_id': Eq_Node,
                'type': None
            }
            #raise Exception('No solution! Probably all solutions were ignored due \
            #                to the variable restrictions (only positive, etc)')
        if self.error == {}:
            if self.Trace:
                print('Result:', self.G.nodes[Var_Node]['SY_Var'], \
                    '=', Symb_Solution,'= {:.2f}'.format(float(Solution[0])), \
                    self.G.nodes[Var_Node]['unit'].units,'\n')
            if self.Debug:
                print('Result:', self.G.nodes[Var_Node]['SY_Var'], \
                    '=', Symb_Solution,'= {:.2f}'.format(float(Solution[0])), \
                    self.G.nodes[Var_Node]['unit'].units)
            # Update the discovered variable
            self.Update_Var_Solution(Var_Node, float(Solution[0]), Symb_Solution)



    # Solver for the cycle
    def Solve_G_eq_Cycle(self, Cycle, SolutionVarNode):
        # Get the sympy object of the solution variable
        Var = self.G.nodes[SolutionVarNode]['SY_Var']
        # Parse all equations
        NumSystemOfEquations = []
        SymbSystemOfEquations = []
        for i in Cycle:
            (Numeric_Eq, Symbolic_Eq, Symbolic_Repr, Unit) = self.Parse_Eq(i, Ignore_List=[])
            NumSystemOfEquations.append(Numeric_Eq)
            SymbSystemOfEquations.append(Symbolic_Repr)
            if self.Trace or self.Debug:
                print('System of equations: ', Symbolic_Eq, '= 0')
        # Solve the system of equations
        Num_Solution = sy.solvers.solve(NumSystemOfEquations)
        Symb_Solution = sy.solvers.solve(SymbSystemOfEquations)
        # Filter the solutions
        if 'positive' in self.G.nodes[SolutionVarNode]:
            Num_Solution_List = []
            for i in range(len(Num_Solution)):
                if Num_Solution[i][Var] > 0:
                    Num_Solution_List.append(Num_Solution[i])
            Num_Solution = Num_Solution_List
        # Check for ambiguity
        if isinstance(Num_Solution, dict):
            # Extract the needed variable from the solution
            Num_Solution = Num_Solution[Var]
            #print Symb_Solution
            if Var in Symb_Solution[0]:
                Symb_Solution = Symb_Solution[0][Var]
            else:
                Symb_Solution = Num_Solution
        else:
            if len(Num_Solution) > 2:
                self.error = {
                    'message': 'Ambigues solution of equation system',
                    'node_id': None,
                    'type': Cycle
                }
                #raise Exception('Ambiguous solution! Multiple solutions detected')
            # Extract the needed variable from the solution
            Num_Solution = Num_Solution[0][Var]
            Symb_Solution = Symb_Solution[0][Var]
        # Transform the solutions
        if self.Trace:
            print('Result: ', Var, ' = ', Symb_Solution, \
                  ' = {:.2f}'.format(float(Num_Solution)), \
                  self.G.nodes[SolutionVarNode]['unit'].units,'\n')
        if self.Debug:
            print('Result: ', Var, ' = ', Symb_Solution, \
                  ' = {:.2f}'.format(float(Num_Solution)), \
                  self.G.nodes[SolutionVarNode]['unit'].units)
        # Update the variable in the graph
        self.Update_Var_Solution(SolutionVarNode, float(Num_Solution), Symb_Solution)



    # Find unknown variable list of the equation
    def FindVariableList(self, NodeNum, Start, Var_List = [], Ignore_List = []):
        Ignore_List.append(NodeNum)
        AllowedTypes = ['MG','ABS','PG','SIN','COS']
        # Look around in the beginning
        if NodeNum == Start:
            for i in self.G.predecessors(NodeNum):
                Var_List = self.FindVariableList(i, Start,
                                                     Var_List,
                                                     Ignore_List)
        # If the node is an unknown variable:
        elif (self.G.nodes[NodeNum]['type'] == 'V') and not self.G.nodes[NodeNum]['known']:
            Var_List.append(NodeNum)
        # If the node is structural then go in the direction variable:
        elif (self.G.nodes[NodeNum]['type'] in AllowedTypes):
            for i in self.G.predecessors(NodeNum):
                Var_List = self.FindVariableList(i, Start,
                                                 Var_List,
                                                 Ignore_List)
        return Var_List



    # Find shared unknown variable
    def FindSharedUnknownVariable(self,Eq1,Eq2):
        VarList1 = self.FindVariableList(Eq1,Eq1, Var_List = [], Ignore_List = [])
        VarList2 = self.FindVariableList(Eq2,Eq2, Var_List = [], Ignore_List = [])
        for i in VarList1:
            if i in VarList2:
                SharedVariable = i
        return SharedVariable



    # Check whether 2 numerical equations are symmetrical
    def Equations_Symmetrical(self, Solution1, Solution2):
        Division = Solution1 / Solution2
        if Division.is_real:
            return Division
        else: return False



    # Symmetry condition on dependent variables
    # In order for two equations to be symmetrical their dependent
    # vaiables have to match except one
    def Symmetry_Condition_On_Variables(self, Var1, Var2):
        Condition = True
        NotMatchingVariableCount = 0
        a = [i for i in Var1 if i not in Var2]
        b = [i for i in Var2 if i not in Var1]
        if (len(a) == 1) and (len(b) == 1):
            return True, a, b
        else: return False, 0, 0



    # RECURENT IMPLEMENTATION
    # Go through all structural nodes until the variable and save it
    def Get_Equation_Variables(self, NodeVar,
                               BagOfVariables = [],
                               Ignore_List = []):
        Ignore_List.append(NodeVar)
        AllowedTypes = ['MG','ABS','PG','E','SIN','COS']
        if self.G.nodes[NodeVar]['type'] == 'V':
            BagOfVariables.append(NodeVar)
            return BagOfVariables
        elif (self.G.nodes[NodeVar]['type'] in AllowedTypes):
            for i in self.G.predecessors(NodeVar):
                BagOfVariables = self.Get_Equation_Variables(i,
                                                             BagOfVariables,
                                                             Ignore_List)
        return BagOfVariables



    # Checks if two given equations are symmetrical (a = f(x) and
    # b = alpha * f(x), where alpha is a constant)
    def Check_For_Symmetry(self, VarNode):
        if self.G_eq.has_node(VarNode):
            # Get the cycles around the fused variable
            Cycles = nx.cycle_basis(self.G_eq,VarNode)
            # Filter only cycles of length 4 and leave only equations
            FourCycles = [x for x in Cycles if len(x) == 4]
            FilteredCycles = []
            for i in FourCycles:
                PotentialPair = [x for x in i if self.G_eq.nodes[x]['type']=='E']
                # Get two equations
                Eq1 = PotentialPair[0]
                Eq2 = PotentialPair[1]
                # Get the list of variables for both equations
                Var1 = self.Get_Equation_Variables(Eq1,
                                               BagOfVariables = [],
                                               Ignore_List = [])
                Var2 = self.Get_Equation_Variables(Eq2,
                                               BagOfVariables = [],
                                               Ignore_List = [])
                # If both equations depend on different amount of variables then
                # the symmetry condition is automatically broken
                # If the number of dependent variables is equal, then
                # check that for both equations all except one variable (main unknown) are shared
                if len(Var1) == len(Var2):
                    SymmetryCondition = self.Symmetry_Condition_On_Variables(Var1, Var2)
                    if SymmetryCondition[0]:
                        MainUnknown1 = SymmetryCondition[1][0]
                        MainUnknown2 = SymmetryCondition[2][0]
                        # If the condition is satified then solve both equations
                        # in regard of main variable and check whether solutions are linear to each other
                        # First parse the equations
                        (Numeric_Eq1, Symbolic_Eq1, Symbolic_Repr1, Unit) = self.Parse_Eq(Eq1,
                                                                                Ignore_List=[])
                        (Numeric_Eq2, Symbolic_Eq2, Symbolic_Repr2, Unit) = self.Parse_Eq(Eq2,
                                                                                Ignore_List=[])
                        # Then solve them
                        Solution1 = sy.solvers.solve(Symbolic_Eq1,
                                                 self.G.nodes[MainUnknown1]['SY_Var'])[0]
                        Solution2 = sy.solvers.solve(Symbolic_Eq2,
                                                 self.G.nodes[MainUnknown2]['SY_Var'])[0]
                        # Check the solutions for their linearity
                        SymmetryCoef = self.Equations_Symmetrical(Solution1, Solution2)
                        if SymmetryCoef:
                            self.SymmetryCount += 1
                            EqName = 'SY-' + str(self.SymmetryCount)
                            if self.Debug:
                                print('Connected 2 symmetrical variables', \
                                      MainUnknown1, 'and', MainUnknown2, \
                                      'with equation', EqName, \
                                      '. Symmetry coefficient: ', float(SymmetryCoef))
                            self.G.add_node(EqName, type='E')
                            self.G.add_weighted_edges_from([(MainUnknown1,EqName,-1),
                                                        (MainUnknown2,EqName,float(SymmetryCoef))])




    # Interactive solver
    def Interactive_Solver(self, NodeNum, Start,
                           SolutionVarNode,
                           Ignore_List = [],
                           Distance = 0):
        flag = True
        while flag:
            flag = False
            # Calculate the shortest path and sort the nodes accordingly
            p=nx.shortest_path_length(self.G_eq,source=Start)
            sorted_p = sorted(p.items(), key = lambda i: i[1])
            sorted_eq = [x for x in sorted_p if self.G_eq.nodes[x[0]]['type'] == 'E']
            for i in sorted_eq:
                if not self.G.nodes[SolutionVarNode]['known'] and (self.G_eq.degree(i[0]) == 1) and (self.error == {}):
                    Var_Node = self.Find_Var_Node(i[0], Ignore_List = [])
                    if self.Debug: print('Found a solvable equation:', i[0])
                    self.Solve_Eq(i[0], Var_Node)
                    if self.error == {}:
                        flag = True



    # Interactive solver wrapper
    def Interactive_Solver_Wrapper(self, SolutionVarNode, Final_Eq_List):

        # Output the list of connected equations
        if self.Debug:
            print('Equations giving solution:', Final_Eq_List)

        # Attempt to solve each connected equation individually
        for i in Final_Eq_List:
            if not self.G.nodes[SolutionVarNode]['known'] and (self.error == {}):

                # Debug output
                if self.Debug:
                    print('Attempting to solve through the equation', i)

                # Solve the given equation
                self.Interactive_Solver(i, i, SolutionVarNode,
                                        Ignore_List=[],
                                        Distance=0)

                # If equation was not directly solved attempt to solve it as a
                # system of equations (cycle)
                if not self.G.nodes[SolutionVarNode]['known'] and (self.error == {}):
                    (Cycles, CycleExist) = self.CheckCycle_G_eq(i, Final_Eq_List)
                    if CycleExist:
                        for i in Cycles:
                            self.Solve_G_eq_Cycle(i, SolutionVarNode)

                # Debug output the result of equation solving
                if self.Debug:
                    if self.G.nodes[SolutionVarNode]['known']:
                        print('Problem solved through the equation', i)
                    else:
                        print('Unfortunately equation', i, 'was not solved.')


    # Check for Cycles
    def CheckCycle_G_eq(self, Node, EqList):
        CycleExist = False
        FilteredCycles = []
        # Make a subgraph with only equations with UO of 2
        HelperGraph = self.G_eq.copy()
        for i in self.G_eq.nodes():
            if (HelperGraph.nodes[i]['type'] == 'E') and (HelperGraph.degree(i) != 2):
                HelperGraph.remove_node(i)
        Cycles = nx.cycle_basis(HelperGraph)
        if Cycles:
            CycleExist = True
            for i in Cycles:
                FilteredCycles.append([x for x in i if HelperGraph.nodes[x]['type']=='E'])
        return (FilteredCycles, CycleExist)



    # Interactive solving (lets specify the variable node, important for
    # complex models (multiple connected graphs)):
    def Interactive_Solving_Hidden(self, VarNode=None, VarName=None):

        # Find the node corresponding for the solution variable
        if VarNode != None:
            SolutionVarNode = VarNode
        elif VarName != None:
            SolutionVarNode = self.Find_Node_By_Var_Name(VarName)

        # Check if solution node was found
        if SolutionVarNode != None:
            if self.Debug: print('Solution variable:', SolutionVarNode)
        else:
            raise Exception('Please, identify either the solution variable node \
                            or solution variable name')
        # Initialize G_eq
        if not self.Initialized_G_eq:
            self.Zero_Import_Wrapper()
            self.Initialized_G_eq = True
            self.Make_G_Eq()

        # Calculate the list of equations directly connected to the solution variable
        Final_Eq_List = self.Get_Connected_Eq(SolutionVarNode,
                                              SolutionVarNode,
                                              Ignore_List=[],
                                              Eq_List = [])

        # Solve the problem for the solution variable
        self.Interactive_Solver_Wrapper(SolutionVarNode, Final_Eq_List)

        # If problem solved (solution node known) then return the results
        if self.error != {}:
            Status = 'error'
            Value = None
            Unit = None
            Error = self.error
        elif self.G.nodes[SolutionVarNode]['known'] == True:
            Status = 'solved'
            Value = self.G.nodes[SolutionVarNode]['value']
            Unit = str(self.G.nodes[SolutionVarNode]['unit'].units)
            Error = self.error
            if self.Trace or self.Debug:
                if self.G.nodes[SolutionVarNode]['unit'].units != 1:
                    print('Solution: ', VarName, \
                          ' = {:.2f}'.format(self.G.nodes[SolutionVarNode]['value']), \
                          self.G.nodes[SolutionVarNode]['unit'].units, '\n')
                else:
                    print('Solution: ', VarName, \
                          ' = {:.2f}'.format(self.G.nodes[SolutionVarNode]['value']), '\n')
        # If problem not solved then return the following message
        else:
            if self.Trace or self.Debug:
                print('The problem was not solved. Additional input data is required')
            Status = 'not solved'
            Value = None
            Unit = None
            Error = self.error
        return {
            'status': Status,
            'value': Value,
            'unit': Unit,
            'error': Error
        }
