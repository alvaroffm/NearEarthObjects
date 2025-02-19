"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path=r'./data/neos.csv'):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    csv_data = []
    with open(neo_csv_path, 'r') as f:
        neos = csv.reader(f)
        for row in neos:
            csv_data.append(row)

    posicion_pdes = csv_data[0].index('pdes')
    posicion_name = csv_data[0].index('name')
    posicion_pha = csv_data[0].index('pha')
    posicion_diameter = csv_data[0].index('diameter')

    posicion_columna = posicion_pdes

    neos_encontrados = []
    contador_fake = 0
    for fila in csv_data[1:]:
        nombre_completo = fila[posicion_name]
        id_neo = fila[posicion_pdes]
        try:
            diametro = float(fila[posicion_diameter])
        except ValueError:
            diametro = float('nan')
            contador_fake += 1
        hazard = True if fila[posicion_pha] == 'Y' else False

        info = dict(designation=id_neo, name=nombre_completo, diameter=diametro, hazardous=hazard)

        ast = NearEarthObject(**info)
        neos_encontrados.append(ast)

    return neos_encontrados


def load_approaches(cad_json_path=r'./data/cad.json'):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approaches = []
    with open(cad_json_path, 'r') as file:
        cad = json.load(file)

    for fila_cad in cad['data'][:]:
        info = dict(
            designation=fila_cad[0],
            time=fila_cad[3],
            distance=float(fila_cad[4]),
            velocity=float(fila_cad[7])
        )

        approaches.append(CloseApproach(**info))

    return approaches


if __name__ == '__main__':

    dimNeos = load_neos()
    dimApproaches = load_approaches()
