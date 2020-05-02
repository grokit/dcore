# see https://github.com/google/yapf
find . | grep \.py$ | xargs yapf3 --in-place --style='{based_on_style: pep8, indent_width: 4}' 
