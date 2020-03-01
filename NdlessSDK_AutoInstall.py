import subprocess
import time
import os
from sys import version
from getpass import getuser

def exect(command):
    res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return res.stdout.read()

def countdown(msg, start):
    print(msg)
    for i in range(start, 0, -1):
        print(i)
        time.sleep(1)

art = '                           *     .--.\n' \
      '                                / /  `\n' \
      '               +               | |\n' \
      '                      \'         \ \__,\n' \
      '                  *          +   \'--\'  *\n' \
      '                      +   /\\\n' \
      '         +              .\'  \'.   *\n' \
      '                *      /======\      +\n' \
      '                      ;:.  _   ;\n' \
      '                      |:. (_)  |\n' \
      '                      |:.  _   |\n' \
      '            +         |:. (_)  |          *\n' \
      '                      ;:.      ;\n' \
      '                    .\' \:.    / `.\n' \
      '                   / .-\'\':._.\'`-. \\\n' \
      '                   |/    /||\    \|\n' \
      '             jgs _..--\"\"\"````\"\"\"--.._\n' \
      '           _.-\'``                    ``\'-._\n' \
      '         -\'                                \'-\n' \
      '          Ndless 4.5 SDK Automated Installer\n' \
      '                 by trueToastedCode\n'

# check executed python version, python < 3 causes errors for me!
if int(version[0]) < 3:
    print('Please run this script with python3, maybe a higher version also works!')
    exit(1)
if getuser() != 'root':
    print('This script must run as root!')
    exit(1)

# print art and start
print(art)
if input('Start installation (n/y): ') != 'y':
    exit(0)

# check current path
print('# check path')
path = os.path.abspath(os.getcwd())
print('path=' + path)
if ' ' in path:
    print('\nYour path contains blank characters, this would cause problems with the ndless installation script! Please start the installation in a path without!')
    exit('1')
else:
    print('ok.')

# check dependencies
dependencies = ['g++', 'git', 'libbinutils', 'libgmp-dev', 'libmpfr-dev', 'libmpc-dev', 'zlib1g-dev', 'libboost-program-options-dev', 'wget', 'python-dev', 'python2.7', 'texinfo', 'gcc-arm-none-eabi', 'php-dev']
print('\n# installing dependencies')
i=1
for pkg in dependencies:
    if 'install ok' in str(exect('dpkg -s ' + pkg)):
        print('[{}/{}] {} already installed!'.format(i, len(dependencies), pkg))
    else:
        print('[{}/{}] Installing {}'.format(i, len(dependencies), pkg))
        os.system('sudo apt -y install ' + pkg)
    i+=1

# get login user
print('\n# get login user')
usr = os.getlogin()
print('user=' + usr)

# download ndless
print('\n# download ndless')
os.system('sudo runuser ' + usr + ' -c \'cd ' + path + ' && git clone --recursive https://github.com/ndless-nspire/Ndless.git\'')

# build toolchain
countdown('\n# build toolchain\n! This process can take minutes to hours depending on your connection and power\nStart in..', 5)
os.system('sudo runuser ' + usr + ' -c \'cd ' + path + '/Ndless/ndless-sdk/toolchain && ./build_toolchain.sh\'')

# verify build
print('\n# verify  build')
os.system('sudo apt update')

cm = 'echo $?'
res = str(exect(cm))

if res == 'b\'0\\n\'':
    print('\n' + cm + '=0\nok.')
else:
    print('\n' + cm + '!=0')
    if(input('Error, output of \'' + cm + '\' should be \'0\'! However you can still test it yourself while keeping this running. If this is a bug, enter y!\nContinue (n/y): ') != 'y'):
        exit(1)

# add path environment variable
print('\n# add path environment variable')
pathVar = 'export PATH="' + path + '/Ndless/ndless-sdk/toolchain/install/bin:' + path + '/Ndless/ndless-sdk/bin:${PATH}"'
print('path_environment_variable=' + pathVar)
with open('/home/' + usr + '/.bashrc', 'a') as file:
    file.write('\n# ndless sdk\n' + pathVar)
    file.close()

# build ndless and sdk
pathCommand = 'sudo runuser ' + usr + ' -c \'' + pathVar[7:] + ' && '
countdown('\n# build ndless and sdk\n! This process can take minutes to hours depending on your connection and power\nStart in..', 5)
os.system(pathCommand + 'cd Ndless && make\'')

print('\n#####################################\nThe automated installer has finished!\nTo verify the installation the code runs "nspire-gcc". If everything has been setup correctly the output should look similiar to:'
      '\n\narm-none-eabi-gcc: fatal error: no input files\ncompilation terminated.\n#####################################\n\nnspire-gcc')
os.system(pathCommand + ' nspire-gcc\'')
print('\n! Read above !')