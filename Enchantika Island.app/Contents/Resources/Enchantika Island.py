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
def getangle(x1,y1,x2,y2):
    a = x2-x1
    b = y2-y1

    h = math.sqrt(a**2+b**2)

    theta = math.asin(b/float(h))

    return math.degrees(theta)

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
        self.angry = False
        self.life = 100
    def render(self,offset=[0,0]):
        image = self.img

        if self.direction == 'right':
            image = pygame.transform.flip(image,True,False)
        if not self.alive:
            blit(pygame.transform.rotate(image,90),[self.pos[0]-offset[0],self.pos[1]-offset[1]])
        else:
            blit(image,[self.pos[0]-offset[0],self.pos[1]-offset[1]])

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
                                fl.write(codes.encrypt('level=1\nmana=100\nhealth=100\nscore=0'))
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
    mana = lines[1]
    health = lines[2]
    score = lines[3]

    cam = [0,0]
    pos = [640,480]
    direction = 'left'

    monster = load('images/monster.png')

    plants = []
    monsters = []
    potions = []

    for i in range(0,50):
        plants.append([random.randint(0,6000),random.randint(0,3000)])

    for i in range(0,levelnum*10):
        monsters.append(Creature('monster',monster,[random.randint(0,6000),random.randint(0,3000)],'left'))

    for i in range(0,10):
        potions.append([random.randint(0,6000),random.randint(0,3000),random.choice(['mana','health'])])
    tile = load('images/grass.jpg')
    player = load('images/wizard.png')
    plant = load('images/plant.png')

    manabottle = load('images/mana.png')
    healthbottle = load('images/health.png')
    

    redcrystal = load('images/crystalred.png')
    greencrystal = load('images/crystalgreen.png')
    bluecrystal = load('images/crystalblue.png')

    portal1 = load('images/portal1.png')
    portal2 = load('images/portal2.png')

    fireball = load('images/fireball.png')

    red = [random.randint(0,6000),random.randint(0,3000)]
    green = [random.randint(0,6000),random.randint(0,3000)]
    blue = [random.randint(0,6000),random.randint(0,3000)]

    fireballs = []

    activated = False

    pygame.key.set_repeat(1,1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fl = open('saves/'+selectedgamefile,'w+')

                fl.write(codes.encrypt('level='+str(levelnum)+'\nmana='+str(mana)+'\nhealth='+str(int(health))+'\nscore='+str(score)))

                fl.close()
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                    if pos[0]-16 >= 0:
                        pos[0] -= 16
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                    if pos[0]+16 <= 6000:
                        pos[0] += 16
                elif event.key == pygame.K_UP:
                    if pos[1]-16 >= 0:
                        pos[1] -= 16
                elif event.key == pygame.K_DOWN:
                    if pos[1]+16 <= 3000:
                        pos[1] += 16
            if event.type == pygame.MOUSEBUTTONDOWN:
                mpos = pygame.mouse.get_pos()
                for m in monsters:
                    if distance(m.pos[0],m.pos[1],pos[0],pos[1])<=128:
                        if pygame.mouse.get_pressed()[0]:
                            m.life-=10

                            if m.life <= 0:
                                m.alive = False
                if pygame.mouse.get_pressed()[2]:
                    if mana-10 >= 0:
                        fireballs.append([pos[0],pos[1],mpos[0]+cam[0],mpos[1]+cam[1]])
                        mana-=10
                
                                    

        for x in range(0,11):
            for y in range(0,11):
                blit(tile,[x*600-cam[0],y*300-cam[1]])

        if activated:
            blit(portal2,[3000-cam[0],1500-cam[1]])
        else:
            blit(portal1,[3000-cam[0],1500-cam[1]])
        try:
            blit(redcrystal,[red[0]-cam[0],red[1]-cam[1]])
        except:
            pass
        try:
            blit(greencrystal,[green[0]-cam[0],green[1]-cam[1]])
        except:
            pass
        try:
            blit(bluecrystal,[blue[0]-cam[0],blue[1]-cam[1]])
        except:
            pass

        for p in potions:
            if p[2] == 'mana':
                blit(manabottle,[p[0]-cam[0],p[1]-cam[1]])
            else:
                blit(healthbottle,[p[0]-cam[0],p[1]-cam[1]])

            if distance(p[0],p[1],pos[0],pos[1]) <= 128:
                if p[2] == 'health':
                    health+=10

                    if health > 100:
                        health = 100
                else:
                    mana+=10

                    if mana > 100:
                        mana = 100

                potions.remove(p)

        for p in plants:
            blit(plant,[p[0]-cam[0],p[1]-cam[1]])
        for m in monsters:
            if not m.alive:
                m.render(cam)
                continue
            if m.pos[0]<pos[0]:
                m.direction = 'right'
            else:
                m.direction = 'left'

            if distance(m.pos[0],m.pos[1],pos[0],pos[1]) <= 512 or m.angry:
                m.angry = True
                theta = getangle(m.pos[0],m.pos[1],pos[0],pos[1])
                if distance(m.pos[0],m.pos[1],pos[0],pos[1]) >= 16:
                    if m.pos[0] < pos[0]:
                        m.pos = [math.cos(math.radians(theta))*18+m.pos[0],math.sin(math.radians(theta))*18+m.pos[1]]
                    else:
                        m.pos = [-math.cos(math.radians(theta))*18+m.pos[0],math.sin(math.radians(theta))*18+m.pos[1]]
                else:
                    health-=0.8

                    if health <= 0:
                        msg("You Died!")
                        levelnum-=2

                        if levelnum < 1:
                            levelnum = 1

                        health = 100
                        mana = 100
                        fl = open('saves/'+selectedgamefile,'w+')

                        fl.write(codes.encrypt('level='+str(levelnum)+'\nmana='+str(mana)+'\nhealth='+str(int(health))+'\nscore='+str(score)))

                        fl.close()

                        main()

            m.render(cam)

        if direction == 'right':
            blitcenter(pygame.transform.flip(player,True,False),[pos[0]-cam[0],pos[1]-cam[1]])
        else:
            blitcenter(player,[pos[0]-cam[0],pos[1]-cam[1]])

        if pos[0]-cam[0] >= 1120 and cam[0] < 4720:
            cam[0] += 16
        if pos[1]-cam[1] >= 800 and cam[1] < 2040:
            cam[1] += 16
        if pos[0]-cam[0] <= 160 and cam[0] > 0:
            cam[0] -= 16
        if pos[1]-cam[1] <= 160 and cam[1] > 0:
            cam[1] -= 16

        for f in fireballs:
            blitcenter(fireball,[int(f[0])-cam[0],int(f[1])-cam[1]])

            theta = getangle(f[0],f[1],f[2],f[3])

            if f[0] < f[2]:
                f[0] = math.cos(math.radians(theta))*20+f[0]
                f[1] = math.sin(math.radians(theta))*20+f[1]
            else:
                f[0] = -math.cos(math.radians(theta))*20+f[0]
                f[1] = math.sin(math.radians(theta))*20+f[1]


            for m in monsters:
                if distance(f[0],f[1],m.pos[0],m.pos[1]) <= 128 and m.alive:
                    m.life -= 50
                    
                    if m.life <= 0:
                        m.alive = False
                        score += 1

                    fireballs.remove(f)
            
            x = abs(f[0]-f[2])
            y = abs(f[1]-f[3])

            if f[0] < f[2]:
                f[2]+=x
            if f[1] < f[3]:
                f[3]+=y
            
            if f[0] > f[2]:
                f[2]-=x
            if f[1] > f[3]:
                f[3]-=y

            if f[0] < 0 or f[0] > 6000:
                fireballs.remove(f)
            if f[1] < 0 or f[1] > 3000:
                fireballs.remove(f)

        pygame.draw.rect(screen,[0,0,0],[64,64,256,32])
        pygame.draw.rect(screen,[255,0,0],[64,64,int(health/100.0*256),32])

        pygame.draw.rect(screen,[0,0,0],[512,64,256,32])
        pygame.draw.rect(screen,[0,0,255],[512,64,int(mana/100.0*256),32])

        blit(text(text='Score: '+str(score)),[960,64])

        blit(text(text='Level '+str(levelnum),size=72),[960,800])

        flip()

        if random.randint(0,50) == 1:
            potions.append([random.randint(0,6000),random.randint(0,3000),random.choice(['mana','health'])])

        if not red == True:
            if distance(pos[0],pos[1],red[0],red[1]) <= 128:
                red = True
        if not green == True:
            if distance(pos[0],pos[1],green[0],green[1]) <= 128:
                green = True
        if not blue == True:
            if distance(pos[0],pos[1],blue[0],blue[1]) <= 128:
                blue = True

        if red == True and green == True and blue == True:
            activated = True

        if distance(pos[0],pos[1],3000,1500) <= 256 and activated:
            levelnum+=1

            msg('Level Complete')
            fl = open('saves/'+selectedgamefile,'w+')

            fl.write(codes.encrypt('level='+str(levelnum)+'\nmana='+str(mana)+'\nhealth='+str(int(health))+'\nscore='+str(score)))

            fl.close()

            main()
            
titlescreen()



