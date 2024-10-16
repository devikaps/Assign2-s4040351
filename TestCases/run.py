from os import system
from glob import glob
for file in sorted(glob("TestCases/B_M*Non*.json")):
    system('echo(--------Kruskal_Dijksta: '+file.replace("TestCases\\B_",""))
    system('python mazeTester2.py "'+file +'"')
    system('python mazeTester2.py "'+file.replace("B_","G_")+'"')

for file in sorted(glob("TestCases/B_M*_Over*.json")):
    system('echo(--------Kruskal_Dijksta: '+file.replace("TestCases\\B_",""))
    system('python mazeTester2.py "'+file +'"')
    system('python mazeTester2.py "'+file.replace("B_","G_")+'"')

for file in sorted(glob("TestCases/B_File*Non*.json")):
    system('echo(--------Kruskal_Dijksta: '+file.replace("TestCases\\B_",""))
    system('python mazeTester2.py "'+file+'"')
    system('python mazeTester2.py "'+file.replace("B_","G_")+'"')

# Recur
for file in sorted(glob("TestCases/Recur/B_M*.json")):
    system('echo(--------Recur: '+file.replace("TestCases\\Recu\\B_",""))
    system('python mazeTester2.py "'+file+'"')
    system('python mazeTester2.py "'+file.replace("B_","G_")+'"')
for file in sorted(glob("TestCases/Recur/B_File*.json")):
    system('echo(--------Recur: '+file.replace("TestCases\\Recu\\B_",""))
    system('python mazeTester2.py "'+file+'"')
    system('python mazeTester2.py "'+file.replace("B_","G_")+'"')