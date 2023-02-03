BLS_PRIME=52435875175126190479447740508185965837690552500527637822603658699938581184513

class FieldElement:
    def __init__(self, val):
        self.val = val % BLS_PRIME
    def __radd__(self, other):
        return self + other
    def __add__(self, other):
        if type(other) is FieldElement:
            return FieldElement(self.val + other.val)
        if type(other) is int:
            return FieldElement(self.val + other)
    def __sub__(self, other):
        return FieldElement(self.val - other.val)
    def __mul__(self, other):
        return FieldElement(self.val * other.val)
    def __pow__(self, other):
        res = pow(self.val, other, BLS_PRIME)
        return FieldElement(res)
    def __eq__(self, other):
        if type(other) is int:
            return self.val == other
        if type(other) is FieldElement:
            return self.val == other.val
        print("f")
    def __str__(self):
        return self.val.__str__()
    def __repr__(self):
        return self.val.__repr__()

def dual_encrypt(k1, k2, m):
    # Returns a pair of field elements as the ciphertext
    c0 = mimc_prf(k1, 0) + mimc_prf(k2, 0)
    c1 = mimc_prf(k1, 1) + mimc_prf(k2, 1) + m
    return (c0, c1)

def mimc_prf(key, m):
    x = m + key

    for r in range(64):
        x = x ** 3
        x = x + key + 0 # self.constants[r]

    x = x + key
    return x

def dual_decrypt(k1, k2, c):
    (c0, c1) = c
    assert(type(k1) is FieldElement)
    assert(type(k2) is FieldElement)
    assert(type(c0) is FieldElement)
    assert(type(c1) is FieldElement)
    new_c0 = mimc_prf(k1, 0) + mimc_prf(k2, 0)
    assert(type(new_c0) is FieldElement)
    if c0 != new_c0:
        return False
    m = c1 - (mimc_prf(k1, 1) + mimc_prf(k2, 1))
    #print("decryption: ", m)
    return m

def deserialize_2dlist(text):
    text2 = text.replace('[', '')
    while text2[-1] == ']':
        text2 = text2[:-1]
    rows = text2.split(']')
    out = []
    for row in rows:
        if len(row) == 0:
            continue
        if row[0] == ',':
            row = row[1:]
        if row[-1] == ',':
            row = row[:-1]
        out.append([FieldElement(int(num)) for num in row.split(',')])
    return out

def deserialize_1dlist(text):
    text2 = text.replace('[', '')
    text2 = text2.replace(']', '')
    return [FieldElement(int(num)) for num in text2.split(',')]

def read_circuit(f):
    and_gates = []
    xor_gates = []
    gates = []
    linenum = -1
    for line in f:
        linenum += 1
        s = line.split()
        if linenum < 4 or len(s) < 4:
            if linenum == 2:
                output_len = sum([int(num) for num in s[1:]])
            continue
        if s[4] == "INV":
            gates.append(s[2:5])
        elif s[5] == "AND":
            gates.append(s[2:6])
        elif s[5] == "XOR":
            gates.append(s[2:6])
        else:
            runtime_error93
    return (gates, output_len)

def decrypt_gate(ciphs, label0, label1):
    for ciph in (ciphs[0:2], ciphs[2:4], ciphs[4:6], ciphs[6:8]):
        res = dual_decrypt(label0, label1, ciph)
        if type(res) is FieldElement:
            #print("it went okay")
            return res
    it_went_bad
    
#def eval_circuit(gates, and_ciph, xor_ciph, input_labels, maskbits):
def eval_circuit(gates, and_ciph, xor_ciph, input_labels, output_len):
    label_dict = {}
    for i, label in enumerate(input_labels):
        label_dict[i] = label
    and_count, xor_count = 0,0
    for gate in gates:
        if gate[-1] == "INV":
            #mask bit gets flipped. we don't need to do anything here
            res = label_dict[int(gate[0])]
            out_idx = gate[1]
            label_dict[int(out_idx)] = res
            continue
        inp0 = label_dict[int(gate[0])]
        inp1 = label_dict[int(gate[1])]
        out_idx = gate[2]
        if gate[-1] == "AND":
            res = decrypt_gate([and_ciph[0][and_count], and_ciph[1][and_count], and_ciph[2][and_count], and_ciph[3][and_count], and_ciph[4][and_count], and_ciph[5][and_count], and_ciph[6][and_count], and_ciph[7][and_count]], inp0, inp1)
            and_count += 1
        if gate[-1] == "XOR":
            res = decrypt_gate([xor_ciph[0][xor_count], xor_ciph[1][xor_count], xor_ciph[2][xor_count], xor_ciph[3][xor_count], xor_ciph[4][xor_count], xor_ciph[5][xor_count], xor_ciph[6][xor_count], xor_ciph[7][xor_count]], inp0, inp1)
            xor_count += 1
        
        label_dict[int(out_idx)] = res
    output_keys = sorted(list(label_dict.keys()))[-output_len:]
    return [label_dict[key] for key in output_keys]


a = FieldElement(43040751)
b = FieldElement(-239862521)
m = FieldElement(420)
c = dual_encrypt(a, b, m)
m2 = dual_decrypt(a, b, c)
#print(m2.val)
txtlist = "[[2523234,43636,346,23425],[23425,232,55,5], [2]]"
txtlist1 = "[2523234,43636,346,23425]"
#print(deserialize_1dlist(txtlist1))

f = open('output_step1.txt', 'r')
line = f.readline()
while line != "xor_ciph\n":
    line = f.readline()
xor_ciph = deserialize_2dlist(f.readline()[:-1])
f.readline()
and_ciph = deserialize_2dlist(f.readline()[:-1])
f.close()

f = open('output_step2.txt', 'r')
line = f.readline()
while line != "inp_labels\n":
    line = f.readline()
labels = deserialize_1dlist(f.readline()[:-1])
f.close()

gates, output_len = read_circuit(open('Programs/Circuits/program.txt', 'r'))
outputs = eval_circuit(gates, and_ciph, xor_ciph, labels, output_len)
for output in outputs:
    print(output)