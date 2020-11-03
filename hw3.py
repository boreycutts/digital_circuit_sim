import random

class Gate:
    def __init__(self, name):
        self.name = name
        self.input_connections = []
        self.output_connections = []
        self.stuck_at_0 = False
        self.stuck_at_1 = False
        self.p0 = 0
        self.o0 = 0
        self.p1 = 0
        self.o1 = 0
        self.fault_impact = 0

    def propagate(self, value):
        for connection in self.output_connections:
            if self.stuck_at_0:
                connection.value = 0
            elif self.stuck_at_1:
                connection.value = 1
            else:
                connection.value = value

    def evaluate(self):
        return

class Connection:
    def __init__(self, start, end, name=None):
        self.start = start
        self.end = end
        self.name = name
        self.value = None

class AND(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
    
    def evaluate(self):
        inputs = []
        for connection in self.input_connections:
            inputs.append(connection.value)
        output_value = int(all(inputs))
        self.propagate(output_value)

class OR(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
    
    def evaluate(self):
        inputs = []
        for connection in self.input_connections:
            inputs.append(connection.value)
        output_value = any(inputs)
        self.propagate(output_value)

class NOT(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
    
    def evaluate(self):
        output_value = 1 if not(self.input_connections[0].value) else 0
        self.propagate(output_value)

class XOR(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
    
    def evaluate(self):
        output_value = 1 if self.input_connections[0].value != self.input_connections[0].value else 0
        self.propagate(output_value)

class XNOR(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)
    
    def evaluate(self):
        output_value = 1 if self.input_connections[0].value == self.input_connections[0].value else 0
        self.propagate(output_value)

class Input(Gate):
    def __init__(self, name):
        Gate.__init__(self, name)

    def evaluate(self):
        output_value = 1 if self.input_connections[0].value else 0
        self.propagate(output_value)

class Circuit:
    def __init__(self, input_connections, output_connections, gates):
        self.input_connections = input_connections
        self.output_connections = output_connections
        self.gates = gates

    def evaluate(self, inputs):
        for i in range(len(self.input_connections)):
            self.input_connections[i].value = inputs[i]
    
        for gate in self.gates:
            gate.evaluate()
            if debug:
                print(gate.name)
                print('Inputs:')
                for i in gate.input_connections:
                    print(i.value)
                print('Output')
                print(gate.output_connections[0].value)
                print()
            elif print_eval:
                print(gate.output_connections[0].value, end=', ')

debug = 0
print_eval = 0

G0 = NOT('G0')
G1 = NOT('G1')
G2 = NOT('G2')

F0 = AND('FO')
F1 = AND('F1')
F2 = AND('F2')
F3 = AND('F3')
F4 = AND('F4')
F5 = AND('F5')
F6 = AND('F6')
F7 = AND('F7')

x = Input('x')
y = Input('y')
z = Input('z')

x.input_connections = [Connection(None, x)]
x.output_connections =  [
    Connection(x, G0), 
    Connection(x, F4),
    Connection(x, F5),
    Connection(x, F6),
    Connection(x, F7)
]
y.input_connections = [Connection(None, y)]
y.output_connections =  [
    Connection(y, G1), 
    Connection(y, F2),
    Connection(y, F3),
    Connection(y, F6),
    Connection(y, F7)
]
z.input_connections = [Connection(None, z)]
z.output_connections =  [
    Connection(z, G2), 
    Connection(z, F1),
    Connection(z, F3),
    Connection(z, F5),
    Connection(z, F7)
]

G0.input_connections = [x.output_connections[0]]
G0.output_connections = [
    Connection(G0, F0),
    Connection(G0, F1),
    Connection(G0, F2),
    Connection(G0, F3),
]
G1.input_connections = [y.output_connections[0]]
G1.output_connections = [
    Connection(G1, F0),
    Connection(G1, F1),
    Connection(G1, F4),
    Connection(G1, F5),
]
G2.input_connections = [z.output_connections[0]]
G2.output_connections = [
    Connection(G2, F0),
    Connection(G2, F2),
    Connection(G2, F4),
    Connection(G2, F6),
]

F0.input_connections = [
    G0.output_connections[0],
    G1.output_connections[0],
    G2.output_connections[0],
] 
F0.output_connections = [Connection(F0, None, 'F0')]

F1.input_connections = [
    G0.output_connections[1],
    G1.output_connections[1],
    z.output_connections[1],
] 
F1.output_connections = [Connection(F1, None, 'F1')]

F2.input_connections = [
    G0.output_connections[2],
    y.output_connections[2],
    G2.output_connections[1],
] 
F2.output_connections = [Connection(F2, None, 'F2')]

F3.input_connections = [
    G0.output_connections[3],
    y.output_connections[2],
    z.output_connections[2],
] 
F3.output_connections = [Connection(F3, None, 'F3')]

F4.input_connections = [
    x.output_connections[1],
    G1.output_connections[2],
    G2.output_connections[2],
] 
F4.output_connections = [Connection(F4, None, 'F4')]

F5.input_connections = [
    x.output_connections[2],
    G1.output_connections[3],
    z.output_connections[3],
] 
F5.output_connections = [Connection(F5, None, 'F5')]

F6.input_connections = [
    x.output_connections[3],
    y.output_connections[3],
    G2.output_connections[3]
] 
F6.output_connections = [Connection(F6, None, 'F6')]

F7.input_connections = [
    x.output_connections[4],
    y.output_connections[4],
    z.output_connections[4],
] 
F7.output_connections = [Connection(F7, None, 'F6')]

circuit = Circuit(
    [
        x.input_connections[0], 
        y.input_connections[0], 
        z.input_connections[0]
    ],
    [
        F0.output_connections[0],
        F1.output_connections[0],
        F2.output_connections[0],
        F3.output_connections[0],
        F4.output_connections[0],
        F5.output_connections[0],
        F6.output_connections[0],
        F7.output_connections[0],
    ],
    [x, y, z, G0, G1, G2, F0, F1, F2, F3, F4, F5, F6, F7]
)

# circuit.gates[0].stuck_at_0 = True

# test_vectors = [
#     [0, 0, 0],
#     [0, 0, 1],
#     [0, 1, 0],
#     [0, 1, 1],
#     [1, 0, 0],
#     [1, 0, 1],
#     [1, 1, 0],
#     [1, 1, 1],
# ]

test_vectors = []

for i in range(100):
    test_vectors.append([
        random.randint(0, 1), 
        random.randint(0, 1), 
        random.randint(0, 1)
    ])

for tv in test_vectors:
    circuit.evaluate(tv)
    for i in range(len(circuit.gates)):
        value = circuit.gates[i].output_connections[0].value
        circuit.gates[i].p0 += 1 if value == 1 else 0
        circuit.gates[i].p1 += 1 if value == 0 else 0

    outputs = []
    
    for output in circuit.output_connections:
        outputs.append(output.value)
    
    for i in range(len(circuit.gates)):
        circuit.gates[i].stuck_at_0 = True
        circuit.evaluate(tv)
        circuit.gates[i].stuck_at_0 = False

        outputs_sa0 = []
        for output in circuit.output_connections:
            outputs_sa0.append(output.value)

        circuit.gates[i].stuck_at_1 = True
        circuit.evaluate(tv)
        circuit.gates[i].stuck_at_1 = False

        outputs_sa1 = []
        for output in circuit.output_connections:
            outputs_sa1.append(output.value)

        # if outputs == outputs_sa0 or outputs == outputs_sa1:
        #     print('Gate: ' + circuit.gates[i].name)
        #     print('TV: ' + str(tv))
        #     print(outputs)
        #     print(outputs_sa0)
        #     print(outputs_sa1)
        #     print()

        for n in range(len(outputs)):
            circuit.gates[i].o0 += 1 if outputs[n] != outputs_sa0[n] else 0
            circuit.gates[i].o1 += 1 if outputs[n] != outputs_sa1[n] else 0

fault_impacts = []

for gate in circuit.gates:
    gate.fault_impact = gate.p0 * gate.o0 + gate.p1 * gate.o1
    fault_impacts.append((gate.fault_impact, gate.name))
    print(gate.name + ': ' + str(gate.fault_impact))
    # print(gate.name + ': p0 = ' + str(gate.p0) + ' p1 = ' + str(gate.p1) + ' o0 = ' + str(gate.o0) + ' o1 = ' + str(gate.o1))

print(sorted(fault_impacts))