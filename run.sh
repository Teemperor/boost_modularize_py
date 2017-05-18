#!/bin/bash
rm -rf pcms

$1 -fmodules -Xclang -fmodules-local-submodule-visibility \
-fmodules-cache-path=pcms -fsyntax-only \
-ivfsoverlay overlay.yaml   main.cpp 2>&1

