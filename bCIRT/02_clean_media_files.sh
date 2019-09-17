#!/bin/bash
find ./media/ -not -name *.png -type f -delete
#find ./log/ -type f -delete
> ./log/logs.txt
> ./log/debug.txt
find ./media/uploads/evidences/ -type f -delete
