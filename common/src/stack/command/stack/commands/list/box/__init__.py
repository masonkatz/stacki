# @SI_Copyright@
# Copyright (c) 2006 - 2017 StackIQ Inc.
# All rights reserved. stacki(r) v4.0 stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @SI_Copyright@
#
# @Copyright@
# Copyright (c) 2000 - 2010 The Regents of the University of California
# All rights reserved. Rocks(r) v5.4 www.rocksclusters.org
# https://github.com/Teradata/stacki/blob/master/LICENSE-ROCKS.txt
# @Copyright@

import stack.commands


class command(stack.commands.list.command,
	      stack.commands.BoxArgumentProcessor):
	pass


class Command(command):
	"""
	Lists the pallets and carts that are associated with boxes.
	
	<arg optional='1' type='string' name='box' repeat='1'>
	Optional list of box names.
	</arg>
		
	<example cmd='list box'>
	List all known box definitions.
	</example>
	"""

	def run(self, params, args):
		pallets = {}
		carts	= {}

		for box in self.getBoxNames(args):
			for name, version, rel, arch, osname in self.getBoxPallets(box):
				fullname = '%s-%s' % (name, version)
				if rel:
					fullname += '-%s' % rel

				if box not in pallets:
					pallets[box] = []
				pallets[box].append(fullname)
			
		for row in self.call('list.cart'):
			if row['boxes']:
				for box in row['boxes'].split():
					if box not in carts:
						carts[box] = []
					carts[box].append(row['name'])

		self.beginOutput()

		for box in self.getBoxNames(args):
			id, os = self.db.select("""b.id, o.name from
				boxes b, oses o where b.name='%s'
				and b.os=o.id""" % box)[0]

			if box not in carts:
				carts[box] = []

			if box not in pallets:
				pallets[box] = []

			self.addOutput(box, (os, ' '.join(pallets[box]),
					     ' '.join(carts[box])))
			
		self.endOutput(header=['name', 'os', 'pallets', 'carts'],
			trimOwner=False)

