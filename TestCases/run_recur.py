from os import system
from glob import glob
for file in sorted(glob("TestCases/Recur/B_M*10*.json")):
    system('echo(--------Recur: '+file.replace("TestCases\\Recu\\B_",""))
    system('python mazeTester2.py "'+file+'"')
    system('python mazeTester2.py "'+file.replace("B_","G_")+'"')
