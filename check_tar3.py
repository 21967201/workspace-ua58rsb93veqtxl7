import os
fp = r'D:\QClaw\v0.2.35.624\resources\hermes_0.tar'
print('File size:', os.path.getsize(fp))
print('Magic hex:', open(fp, 'rb').read(8).hex())
