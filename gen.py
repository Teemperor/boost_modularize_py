#!/usr/bin/python

import os
import subprocess
import sys

class ClassModule:
    def __init__(self, start_header):
        self.headers = [start_header]
    def add(self, header):
        self.headers.append(header)

    def module_def(self):
        header = self.headers[0]
        if len(self.headers) == 1:
            return 'module "' + header + '" { header "' + header + '" export * }\n'
        result = 'module "' + header + '" {\n'

        for h in self.headers:
            result += '  module "' + h + '" { header "' + h + '" export * }\n'
        result += '}\n'
        return result

    def includes(self):
        result = ''

        for h in self.headers:
            result += '#include <' + h + '>\n'
        return result

    def name(self):
        return self.headers[0]

modules = []
ignored_modules = []

for root, dirs, files in os.walk("/usr/include/boost"):
    for file in files:
        path = os.sep.join([root, file])
        inc_path = path[len("/usr/include/"):]
        modules.append(ClassModule(inc_path))


for i in range(0, len(modules)):
    main_file = open("main.cpp", "w")
    modulemap = open("boost.modulemap", "w")

    for j in range(0, i + 1):
        if not j in ignored_modules:
            modulemap.write(modules[j].module_def())

    main_file.write(modules[i].includes())

    sys.stdout.write("[" + str(i) + "/" + str(len(modules)) + "] ")

    main_file.close()
    modulemap.close()
    process = subprocess.Popen("./run.sh " + sys.argv[1],
                shell=True, stdout=subprocess.PIPE)
    output = str(process.communicate())
    output = output.replace("\\\\", "\\")
    output = output.replace("\\n", "\n")
    #output = process.stdout.read()
    errcode = process.returncode
    if errcode == 0:
        print("Accepting " + modules[i].name())
    else:
        ignored_modules.append(i)
        print("Ignoring " + modules[i].name())


