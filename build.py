#!/usr/bin/env python
import sys
import os
import subprocess
import glob

python = os.path.normpath(sys.executable)
python_dir = os.path.dirname(python)

print('validating openhltest models...')
data_models_dir = os.path.normpath('%s/models' % os.path.dirname(__file__))
pyang = [
	sys.executable,
	os.path.normpath('%s/Scripts/pyang' % python_dir),
	'--strict',
	'-p',
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
print('done')
