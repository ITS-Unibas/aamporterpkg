#!/usr/bin/python

import sys
import os
import shutil
import subprocess


def validate_input(path_to_file, basedir_cache):
	pkg_name = os.path.splitext(os.path.basename(path_to_file))[0]
	create_pkg = True

	if os.path.splitext(path_to_file)[1] != ".dmg":
		print "Only dmg files are supported. This is not a valide file format: " + path_to_file
		create_pkg = False

	if os.path.exists(os.path.join(basedir_cache, pkg_name + ".pkg")):
		print "Nothing to do. File allready present at " + os.path.join(basedir_cache, pkg_name + ".pkg")
		create_pkg = False

	return create_pkg, pkg_name


def create_template(pkg_scripts, pkg_template, basedir_cache):
	for path in pkg_scripts, pkg_template, basedir_cache:
		if not os.path.exists(path):
			print "Creating folder: " + path
			os.makedirs(path)


def copy_payload(path_to_file, pkg_template):
	print "Copying file %s to destination %s" % (path_to_file, pkg_template)
	shutil.copy(path_to_file, pkg_template)


def prepare_script(postinstall_script, pkg_postinstall_script, pkg_name):
	pkg_postinstall_script = os.path.join(pkg_scripts, "postinstall")
	print "Generate postinstall script at %s from template %s" % (pkg_postinstall_script, postinstall_script)
	payload_name = {'placeholder':pkg_name}

	with open(pkg_postinstall_script, "w") as output_file, open(postinstall_script) as input_file:
		for line in input_file:
			for key, value in payload_name.iteritems():
				line = line.replace(key, value)
				output_file.write(line)

	print "Changing permissions for %s" % (pkg_postinstall_script)
	os.chmod(pkg_postinstall_script, 0755)


def build_pkg(basedir_pkg, pkg_scripts, pkg_name, basedir_cache):
	pkg_payload = os.path.join(basedir_pkg, "payload")
	pkg_output_path = os.path.join(basedir_cache, pkg_name + ".pkg")

	cmd = ['/usr/bin/pkgbuild',
		'--root', pkg_payload,
		'--scripts', pkg_scripts,
		'--identifier', "com.aamporterpkg." + pkg_name,
		'--ownership', "recommended",
		'--install-location', '/',
		'--quiet', pkg_output_path
	]
	print "Creating pkg: %s" % (pkg_output_path)
	subprocess.call(cmd)


def cleanup(basedir_pkg):
	if os.path.exists(basedir_pkg):
		print "Deleting temporary folder: " + basedir_pkg
		shutil.rmtree(basedir_pkg)


basedir = os.path.dirname(os.path.abspath(__file__))
basedir_pkg = os.path.join(basedir, "tmp")
basedir_cache = os.path.join(basedir, "cache")
postinstall_script = os.path.join(basedir, "scripts", "postinstall")
pkg_scripts = os.path.join(basedir_pkg, "scripts")
pkg_template = os.path.join(basedir_pkg, "payload", "private", "tmp")

for path_to_file in sys.argv[1:]:
	create_pkg, pkg_name = validate_input(path_to_file, basedir_cache)
	if create_pkg:
		print "Creating pkg for input %s" % (path_to_file)
		cleanup(basedir_pkg)
		create_template(pkg_scripts, pkg_template, basedir_cache)
		copy_payload(path_to_file, pkg_template)
		prepare_script(postinstall_script, pkg_scripts, pkg_name)
		build_pkg(basedir_pkg, pkg_scripts, pkg_name, basedir_cache)
		cleanup(basedir_pkg)

