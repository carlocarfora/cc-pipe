import os
import nuke

def onLoad():
    print "launched init.py!"

    fps = os.environ['FPS']
    width = os.environ['WIDTH']
    height = os.environ['HEIGHT']
    project = os.environ['PROJECT']
    task = os.environ['TASK']
    shot = os.environ['SHOT']
    job = os.environ['JOB']

    # Set Job folder in file browser
    nuke.addFavoriteDir(
        name = 'Task Dir',
        directory = job,
        type = nuke.SCRIPT)

    # Set res
    nuke.knobDefault('Root.format', width + ' ' + height + ' HD')

onLoad()
