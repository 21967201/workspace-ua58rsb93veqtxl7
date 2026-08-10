import tarfile

# Check hermes_0.tar content
t = r'D:\QClaw\v0.2.35.624\resources\hermes_0.tar'
with tarfile.open(t, 'r') as tf:
    names = tf.getnames()
    print('hermes_0.tar contents:')
    for n in sorted(names):
        print(' ', n)
