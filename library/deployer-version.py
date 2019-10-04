#!/usr/bin/python
import xml.etree.ElementTree as ET
import sys
import urllib

def ns_tag(tag):
    return str(ET.QName('http://maven.apache.org/POM/4.0.0', tag))

def version_from_deploy(file_path):
    # This is where we pull down releaser and extract the component version to use.
    pom_output_file = '{file_path}/pom.xml'.format(file_path=file_path)
    with open(pom_output_file, "r") as myfile:
        tree = ET.parse(myfile)
    project = tree.getroot()
    return project.findtext(ns_tag('version'))



file_path = sys.argv[1]

print str(version_from_deploy(file_path))
