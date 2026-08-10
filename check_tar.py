import tarfile

tars = [
    r'D:\QClaw\v0.2.35.624\resources\hermes_0.tar',
    r'D:\QClaw\v0.2.35.624\resources\hermes_1.tar',
    r'D:\QClaw\v0.2.35.624\resources\hermes_2.tar'
]

for t in tars:
    try:
        with tarfile.open(t, 'r') as tf:
            names = tf.getnames()
            print(t.split('\\')[-1], ':', len(names), 'files')
            libs = [n for n in names if n.startswith('libs/') and n.count('/') == 1]
            for n in sorted(libs)[:30]:
                print(' ', n)
    except Exception as e:
        print('error:', t.split('\\')[-1], e)
