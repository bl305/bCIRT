#!/bin/bash
find . -path "*/__pycache__/*.pyc" -delete
find . "__pycache__" -type d -delete
