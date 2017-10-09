#!/opt/stack/bin/python3
#
# this program is used to check that all the packages for a roll are built
# when 'make roll' is run
#
# @copyright@
# Copyright (c) 2006 - 2017 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@
#
# @rocks@
# Copyright (c) 2000 - 2010 The Regents of the University of California
# All rights reserved. Rocks(r) v5.4 www.rocksclusters.org
# https://github.com/Teradata/stacki/blob/master/LICENSE-ROCKS.txt
# @rocks@

import os
import sys
import stack.file
import stack.util

if len(sys.argv) != 3:
	print('error - use make manifest-check')
	sys.exit(1)

rollname  = sys.argv[1]
buildpath = sys.argv[2]

tree = stack.file.Tree(os.getcwd())

builtfiles = []
for arch in [ 'noarch', 'i386', 'x86_64', 'armv7hl' ]:
	builtfiles  += tree.getFiles(os.path.join(buildpath, 'RPMS', arch))

manifest = []

manifests = [ 'manifest', 'manifest.%s' % rollname ]
try:
	for f in os.listdir(os.path.join(buildpath, 'manifest.d')):
		manifests.append(os.path.join(buildpath, 'manifest.d', f))
except FileNotFoundError:
	pass

found = False
for filename in manifests:
	if not os.path.exists(filename):
		continue
	print('searching %s' % filename)
	found = True
	file = open(filename, 'r')
	for line in file.readlines():
		l = line.strip()
		if len(l) == 0 or (len(l) > 0 and l[0] == '#'):
			continue
		if l not in manifest: # ignore duplicates
			manifest.append(l)
	file.close()

if not found:
	print('Cannot find any manifest files')
	sys.exit(0)

built = []
notmanifest = []

for rpm in builtfiles:
	try:
		pkg = rpm.getPackageName()
		if pkg in manifest:
			if pkg not in built:
				#
				# this check will catch duplicate package
				# basenames -- this occurs when the i386 and
				# x86_64 versions of the same package are in
				# a roll
				#
				built.append(pkg)
		else:
			notmanifest.append(pkg)
	except:
		pass

exit_code = 0
if len(manifest) != len(built):
	print('\nERROR - the following packages were not built:')
	for pkg in manifest:
		if pkg not in built:
			print('\t%s' % pkg)
	exit_code += 1

if len(notmanifest) > 0:
	print('\nERROR - the following packages were built but not in manifest:')
	for pkg in notmanifest:
		print('\t%s' % pkg)
	exit_code += 1

if exit_code == 0:
	print('done')
sys.exit(exit_code)