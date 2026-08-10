import tarfile, os

# hermes_2.tar has 21393 files. Let's look for files containing 'paths' in name
tf = tarfile.open(r'D:\QClaw\v0.2.35.624\resources\hermes_2.tar', 'r')
members = tf.getmembers()

# Sort by name
by_name = sorted(members, key=lambda m: m.name)

hits = [m for m in by_name if 'paths' in m.name.lower()]
print('Files with "paths" in name (' + str(len(hits)) + '):')
for m in hits[:20]:
    print('  ' + m.name + ' (' + str(m.size) + ')')

# Also check hermes_1
tf.close()
tf = tarfile.open(r'D:\QClaw\v0.2.35.624\resources\hermes_1.tar', 'r')
members = tf.getmembers()
hits = [m for m in members if 'paths' in m.name.lower()]
print('\nhermes_1 - Files with "paths" (' + str(len(hits)) + '):')
for m in hits[:10]:
    print('  ' + m.name)

tf.close()
