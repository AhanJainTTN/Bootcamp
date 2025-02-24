import sys

print(sys.path)

# ahan@Ahans-MacBook-Air Bootcamp % /usr/bin/python3 /Users/ahan/Documents/GitHub/Bootcamp/temp.py
# ['/Users/ahan/Documents/GitHub/Bootcamp', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python39.zip', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/lib-dynload', '/Users/ahan/Library/Python/3.9/lib/python/site-packages', '/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/site-packages']

# ahan@Ahans-MacBook-Air Bootcamp % /usr/local/bin/python3 /Users/ahan/Documents/GitHub/Bootcamp/temp.py
# ['/Users/ahan/Documents/GitHub/Bootcamp', '/Library/Frameworks/Python.framework/Versions/3.10/lib/python310.zip', '/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10', '/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/lib-dynload', '/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/site-packages']

# ahan@Ahans-MacBook-Air Bootcamp % /usr/local/bin/python3.12 /Users/ahan/Documents/GitHub/Bootcamp/temp.py
# ['/Users/ahan/Documents/GitHub/Bootcamp', '/Library/Frameworks/Python.framework/Versions/3.12/lib/python312.zip', '/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12', '/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/lib-dynload', '/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages']

# List pip packages
# /usr/bin/python3 -m pip list
# /usr/local/bin/python3.12 -m pip list
# /usr/local/bin/python3.10 -m pip list

# Uninstall all pip packages
# pip freeze | xargs pip uninstall -y

# nano ~/.bashrc
# nano ~/.bash_profile
# nano ~/.zshrc
# nano ~/.zprofile

# ahan@Ahans-MacBook-Air Desktop % cat ~/.bashrc
# alias python="python3"
# ahan@Ahans-MacBook-Air Desktop % cat ~/.bash_profile

# ahan@Ahans-MacBook-Air Desktop % cat ~/.zshrc
# alias python="python3"
# ahan@Ahans-MacBook-Air Desktop % cat ~/.zprofile

# eval "$(/opt/homebrew/bin/brew shellenv)"

# # Setting PATH for Python 3.12
# # The original version is saved in .zprofile.pysave
# PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin:${PATH}"
# export PATH

# # Setting PATH for Python 3.10
# # The original version is saved in .zprofile.pysave
# PATH="/Library/Frameworks/Python.framework/Versions/3.10/bin:${PATH}"
# export PATH
# ahan@Ahans-MacBook-Air Desktop %
