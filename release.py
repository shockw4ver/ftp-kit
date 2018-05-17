import toml
import hashlib
import time
import os
from ftplib import FTP

CDN = toml.load('./release.toml')['info']

RELEASE = hashlib.sha256(CDN['appSecret'] + CDN['appName'] + bytes(time.time())).hexdigest()

print RELEASE

def dirlist (path, allfile = [], alldir = []):
  filelist = os.listdir(path)

  for filename in filelist:
    filepath = os.path.join(path, filename)
    if os.path.isdir(filepath):
      alldir.append(filename)
      dirlist(filepath, allfile)
    else:
      allfile.append(filepath)
  
  return (allfile, alldir)

def upload (seed):
  f = FTP(CDN['CDN_HOST'])
  f.login(CDN['USERNAME'], CDN['PASSWORD'])
  f.cwd(CDN['appName'])
  f.mkd(RELEASE)
  f.cwd(RELEASE)
  f.mkd('dist')

  buffer_size = 1024

  for path in seed[1]:
    f.mkd(path)

  for file in seed[0]:
    target = file.replace('/dist', '')
    print target
    f.storbinary('STOR ' + target, open(file, 'rb'), buffer_size)

upload (dirlist('./dist'))