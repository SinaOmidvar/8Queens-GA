import random
import itertools
population_size = 20


class Gene():
    def __init__(self, instance):
        self.instance = instance

    def crossover(self, other):
        cut = random.randint(2, 6)
        child_1 = Gene(self.instance[:cut] + other.instance[cut:])
        child_2 = Gene(self.instance[cut:] + other.instance[:cut])
        return [child_1, child_2]

    def mutate(self):
        mutant_indices = random.choices(range(8), k=2)
        mutant_values = random.choices(range(1, 9), k=2)
        mutant_instance = self.instance.copy()
        mutant_instance[mutant_indices[0]] = mutant_values[0]
        mutant_instance[mutant_indices[1]] = mutant_values[1]
        return Gene(mutant_instance)

    def fitness_function(self):
        threats = 0
        for i in range(7):
            for j in range(i + 1, 8):
                if self.instance[i] == self.instance[j]:
                    threats += 1
        for i in range(7):
            for j in range(i + 1, 8):
                if abs(self.instance[j] - self.instance[i]) == abs(j - i):
                    threats += 1
        return 28 - threats


def evalution(iterable):
    fitness_list = []
    for gene in iterable:
        fitness_list.append(gene.fitness_function())
    return fitness_list


def generate():
    DNA = list(range(1, 9))
    for i in range(population_size):
        random.shuffle(DNA)
        chrom = DNA.copy()
        new_gene = Gene(chrom)
        init_population[new_gene] = new_gene.fitness_function()


def selection(generation):
    for i in range(int(population_size / 2)):
        selected = random.choices(
            list(generation.keys()), weights=list(generation.values()), k=2)
        child_1, child_2 = selected[0].crossover(selected[1])
        next_population[child_1] = child_1.fitness_function()
        next_population[child_2] = child_2.fitness_function()


def mutation(generation):
    for gene in generation.keys():
        new_gene = gene.mutate()
        mutants[new_gene] = new_gene.fitness_function()


init_population = {}
generate()

while True:
    next_population = {}
    mutants = {}
    selection(init_population)
    mutation(next_population)

    total = init_population.copy()
    total.update(next_population)
    total.update(mutants)

    total = dict(sorted(total.items(), key=lambda item: item[1]))
    elites = dict(itertools.islice(total.items(), 40, 60))

    best = max(elites.values())
    if best == 28:
        print("Solution Found")
        answer = list(elites.items())[-1][0].instance
        print(answer)
        for i in range(8):
            x = answer[i] - 1
            for j in range(8):
                if j == x:
                    print('[Q]', end='')
                else:
                    print('[ ]', end='')
            print()

        print()
        break
    else:
        init_population = {}
        init_population = elites.copy()
