from pathlib import Path
root = Path('demo')
root.mkdir(exist_ok=False)
for name in ('report.txt', 'notes.txt', 'sales.csv', 'README'):
    (root / name).write_text('Example data only\n', encoding='utf-8')
print('Created demo with four sample files')
