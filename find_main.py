import tarfile, os, sys

t = r'D:\QClaw\v0.2.35.624\resources\hermes_2.tar'
print('Opening hermes_2.tar...', flush=True)

with tarfile.open(t, 'r') as tf:
    print('Opened', flush=True)
    names = tf.getnames()
    print('Total files:', len(names), flush=True)
    
    # Search for hermes-paths or hermes_cli_main_
    hits = [n for n in names if 'hermes_paths' in n.lower() or 'hermes_cli_main' in n.lower()]
    print('hits:', hits)
    
    # Show libs structure
    libs = [n for n in names if n.startswith('libs/')]
    print('libs files:', len(libs))
    for n in sorted(libs)[:20]:
        print(' ', n)
    
    # Check for a single top-level hermes_cli dir
    cli = [n for n in names if 'hermes_cli_main' in n]
    print('hermes_cli_main:', cli)
