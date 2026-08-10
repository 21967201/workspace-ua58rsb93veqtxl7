import tarfile, os

tf = tarfile.open(r'D:\QClaw\v0.2.35.624\resources\hermes_2.tar', 'r')
m = tf.getmember('hermes/libs/hermes_cli/__main__.py')
f = tf.extractfile(m)
content = f.read()
tf.close()

print('File size: ' + str(len(content)))
print('Content:')
print(content.decode('utf-8', errors='replace'))
