class FieldOfOrder4:
    def __init__(self, element):
        self.element = element

    def __add__(self, other):
        # Define custom addition operation for the field
        element_dict = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        result_index = (element_dict[self.element] + element_dict[other.element]) % 4
        result_elements = ['A', 'C', 'G', 'T']
        return FieldOfOrder4(result_elements[result_index])

    row0=[]
    row1=[]
    row2=[]
    row3=[]
    mul=[row0, row1, row2, row3]
    def __mul__(self, other):
        # Define custom multiplication operation for the field
        element_dict = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
        
        result_index = mul[self.element][other.element]
        result_elements = ['A', 'C', 'G', 'T']
        return FieldOfOrder4(result_elements[result_index])

    def __str__(self):
        return self.element


    A = FieldOfOrder4('A')
    C = FieldOfOrder4('C')
    G = FieldOfOrder4('G')
    T = FieldOfOrder4('T')

