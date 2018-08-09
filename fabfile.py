# -*- coding: utf-8 -*-

from fabric.api import *
import os


env.hosts=['35.198.160.181']
env.user='jose-luis'
env.key_filename='/home/jose-luis/.ssh/gotmKeys/jose-luis'
env.roledefs={'stage':['35.198.160.181'],
                'production': [''],
               }
env.disable_known_hosts = False
env.reject_unknown_hosts = False

def whoAmI():
    run('uname -a')
    run ('whoami')

def updateMachine():
    run('sudo apt-get update')

def installUtilities():
    run('yes | sudo apt-get install gcc g++ gfortran cmake make git libnetcdf-dev libnetcdff-dev netcdf-bin xmlstarlet')

def getGOTM():
    run(' '.join('''if [ ! -d ./code ];
                    then
                        git clone https://github.com/gotm-model/code.git &&
                        cd code &&
                        git checkout lake;
                    fi
           '''.replace('\n', ' ').split())
        )

def getGOTMGUI():
    run(' '.join('''if [ ! -d ./gotmgui ];
                    then
                        git clone https://github.com/BoldingBruggeman/gotmgui.git &&
                        sudo cp -r ~/gotmgui/gotmgui  /usr/local/lib/python2.7/dist-packages;
                    fi
           '''.replace('\n', ' ').split())
       )

def getFABM():
    run('rm -rf Keys')
    run('mkdir Keys')
    put('fabmKey','Keys/fabmKey')
    run('sudo chmod 400 Keys/fabmKey ')
    run(' '.join('''if [ ! -d ./fabm-prognos ];
                    then
                        GIT_SSH_COMMAND='ssh -i ./Keys/fabmKey -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no' git clone git@gitlab.au.dk:anbios/fabm-prognos.git;
                    fi
           '''.replace('\n', ' ').split()
                )
       )

def addGOTMToPath():
    run('''echo 'export GOTMDIR=~/code' >> ~/.profile ''')

def compileFABM():
    run('rm -rf fabm-prognos/build')
    run('mkdir -p fabm-prognos/build')
    run('cd fabm-prognos/build && cmake ../src -DFABM_HOST=gotm && make')

def compileGOTM():
    run('rm -rf code/build')
    run('mkdir -p code/build')
    run('cd code/build && cmake ../src -DFABM_BASE=../../fabm-prognos && make')

def installGOTM():
    run('sudo cp code/build/gotm /usr/bin/')

def getLakeSetups():
    run('rm -rf PROGNOS')
    run(' '.join('''if [ ! -d ./PROGNOS ];
                    then
                        GIT_SSH_COMMAND='ssh -i ./Keys/fabmKey -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no' git clone git@gitlab.au.dk:anbios/PROGNOS.git;
                    fi
           '''.replace('\n', ' ').split()
                )
       )


def getPip():
    run('yes | sudo apt-get install python-pip')

def getModules():
    run('sudo pip install xmlstore editscenario xmlplot matplotlib')

def changeScenarioInXML(oldScenario,newScenario,file):
    run('''xmlstarlet ed --inplace -u "scenario[@version='{}']/@version" -v '{}' {}'''.format(oldScenario,newScenario,file))

def setSchemaDir(filename):
    scenarioFile = os.path.split(filename)[0] + '/editscenario.sh'
    run(''' 'sed -i 's_\(--schemadir=.*\s\)_--schemadir="$GOTMDIR"/schemas _g' {}'''.format(scenarioFile))

def editScenario(filename):
    #run("tail ~/.profile")
    #run('echo $GOTMDIR')
    run('''cd "$(dirname {})" && editscenario --schemadir "$GOTMDIR"/schemas -e nml . langtjern.xml'''.format(filename))

def runGOTM(filename):
    run('cd "$(dirname "{}")" && gotm'.format(filename));


@task
def testConnection():
    whoAmI.roles=('stage',)
    execute(whoAmI)

@task
def update():
    updateMachine.roles=('stage',)
    execute(updateMachine)

@task
def getUtilities():
    updateMachine.roles=('stage',)
    installUtilities.roles=('stage',)
    getPip.roles=('stage',)
    getModules.roles=('stage',)
    execute(update)
    execute(installUtilities)
    execute(getPip)
    execute(getModules)

@task
def downloadModels():
    getGOTM.roles=('stage',)
    getFABM.roles=('stage',)
    getGOTMGUI.roles=('stage',)
    addGOTMToPath.roles=('stage',)
    execute(getFABM)
    execute(getGOTM)
    execute(getGOTMGUI)
    execute(addGOTMToPath)

@task
def compileModels():
    compileFABM.roles=('stage',)
    compileGOTM.roles=('stage',)
    installGOTM.roles=('stage',)
    execute(compileFABM)
    execute(compileGOTM)
    execute(installGOTM)

@task
def getPROGNOS():
    getLakeSetups.roles=('stage',)
    execute(getLakeSetups)


@task
def testRun(filename):
    changeScenarioInXML.roles=('stage',)
    setSchemaDir.roles=('stage',)
    editScenario.roles=('stage',)
    runGOTM.roles=('stage',)

    changeScenarioInXML('gotm-5.1','gotm-5.3',filename)
    #setSchemaDir(filename)
    editScenario(filename)
    runGOTM(filename)




