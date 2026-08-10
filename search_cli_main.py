import tarfile, os

# Search ALL files in hermes_2.tar for hermes_cli_main_ string content
tf = tarfile.open(r'D:\QClaw\v0.2.35.624\resources\hermes_2.tar', 'r')
members = tf.getmembers()

# Find files with 'hermes_cli_main_' in the name
cli_main = [m for m in members if 'hermes_cli_main' in m.name]
print('hermes_cli_main in filenames:', cli_main)

# Also check for any .py files in hermes_cli/
cli_files = [m for m in members if 'hermes_cli/' in m.name]
print('\nAll hermes_cli/ files (' + str(len(cli_files)) + '):')
for m in sorted(cli_files):
    print('  ' + m.name + ' (' + str(m.size) + ' bytes)')

tf.close()
