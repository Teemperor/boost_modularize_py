#!/usr/bin/python

import os
import subprocess
import sys

class ClassModule:
    def __init__(self, path, header):
        self.header = header
        self.path = path
        self.name_ = self.header.title().replace("/", "")

    def add(self, header):
        self.headers.append(header)

    def module_def(self):
        return 'module "' + self.name() + '" { header "' + self.header + '" export * }\n'

    def includes(self):
        return '#include <' + self.header + '>\n'

    def name(self):
        return self.name_

modules = []
ignored_modules = []

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def has_headerguard(path):
    with open(path) as f:
        try:
            content = f.readlines()
            for i in range(0, len(content) - 1):
                if content[i].startswith("#ifndef "):
                    if content[i + 1].startswith("#define "):
                        return True
        except UnicodeDecodeError as e:
            print("Can't unicode encode " + path + " due to exception " + str(e))
    print("No header guards: " + path)
    return False

for root, dirs, files in os.walk("/usr/include/boost"):
    for file in files:
        path = os.sep.join([root, file])
        if has_headerguard(path):
            inc_path = path[len("/usr/include/"):]
            modules.append(ClassModule(path, inc_path))


for i in range(0, len(modules)):
    modulemap = open("boost.modulemap", "w")
    modulemap.write("module boost {\n")
    for j in range(0, i + 1):
        if not j in ignored_modules:
            modulemap.write("  " + modules[j].module_def())
    modulemap.write("}\n")
    modulemap.close()

    main_file = open("main.cpp", "w")
    main_file.write(modules[i].includes())
    sys.stdout.write("[" + str(i).rjust(6, ' ') + "/" + str(len(modules)) + "] ")
    main_file.close()

    process = subprocess.Popen("./run.sh " + sys.argv[1],
                shell=True, stdout=subprocess.PIPE)
    output = str(process.communicate())
    output = output.replace("\\\\", "\\")
    output = output.replace("\\n", "\n")
    #output = process.stdout.read()
    errcode = process.returncode
    mod_name = modules[i].name().ljust(50, ' ')
    pcm_size = sum( os.path.getsize(os.path.join(dirpath, filename)) for dirpath, dirnames, filenames in os.walk("pcms") for filename in filenames )
    pcm_size_str = " " + sizeof_fmt(pcm_size).rjust(10)
    if errcode == 0:
        print("Accepting " + mod_name + pcm_size_str)
    else:
        ignored_modules.append(i)
        print("Ignoring  " + mod_name)


