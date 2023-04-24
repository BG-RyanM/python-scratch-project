import numpy as np

# Define two 3-dimensional vectors
vector_a = np.array([1, 2, 3])
vector_b = np.array([4, 5, 6])
vector_c = np.array([-1, 0, -2])
vector_a = vector_a / np.linalg.norm(vector_a)
vector_b = vector_b / np.linalg.norm(vector_b)
vector_c = vector_c / np.linalg.norm(vector_c)

# Compute the cross product of the vectors
cross_product = np.cross(vector_a, vector_b)

# Compute the dot product of the vectors
dot_product = np.dot(vector_a, vector_b)

# Print the results
print("Vector A:", vector_a)
print("Vector B:", vector_b)
print("Cross product:", cross_product)
print("Dot product:", dot_product)

print(f"Just to be sure {vector_c * np.dot(vector_a, vector_b)} and {np.dot(vector_a, vector_b) * vector_c}")

print("----------------------------------------------------------------")

vector_a = np.array([1.0, 0.0, 0.0])
vector_b = np.array([1.0, 0.0, 0.0])
vector_c = np.array([0.0, 2.0, 0.0])

print("Vector A:", vector_a)
print("Vector B:", vector_b)
print("Vector C:", vector_c)

print(f"Just to be sure 2 {vector_c * np.dot(vector_a, vector_b)} and {np.dot(vector_a, vector_b) * vector_c}")

# = c (a . b) // Commutative property of scalar multiplication
commutative_1 = vector_c * np.dot(vector_a, vector_b)

# = b (a . c) // Commutative property of dot product
commutative_2 = vector_b * np.dot(vector_a, vector_c)

print("c (a . b) =", commutative_1)
print("b (a . c) =", commutative_2)

# Trying out associative property: a (b . c) =? (a . b) c
assoc_left = vector_a * np.dot(vector_b, vector_c)
assoc_right = np.dot(vector_a, vector_b) * vector_c
print("a (b . c) =", assoc_left)
print("(a . b) c =", assoc_right)

print("----------------------------------------------------------------")

for i in range(5):

    three_vectors = [np.random.randint(100, size=(3)) - np.array([50, 50, 50]) for v in range(3)]
    three_vectors = [vect / np.linalg.norm(vect) for vect in three_vectors]
    vector_a, vector_b, vector_c = three_vectors[0], three_vectors[1], three_vectors[2]

    # Where . is a vector dot product, is the following true? (a . c) b - (a . b) c = [(a . c) - (b . c)] b

    print("round", i)

    formula_left = np.dot(vector_a, vector_c) * vector_b - np.dot(vector_a, vector_b) * vector_c
    print("(a . c) b - (a . b) c =", formula_left)
    formula_right = (np.dot(vector_a, vector_c ) - np.dot(vector_b, vector_c)) * vector_b
    print("[(a . c) - (b . c)] b", formula_right)

