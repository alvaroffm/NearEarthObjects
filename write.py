import csv
import json
from helpers import datetime_to_str


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for approach in results:
            writer.writerow({
                'datetime_utc': datetime_to_str(approach.time),
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'designation': approach.neo.designation,
                'name': approach.neo.name if approach.neo.name else '',
                'diameter_km': approach.neo.diameter if approach.neo.diameter else 'nan',
                'potentially_hazardous': str(approach.neo.hazardous)
            })


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    data = []

    for approach in results:
        data.append({
            'datetime_utc': datetime_to_str(approach.time),
            'distance_au': approach.distance,
            'velocity_km_s': approach.velocity,
            'neo': {
                'designation': approach.neo.designation,
                'name': approach.neo.name if approach.neo.name else '',
                'diameter_km': approach.neo.diameter if approach.neo.diameter else float('nan'),
                'potentially_hazardous': approach.neo.hazardous
            }
        })

    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=2)
