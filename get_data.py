"""Get data from the web and save it locally."""
# imports
import os
import pandas as pd
import requests
from gedcom.parser import Parser
from gedcom.element.individual import IndividualElement

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(FILE_PATH, '..', 'data')

def fetch_ged():
    """Fetch gedcom file from the web."""
    # get british royal family tree gedcom file
    r = requests.get(
        'https://raw.githubusercontent.com/neo4j-examples/discoveraurafree/main/data/royal92.ged',
        timeout=10
        )

    # save gedcom file locally
    with open(DATA_PATH + 'royal92.ged', 'wb') as ged:
        ged.write(r.content)


def parse_ged():
    """Parse gedcom file and save data to csv."""
    # parse gedcom file an generate dataframe
    gedcom_parser = Parser()
    gedcom_parser.parse_file(DATA_PATH + 'royal92.ged')

    root_child_elements = gedcom_parser.get_root_child_elements()

    # cols to parse
    cols = [
        'pointer',
        'name',
        'first',
        'last',
        'birth',
        'death',
        'gender',
        'mother',
        'father'
        ]

    df = pd.DataFrame(columns=cols)

    # iterate through all root child elements
    for e in root_child_elements:
        # check if element is an individual
        if isinstance(e, IndividualElement):
            # get data from individual
            pointer = e.get_pointer()
            name = ' '.join(e.get_name())
            first = e.get_name()[0]
            last = e.get_name()[-1]
            birth = e.get_birth_year()
            death = e.get_death_year()
            gender = e.get_gender()
            parents = gedcom_parser.get_parents(e)

            for p in parents:
                if p.get_gender() == 'F':
                    mother = p.get_pointer()
                else:
                    father = p.get_pointer()

            # append data to dataframe
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        [[
                            pointer,
                            name,
                            first,
                            last,
                            birth,
                            death,
                            gender,
                            mother,
                            father
                            ]],
                        columns=cols
                        )
                    ]
            )

    # save dataframe to csv
    df.to_csv(DATA_PATH + 'royal92.csv', index=False)


if __name__ == '__main__':
    fetch_ged()
    parse_ged()
