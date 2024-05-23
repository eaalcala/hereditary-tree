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
                "trait": float(data['trait'])
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
                "trait": float(data['trait'])
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
            father = people[person]['father']
            mother = people[person]['mother']
            probabilities[person] = trait_helper(father, mother, probabilities, people)
    


# calculates probability of a child having a trait given parent's trait & genotype information
def trait_helper(father, mother, probabilities, people):
    to_return = {
        "gene": {
            2: 0,
            1: 0,
            0: 0
        },
        "trait": 0
    }

    father_data = probabilities[father]
    mother_data = probabilities[mother]


    # recursively update family tree
    if father_data['trait'] == None:
        grandfather = people[father]['father']
        grandmother = people[father]['mother']
        father_data = trait_helper(grandfather, grandmother, probabilities, people)

    if mother_data['trait'] == None:
        grandfather = people[mother]['father']
        grandmother = people[mother]['mother']
        mother_data = trait_helper(grandfather, grandmother, probabilities, people)

    gfather = father_data['gene']
    gmother = mother_data['gene']

    to_return['gene'][2] =  1.0 * gfather[2] * gmother[2] + \
                            0.5 * gfather[2] * gmother[1] + \
                            0.5 * gfather[1] * gmother[2] + \
                            0.25 * gfather[1] * gmother[1]

    to_return['gene'][1] = 0.5 * gfather[2] * gmother[1] + \
                            0.5 * gfather[1] * gmother[2] + \
                            0.5 * gfather[1] * gmother[1] + \
                            1.0 * gfather[2] * gmother[0] + \
                            1.0 * gfather[0] * gmother[2] + \
                            0.5 * gfather[1] * gmother[0] + \
                            0.5 * gfather[0] * gmother[1]

    to_return['gene'][0] = 1.0 * gfather[0] * gmother[0] + \
                            0.5 * gfather[1] * gmother[0] + \
                            0.5 * gfather[0] * gmother[1] + \
                            0.25 * gfather[1] * gmother[1]

    to_return['trait'] = to_return['gene'][2]
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