# @copyright@
# Copyright (c) 2006 - 2019 Teradata
# All rights reserved. Stacki(r) v5.x stacki.com
# https://github.com/Teradata/stacki/blob/master/LICENSE.txt
# @copyright@

ROLLROOT	= ../../../../../../..

include $(STACKBUILD)/etc/CCRules.mk

EXTRACT := xzcat

include images.mk
include ../../../common/images.mk

install::
SHA = $(shell sha256sum sles-stacki.img | awk '{print $$1;}')

clean::
	rm -rf cache
