print('This is experimental!!!')
import pip
pkgs = ['zipfile', 'os','html','shutil','csv','datetime','requests']
for package in pkgs:
    try:
        import package
    except ImportError as e:
        pip.main(['install', package])


import IliasAdapter, MaAdapter

IliasAdapter.getStudentsOverView()
MaAdapter.getStudentsOverView()
