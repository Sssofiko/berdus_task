import re

# Способ 1
data = {
    'author': 'root',
    'previous_snapshot_id': 'cab83dea6db62d2fc0ffea1b93acdd10ac9d5cae',
    'create_time': 'Fri Jul 17 08:51:00 MSK 2020',
    'snapshot_id': '609ec1d9577c070e53c8a3073e74dbc4c05d32ad',
    'description': 'Fri Jul 17 08:51:00 MSK 2020'
}

# Регулярное выражение для поиска значения snapshot_id
match = re.search(r"'snapshot_id':\s*'(\w+)'", str(data))

if match:
    snapshot_id = match.group(1)
    first_six_chars = snapshot_id[:6]
    print("Первые 6 символов snapshot_id:", first_six_chars)
else:
    print("snapshot_id не найден")

# # Способ 2
# snapshot_id = data.get('snapshot_id')
#
# if snapshot_id:
#     first_six_chars = snapshot_id[:6]
#     print("Первые 6 символов snapshot_id:", first_six_chars)
# else:
#     print("snapshot_id не найден")

# # Способ 3
# data = "{'author': 'root', 'previous_snapshot_id': 'cab83dea6db62d2fc0ffea1b93acdd10ac9d5cae', 'create_time': 'Fri Jul 17 08:51:00 MSK 2020', 'snapshot_id': '609ec1d9577c070e53c8a3073e74dbc4c05d32ad', 'description': 'Fri Jul 17 08:51:00 MSK 2020'}"
#
# match = re.search(r"'snapshot_id':\s*'([a-f0-9]{6})", data)
#
# if match:
#     first_six_chars = match.group(1)
#     print("Первые 6 символов snapshot_id:", first_six_chars)
# else:
#     print("snapshot_id не найден")
