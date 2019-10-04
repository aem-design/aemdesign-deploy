#!/usr/bin/python
import xml.etree.ElementTree as ET
import sys
import urllib

def ns_tag(tag):
    return str(ET.QName('http://maven.apache.org/POM/4.0.0', tag))

def version_from_deploy(nexus_artifact, file_path):
    # This is where we pull down releaser and extract the component version to use.
    pom_output_file = '{file_path}/pom.xml'.format(file_path=file_path)
    wrap_module_mame = 'deployer'
    with open(pom_output_file, "r") as myfile:
        tree = ET.parse(myfile)
    project = tree.getroot()

    version_element = project.findtext(ns_tag('version'))
    return version_element

    # dependencies_element = project.find(ns_tag('dependencies'))
    # dependencies = dependencies_element.findall(ns_tag("dependency"))
    # component_version = "missing from {wrap_module_mame} POM".format(wrap_module_mame=wrap_module_mame)
    # for dependency in dependencies:
    #     name = dependency.findtext(ns_tag('artifactId'))
    #     if name == nexus_artifact:
    #         component_version = dependency.findtext(ns_tag('version'))
    #         break
    #         # otherwise we use the version passed in.
    # return component_version


nexus_artifact = sys.argv[1]
file_path = sys.argv[2]

print str(version_from_deploy(nexus_artifact, file_path))
