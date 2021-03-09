# -*- coding: utf-8 -*-

import re
import simplejson as json
import six
import sys
if sys.version_info[0] >= 3:
	unicode = str

def json_load_as_str(file_handle):
	return byteify(json.load(file_handle, object_hook=byteify), ignore_dicts=True)


def json_loads_as_str(json_text):
	return byteify(json.loads(json_text, object_hook=byteify), ignore_dicts=True)


def byteify(data, ignore_dicts=False):
	if isinstance(data, six.string_types):
		return data
	if isinstance(data, list):
		return [byteify(item, ignore_dicts=True) for item in data]
	if isinstance(data, dict) and not ignore_dicts:
		return dict([(byteify(key, ignore_dicts=True), byteify(value, ignore_dicts=True)) for key, value in six.iteritems(data)])
	return data