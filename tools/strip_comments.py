#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# strip_comments.py - Remove comentarios de arquivos NVGT (AngelScript).
#
# Trata corretamente:
#   - comentarios de linha   //
#   - comentarios de bloco   /* ... */  (aninhados, como no AngelScript)
#   - strings "..." e '...' com escapes
#   - heredocs de tres aspas (conteudo bruto, nada e removido dentro)
#   - diretivas #include / #pragma (nao sao tocadas)
#
# Uso:
#   python tools/strip_comments.py --dry-run             # so relata
#   python tools/strip_comments.py                       # aplica in-place
#   python tools/strip_comments.py --ext .nvgt --root .  # customizado

import argparse
import os
import sys

TRIPLE = '"' * 3
BACKSLASH = chr(92)


def strip_source(src):
    out = []
    i = 0
    n = len(src)
    block_depth = 0

    while i < n:
        c = src[i]

        # --- dentro de comentario de bloco ---
        if block_depth:
            if src.startswith('/*', i):
                block_depth += 1
                i += 2
                continue
            if src.startswith('*/', i):
                block_depth -= 1
                i += 2
                continue
            # preserva quebras de linha para nao colar codigo
            if c == '\n':
                out.append('\n')
            i += 1
            continue

        # --- heredoc de tres aspas ---
        if src.startswith(TRIPLE, i):
            end = src.find(TRIPLE, i + 3)
            if end == -1:
                out.append(src[i:])
                break
            end += 3
            out.append(src[i:end])
            i = end
            continue

        # --- string / char literal ---
        if c == '"' or c == "'":
            quote = c
            out.append(c)
            i += 1
            while i < n:
                ch = src[i]
                out.append(ch)
                i += 1
                if ch == BACKSLASH and i < n:
                    out.append(src[i])
                    i += 1
                    continue
                if ch == quote:
                    break
                if ch == '\n':  # string nao fechada na linha: aborta o estado
                    break
            continue

        # --- comentario de linha ---
        if src.startswith('//', i):
            while i < n and src[i] != '\n':
                i += 1
            continue

        # --- abertura de bloco ---
        if src.startswith('/*', i):
            block_depth = 1
            i += 2
            continue

        out.append(c)
        i += 1

    return ''.join(out)


def clean_lines(original, stripped):
    # Remove linhas que viraram vazias por causa da limpeza, preservando as
    # linhas em branco que ja existiam no original.
    orig_lines = original.split('\n')
    new_lines = stripped.split('\n')
    result = []
    for idx, line in enumerate(new_lines):
        line = line.rstrip()
        if line:
            result.append(line)
            continue
        was_blank = idx < len(orig_lines) and not orig_lines[idx].strip()
        if was_blank:
            result.append('')
    # colapsa linhas em branco consecutivas em uma so
    collapsed = []
    blanks = 0
    for line in result:
        if line:
            blanks = 0
            collapsed.append(line)
        else:
            blanks += 1
            if blanks <= 1:
                collapsed.append('')
    while collapsed and not collapsed[-1]:
        collapsed.pop()
    return '\n'.join(collapsed) + '\n'


def process(path, dry_run):
    with open(path, 'r', encoding='utf-8', errors='surrogateescape', newline='') as fh:
        raw = fh.read()
    text = raw.replace('\r\n', '\n').replace('\r', '\n')
    new = clean_lines(text, strip_source(text))
    if new == text:
        return (0, 0)
    removed = len(text.split('\n')) - len(new.split('\n'))
    if not dry_run:
        with open(path, 'w', encoding='utf-8', errors='surrogateescape', newline='\n') as fh:
            fh.write(new)
    return (1, removed)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--ext', action='append', default=None,
                    help='extensoes a processar (padrao: .nvgt)')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--quiet', action='store_true')
    args = ap.parse_args()
    exts = tuple(args.ext or ['.nvgt'])

    skip_dirs = {'.git', 'node_modules', '__pycache__', 'backups', 'venv', '.venv'}
    changed = total = removed_total = 0

    for dirpath, dirnames, filenames in os.walk(args.root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for name in sorted(filenames):
            if not name.lower().endswith(exts):
                continue
            path = os.path.join(dirpath, name)
            total += 1
            ch, rem = process(path, args.dry_run)
            changed += ch
            removed_total += rem
            if ch and not args.quiet:
                print(('[dry] ' if args.dry_run else '') + path + ': -' + str(rem) + ' linhas')

    print('\nArquivos analisados: %d | alterados: %d | linhas removidas: %d'
          % (total, changed, removed_total))
    return 0


if __name__ == '__main__':
    sys.exit(main())
