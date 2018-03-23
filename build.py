#!/usr/bin/env python
import sys
import os
import subprocess
import glob

python = os.path.normpath(sys.executable)
python_dir = os.path.dirname(python)

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

pyang = find('pyang', os.path.normpath('%s/..'% python_dir))
print('pyang location %s' % pyang)

print('validating openhltest models in %s...' % os.getcwd())
data_models_dir = './models'
pyang = [
    sys.executable,
    pyang,
    '--strict',
    '--path',
    data_models_dir,
    'openhltest-session.yang'
]
pyang_process = subprocess.Popen(pyang, bufsize=1, cwd=data_models_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
while pyang_process.returncode is None:
    stdout_data, stderr_data = pyang_process.communicate()
    if pyang_process.returncode == 0:
        print(stdout_data)
    elif pyang_process.returncode > 0:
        print(stderr_data)
sys.exit(pyang_process.returncode)
