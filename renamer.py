"""Rename immediate files; preview by default, never overwrite existing names."""
import argparse
from pathlib import Path


def plan(folder, prefix='', replace=None, number=False, start=1):
    root = Path(folder).resolve()
    if not root.is_dir():
        raise ValueError('Folder does not exist')
    if replace and not replace[0]:
        raise ValueError('Replacement search text cannot be empty')
    if start < 0:
        raise ValueError('Start must be nonnegative')
    files = sorted(p for p in root.iterdir() if p.is_file() and not p.is_symlink() and not p.name.startswith('.'))
    moves, names = [], set()
    for index, source in enumerate(files, start):
        stem = source.stem.replace(*replace) if replace else source.stem
        name = prefix + (f'{index:03d}_' if number else '') + stem + source.suffix
        if any(c in name for c in '<>:"/\\|?*') or any(ord(c) < 32 for c in name) or name.endswith((' ', '.')) or name in ('', '.', '..'):
            raise ValueError(f'Invalid filename: {name}')
        if name.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)), *(f'LPT{i}' for i in range(1, 10))}:
            raise ValueError(f'Reserved filename: {name}')
        target = root / name
        if name.casefold() in names:
            raise ValueError(f'Duplicate target: {name}')
        names.add(name.casefold())
        if source.name == name:
            continue
        if target.exists() or source.name.casefold() == name.casefold():
            raise ValueError(f'Target already exists: {name}')
        moves.append((source, target))
    return moves


def rename(folder, apply=False, **options):
    moves = plan(folder, **options)
    if apply:
        completed = []
        try:
            for source, target in moves:
                if target.exists():
                    raise ValueError(f'Target already exists: {target}')
                source.rename(target)
                completed.append((source, target))
        except (OSError, ValueError):
            for source, target in reversed(completed):
                if not source.exists():
                    target.rename(source)
            raise
    return moves


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder')
    parser.add_argument('--prefix', default='')
    parser.add_argument('--replace', nargs=2, metavar=('OLD', 'NEW'))
    parser.add_argument('--number', action='store_true')
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--apply', action='store_true')
    args = vars(parser.parse_args())
    try:
        moves = rename(**args)
        for source, target in moves:
            print(f'{source.name} -> {target.name}')
        print(f'{len(moves)} file(s); ' + ('completed' if args['apply'] else 'preview only; use --apply'))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
