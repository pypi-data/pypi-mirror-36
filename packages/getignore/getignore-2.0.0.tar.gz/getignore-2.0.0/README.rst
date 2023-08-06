==========
Getignorer
==========

Command line utility to fetch common .gitignore files

Installation
============

Install through PyPi::

    λ pip install getignore

Usage
=====

Enter a variable number of language to create the .gitignore file from::

    λ getignore Python Haskell

Output location can be change with -o (default is .gitignore)::

    λ getignore Python -o sample.txt

Output can be previewed with --preview::

    λ getignore --preview

View all available gitignore templates with --list::

    λ getignore --list

For a full rundown of available options::

    λ getignore --help
