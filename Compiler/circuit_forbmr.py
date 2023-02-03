class Circuit:
    def __init__(self, name):
        self.filename = 'Programs/Circuits/%s.txt' % name
        f = open(self.filename)
        self.functions = {}

    def compile(self):
        f = open(self.filename)
        lines = iter(f)
        next_line = lambda: next(lines).split()
        n_gates, n_wires = (int(x) for x in next_line())
        self.n_wires = n_wires
        input_line = [int(x) for x in next_line()]
        n_inputs = input_line[0]
        self.n_inputs = n_inputs
        n_input_wires = input_line[1:]
        self.n_input_wires = n_input_wires
        assert(n_inputs == len(n_input_wires))

        s = 0
        for n in n_input_wires:
            s += n
        output_line = [int(x) for x in next_line()]
        n_outputs = output_line[0]
        self.n_outputs = n_outputs
        self.n_output_wires = output_line[1:]
        assert(n_outputs == len(self.n_output_wires))
        next(lines)

        self.gates = []
        for i in range(n_gates):
            line = next_line()
            t = line[-1]
            if t in ('XOR', 'AND'):
                assert line[0] == '2'
                assert line[1] == '1'
                assert len(line) == 6
                ins = [int(line[2 + i]) for i in range(2)]
                if t == 'XOR':
                    self.gates.append(('XOR', ins[0], ins[1], int(line[4])))
                else:
                    self.gates.append(('AND', ins[0], ins[1], int(line[4])))
            elif t == 'INV':
                assert line[0] == '1'
                assert line[1] == '1'
                assert len(line) == 5
                self.gates.append(('INV', int(line[2]), int(line[3])))

