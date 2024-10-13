from os import system
from glob import glob
print("Start processing")
for file in sorted(glob("TestCases/B_M*Non*.json")):
    system('echo("--------",'+file.replace("B_","")+')')
    system('python mazeTester2.py "'+file +'"')
    system('python mazeTester2.py "'+file.replace("B_","C_")+'"')

for file in sorted(glob("TestCases/B_M*_Over*.json")):
    system('echo("--------",'+file.replace("B_","")+')')
    system('python mazeTester2.py "'+file +'"')
    system('python mazeTester2.py "'+file.replace("B_","C_")+'"')

for file in sorted(glob("TestCases/B_File0*Non*.json")):
    system('echo("--------",'+file.replace("B_","")+')')
    system('python mazeTester2.py "'+file+'"')
    system('python mazeTester2.py "'+file.replace("B_","C_")+'"')

print("Process completed")