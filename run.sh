#!/bin/bash
rm -rf pcms

$1 -fmodules -Rmodule-build \
-fmodules-cache-path=pcms -fsyntax-only \
-ivfsoverlay overlay.yaml   main.cpp 2>&1

