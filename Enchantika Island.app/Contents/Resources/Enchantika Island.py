import pygame,random,math,os,codes

pygame.init()

screen = pygame.display.set_mode([1280,960])

pygame.display.set_caption("Enchantika Island")

mixer=pygame.mixer
music=mixer.music
fill=screen.fill
blit=screen.blit
flip=pygame.display.flip
load=pygame.image.load

selectedgamefile = None

pygame.display.set_icon(load('images/mana.png'))

def blitcenter(surf,pos): # Blit pygame.Surface with center anchor
    screen.blit(surf,[pos[0]-surf.get_size()[0]/2,pos[1]-surf.get_size()[1]/2])
    
def distance(x1,y1,x2,y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

def gettilepos(x,y):
    return [x*256+(y*256),-y*128+(x*128)]

def sortobjs(objs):
    new = []

    for i in objs:
        new.append(i.pos[1])

    new.sort()

    final = []

    for i in new:
        for obj in objs:
            if obj.pos[1] == i:
                final.append(obj)
    return final


class Button:
    def __init__(self,surf,pos,center=False):
        self.surf = surf
        
        if center:
            pos = [pos[0]-surf.get_size()[0]/2,pos[1]-surf.get_size()[1]/2]

        self.pos = pos
            
    def hover(self):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        sizex = self.surf.get_size()[0]
        sizey = self.surf.get_size()[1]
        if x>=self.pos[0] and x<=self.pos[0]+sizex:
            if y>=self.pos[1] and y<=self.pos[1]+sizey:
                return True
    def render(self):
        blit(self.surf,self.pos)

class Area:
    def __init__(self,tile,xsize,ysize,objs,items,monsters):
        self.tile = tile
        self.xsize = xsize
        self.ysize = ysize
        self.trees = objs
        self.items = items
        self.monsters = monsters
    def rendertiles(self,offset):
        for x in range(0,self.xsize):
            for y in range(0,self.ysize):
                pos = [x*600+offset[0],y*300+offset[1]]

                blit(self.tile,pos)

class Creature:
    def __init__(self,name,img,pos,direction):
        self.name = name
        self.img = img
        self.pos = pos
        self.direction = direction
        self.alive = True
    def render(self):
        if not self.alive:
            blit(pygame.transform.rotate(self.img,90),self.pos)
        else:
            blit(self.img,self.pos)

class Sprite:
    def __init__(self,name,img,pos):
        self.name = name
        self.img = img
        self.pos = pos
    def render(self):
        blit(self.img,self.pos)
            
        
def text(**kwargs):
    if not 'text' in kwargs:
        kwargs['text'] = ''
    if not 'color' in kwargs:
        kwargs['color'] = [0,0,0]
    if not 'size' in kwargs:
        kwargs['size'] = 50
    if not 'font' in kwargs:
        kwargs['font'] = 'font.ttf'
        
        
    font = pygame.font.Font(kwargs['font'],kwargs['size'])

    txt = font.render(kwargs['text'],1,kwargs['color'])

    return txt

def msg(message):
    okbutton = Button(text(text='OK',color=[200,0,0],size=64),[601,640])
    txt = text(text=message,color=[200,0,0])

    run = True
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                save_cfg()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if okbutton.hover():
                    run = False

        fill([0,0,128])
        okbutton.render()
        blitcenter(txt,[640,320])
        flip()

def titlescreen():
    music.load('music/Title.wav')
    music.set_volume(1)
    music.play(-1)
    mana = load('images/mana.png')
    health = load('images/health.png')
    monster = load('images/monster.png')
    monster = load('images/monster.png')
    title = text(text='Enchantika Island',size=128,color=[200,0,0])
    bgtitle = Area(load('images/grass.jpg'),6,6,[],[],[])
    start = Button(text(text='Start',size=64),[640,640],True)
    x = 0

    potions = []
    monsterpos = [random.randint(640,2432),random.randint(0,624)]

    for i in range(0,4):
        potions.append([random.randint(640,2432),random.randint(0,624),random.choice([mana,health])])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.hover():
                    savefileselect()
        fill([0,0,0])

        bgtitle.rendertiles([x,0])

        for i in potions:
            blit(i[2],[i[0]+x,i[1]])

        blit(monster,[monsterpos[0]+x,monsterpos[1]])

        blitcenter(title,[640,240])
        start.render()
        flip()
        x-=2

        if x == -1792:
            x = 0

def savefileselect():
    global selectedgamefile
    title = text(text='Save File Select',size=72,color=[200,0,0])
    new = Button(text(text='New Game',size=64,color=[200,0,0]),[128,880],True)
    delete = Button(text(text='Delete Game',size=64,color=[200,0,0]),[640,880],True)
    play = Button(text(text='Play Game',size=64,color=[200,0,0]),[1152,880],True)
    selected = None
    saves = os.listdir('saves')

    if '.DS_Store' in saves:
        saves.remove('.DS_Store')
    y = 320
    for i in saves:
        saves[saves.index(i)] = [Button(text(text=i.split('.')[0],color=[0,200,0],size=64),[128,y]),i]
        y+=96
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new.hover():
                    createsavefile()
                for save in saves:
                    if save[0].hover():
                        selected = save
                if delete.hover() and not selected == None:
                    os.remove('saves/'+selected[1])
                    msg('Save file deleted.')
                    savefileselect()
                if play.hover() and not selected == None:
                    selectedgamefile = selected[1]
                    main()
        
        fill([0,0,128])
        blitcenter(title,[640,160])
        
        for save in saves:
            save[0].render()

        if not selected == None:
            pygame.draw.line(screen,[200,0,0],[selected[0].pos[0],selected[0].pos[1]+selected[0].surf.get_size()[1]],[selected[0].pos[0]+selected[0].surf.get_size()[0],selected[0].pos[1]+selected[0].surf.get_size()[1]],2)

        pygame.draw.rect(screen,[0,0,255],[0,800,1280,160])
        new.render()
        delete.render()
        play.render()
        
        flip()

def createsavefile():
    saves = os.listdir('saves')

    if '.DS_Store' in saves:
        saves.remove('.DS_Store')
    title = text(text='Create Save File',size=72,color=[200,0,0])
    prompt = text(text='Please type your name',color=[200,0,0])
    ok = Button(text(text='OK',color=[200,0,0],size=64),[1120,800],True)
    cancel = Button(text(text='Cancel',color=[200,0,0],size=64),[160,800],True)

    name = ''
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if not event.key == pygame.K_BACKSPACE:
                    try:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            name+=chr(event.key).upper()
                        else:
                            name+=chr(event.key)
                    except:
                        pass
                else:
                    name = name[:len(name)-1]
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ok.hover():
                    if len(saves)<4:
                        if not name+'.txt' in saves:
                            if not name == '':
                                fl = open('saves/'+name+'.txt','w+')
                                fl.write(codes.encrypt('level=1\ngold=0\nmana=100\nhealth=100\nscore=0'))
                                fl.close()
                                savefileselect()
                        else:
                            msg("Name taken. Please choose a different name.")
                    else:
                        msg("Maximum number of save files is 4")
                if cancel.hover():
                    savefileselect()
        fill([0,0,128])
        blitcenter(title,[640,160])
        blitcenter(prompt,[640,320])
        blitcenter(text(text=name+'_',color=[0,200,0]),[640,480])
        ok.render()
        cancel.render()
        flip()

def loadsavefile(fl):
    new = []
    for i in fl.readlines():
        try:
            new.append(int(codes.decrypt(i.strip('\n')).split('=')[1]))
        except ValueError:
            new.append(codes.decrypt(i.strip('\n')).split('=')[1])
    return new

def main():
    fl = open('saves/'+selectedgamefile)

    music.stop()
    music.load('sounds/bg.ogg')
    music.set_volume(0.05)
    music.play(-1)

    lines = loadsavefile(fl)
    fl.close()
    
    levelnum = lines[0]
    gold = lines[1]
    mana = lines[2]
    health = lines[3]
    score = lines[4]

    tile = load('images/grass.jpg')
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        for x in range(0,10):
            for y in range(0,10):
                blit(tile,[x*600,y*300])
        flip()

        
        
titlescreen()



