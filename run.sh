#!/bin/bash
rm -rf pcms

~/CERN/clang-rel/bin/clang++ -fmodules -Rmodule-build \
-fmodules-cache-path=pcms -fsyntax-only \
-ivfsoverlay overlay.yaml   main.cpp

