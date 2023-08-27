import os, shutil
import json

conf = {}
with open('config.json', 'r') as f:
    conf = json.loads(f.read())
tmp_path = conf['temp']
web_path = conf['web']
cap_path = ""
c2_path = ""
print('detecting construct 2 previews...')
def detect(start=False):
    global cap_path
    global c2_path
    os.chdir(tmp_path)
    files = filter(os.path.isdir, os.listdir(tmp_path))
    files = [os.path.join(tmp_path, f) for f in files] # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    files.reverse()
    pr = False
    for i in files:
        if i.find('cap') != -1:
            if cap_path != i + '/' and start == False:
                pr = True
            cap_path = i + '/'
            break
    for i in files:
        if i.find('c2') != -1:
            if c2_path != i + '/' and start == False:
                pr = True
            c2_path = i + '/html5/'
            break
    if pr == True or start == True:
        print('detected directories:\n| - Caproj: ' + cap_path + '\n| - HTML: ' + c2_path)
detect(True)
def pre():
    global web_path
    input('Press ENTER to preview...')
    detect(False)
    folder = web_path
    print('clearing web folder...')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    #shutil.copy(src, dst)
    print('copying files from html...')
    for file in os.listdir(c2_path):
        #print(file)
        shutil.copy(c2_path + file, web_path)
    print('patiently cutting sprites...')
    for sprite in os.listdir(cap_path + 'Animations/'):
        for anim in os.listdir(cap_path + 'Animations/' + sprite + '/'):
            for frame in os.listdir(cap_path + 'Animations/' + sprite + '/' + anim + '/'):
                #print(web_path + frame)
                shutil.copy(cap_path + 'Animations/' + sprite + '/' + anim + '/' + frame, web_path)
                os.rename(web_path + frame, web_path + f"{sprite.lower()}-{anim.lower()}-{frame.lower()}")
    print('patiently cutting textures...')
    for texture in os.listdir(cap_path + 'Textures/'):
        shutil.copy(cap_path + 'Textures/' + texture, web_path)
        os.rename(web_path + texture, web_path + texture.lower())
    pre()

    
pre()
