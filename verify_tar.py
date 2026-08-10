import tarfile, os

files = [
    r'D:\QClaw\v0.2.35.624\resources\hermes_0.tar',
    r'D:\QClaw\v0.2.35.624\resources\hermes_1.tar',
    r'D:\QClaw\v0.2.35.624\resources\hermes_2.tar'
]

for fp in files:
    size = os.path.getsize(fp)
    name = fp.split('\\')[-1]
    print(name + ': ' + str(size) + ' bytes')
    with open(fp, 'rb') as f:
        magic = f.read(8)
    print('  Magic: ' + str(magic))
    
    try:
        tf = tarfile.open(fp, 'r')
        members = tf.getmembers()
        print('  Members: ' + str(len(members)))
        for m in members[:3]:
            print('    ' + m.name + ' (' + str(m.size) + ' bytes)')
        tf.close()
    except Exception as e:
        print('  ERROR: ' + str(e))
