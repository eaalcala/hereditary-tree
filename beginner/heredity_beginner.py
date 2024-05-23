import csv
import sys

import argparse

def arg_parser():
    parser = argparse.ArgumentParser(
        prog='Hereditary Tree',
        description='Finds probabilities of inheriting trait for every person in a family'
    )
    # Define the command-line arguments.
    parser.add_argument("i", type=file_type_checker('.csv'), help="Input file of type .csv")
    return parser.parse_args()

def file_type_checker(extension):
    def check(file_name):
        global error
        if not file_name.lower().endswith(extension):
            # Usually you would throw an exception here, but it's easier to test with a string variable
            error = f"File must be a {extension} file"
            return file_name
        return file_name
    return check


def main():
    # Parse the command-line arguments.
    ARGS = arg_parser()

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(ARGS.i)

    # Keep track of gene and trait probabilities for each person
    probabilities = dict()

    for person, data in people.items():
        if data['trait'] == 1:
            probabilities[person] = {
                "gene": {
                    2: 1,
                    1: 0,
                    0: 0
                },
                "trait": int(data['trait'])
            }
        elif data['trait'] == None:
            probabilities[person] = {
                "gene": {
                    2: 0,
                    1: 0,
                    0: 0
                },
                "trait": data['trait']
            }
        else:
            probabilities[person] = {
                "gene": {
                    2: 0,
                    1: 0,
                    0: 1
                },
                "trait": int(data['trait'])
            }


    calculate_trait(probabilities, people)

    # names = set(people)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            if field.capitalize() == "Trait":
                print(f"  {field.capitalize()}: {probabilities[person][field]}")
                continue
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def calculate_trait(probabilities, people):
    for person, data in probabilities.items():
        if data['trait'] == None:
            father = probabilities[people[person]['father']]
            mother = probabilities[people[person]['mother']]
            fgenotype = parent_genotype(father['gene'])
            mgenotype = parent_genotype(mother['gene'])
            probabilities[person] = trait_helper(fgenotype, mgenotype)
    

# Note: This method will only work for beginners.
# Here we just walk through the gene and check what genotype the parent has
# Since it is only 0 or 2 for the beginner case, we can just return true
# Whenever one of the values of the dictionary is 1
def parent_genotype(gene):
    for key, val in gene.items():
        if val == 1:
            return key

# calculates probability of a child having a trait given parent's trait & genotype information
def trait_helper(genes1, genes2):

    maximum = max(genes1, genes2)
    minimum = min(genes1, genes2)
    to_return = {
        "gene": {
            2: 0,
            1: 0,
            0: 0
        },
        "trait": 0
    }
    if maximum == 2 and minimum == 2:
        to_return['gene'][2] = 1
        to_return['trait'] = 1
        return to_return

    if maximum == 2 and minimum == 1:
        to_return['gene'][2] = 0.5
        to_return['gene'][1] = 0.5
        to_return['trait'] = 0.5
        return to_return


    if maximum == 2 and minimum == 0:
        to_return['gene'][1] = 1
        to_return['trait'] = 0
        return to_return

    if maximum == 1 and minimum == 1:
        to_return['gene'][2] = 0.25
        to_return['gene'][1] = 0.5
        to_return['gene'][0] = 0.25
        to_return['trait'] = 0.25
        return to_return

    to_return['gene'][0] = 1
    return to_return



def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


if __name__ == "__main__":
    main()