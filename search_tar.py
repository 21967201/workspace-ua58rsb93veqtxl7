import tarfile, os

# Search hermes_1.tar for hermes_paths, hermes_cli_main
files = [
    r'D:\QClaw\v0.2.35.624\resources\hermes_1.tar',
    r'D:\QClaw\v0.2.35.624\resources\hermes_2.tar'
]

patterns = ['hermes_paths', 'hermes_cli_main', 'hermes-paths', '找不到', 'hermes_cli/__main__']

for fp in files:
    name = fp.split('\\')[-1]
    print('Searching ' + name + '...')
    try:
        tf = tarfile.open(fp, 'r')
        members = tf.getmembers()
        hits = []
        for m in members:
            for pat in patterns:
                if pat in m.name:
                    hits.append((pat, m.name, m.size))
        print('  Hits: ' + str(len(hits)))
        for h in hits[:10]:
            print('    ' + str(h))
        tf.close()
    except Exception as e:
        print('  ERROR: ' + str(e))
