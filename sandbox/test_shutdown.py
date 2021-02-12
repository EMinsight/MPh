﻿"""
Tests if the Java VM shuts down in a timely manner.

The Java Virtual Machine will often "hang" at the end of the Python
session, delaying the termination of the program. If we run this
script with Comsol 5.5 or 5.6 via JPype 1.2.1, the shutdown takes
almost exactly 60 seconds. If we only start the client, but never
load a model (by commenting out the corresponding lines of code),
things are fine, though obviously that is a use case of next to no
practical relevance. In other scenarios, not tested by this script,
where the client actually did something useful in between, such as
evaluating a solution, the shutdown seems to never happen.

The only work-around, at this point, is to forcefully stop the Java
VM at the end of the Python session. This does not necessarily point
to a problem with the Python-to-Java bridge JPype. Oddly, the Comsol
documentation insists on calling `System.exit(0)` at the end of Java
programs too, where such a call should not be necessary.

Edit: This seems to work as of JPype 1.2.2-dev0 if we set configure
the shutdown behavior with `jpype.config.destroy_jvm = False`.

The script does not depend on MPh, but starts the Comsol client
directly via JPype. Paths to the Comsol installation are hard-coded
for a Windows installation of Comsol 5.5. Other versions or install
locations can be tested by editing the assignment to the `root`
variable. On Linux, 'win64' has to be replaced by 'glnxa64', and on
macOS by 'maci64'.
"""

import jpype
import jpype.imports
import jpype.config
from timeit import default_timer as now
from pathlib import Path

print(f'Starting Comsol\'s Java VM via JPype {jpype.__version__}.')
t0 = now()
root = Path(r'C:\Program Files\COMSOL\COMSOL55\Multiphysics')
jvm  = root/'java'/'win64'/'jre'/'bin'/'server'/'jvm.dll'
jpype.config.destroy_jvm = False
jpype.startJVM(str(jvm), classpath=str(root/'plugins'/'*'))
print(f'Java VM started in {now()-t0:.3f} seconds.')

print('Starting stand-alone Comsol client.')
t0 = now()
from com.comsol.model.util import ModelUtil as client
client.initStandalone(False)
client.loadPreferences()
print(f'Client started in {now()-t0:.3f} seconds.')

print('Loading model file.')
t0 = now()
tag = client.uniquetag('model')
model = client.load(tag, '../tests/capacitor.mph')
print(f'Model loaded in {now()-t0:.3f} seconds.')

print('Shutting down Java VM.')
t0 = now()
jpype.shutdownJVM()
print(f'Java VM shut down in {now()-t0:.3f} seconds.')
