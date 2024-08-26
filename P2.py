import json
import csv

sarif_file_path = 'SARIF.sarif'
csv_file_path = 'output.csv'

with open(sarif_file_path, 'r') as sarif_file:
    sarif_data = json.load(sarif_file)

with open(csv_file_path, 'w', newline='') as csv_file:
    fieldnames = ['location', 'line', 'column', 'message', 'toolname', 'toolversion']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for run in sarif_data.get('runs', []):
        tool = run.get('tool', {})
        for result in run.get('results', []):
            location = result.get('locations', [{}])[0].get('physicalLocation', {}).get('artifactLocation', {}).get(
                'uri', '')
            line = result.get('locations', [{}])[0].get('physicalLocation', {}).get('region', {}).get('startLine', '')
            column = result.get('locations', [{}])[0].get('physicalLocation', {}).get('region', {}).get('startColumn',
                                                                                                        '')
            message = result.get('message', {}).get('text', '')
            toolname = tool.get('driver', {}).get('name', '')
            toolversion = tool.get('driver', {}).get('version', '')

            writer.writerow({
                'location': location,
                'line': line,
                'column': column,
                'message': message,
                'toolname': toolname,
                'toolversion': toolversion
            })

print(f'CSV файл сохранен по пути {csv_file_path}')
