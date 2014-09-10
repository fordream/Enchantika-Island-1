import pygame

pygame.init()

screen = pygame.display.set_mode([1280,960])

pygame.display.set_caption("Enchantika Island")

mixer=pygame.mixer
music=mixer.music
fill=screen.fill
blit=screen.blit
flip=pygame.display.flip
load=pygame.image.load

pygame.display.set_icon(load('images/mana.png'))

music.set_volume(0.5)

def blitcenter(surf,pos): # Blit pygame.Surface with center anchor
    screen.blit(surf,[pos[0]-surf.get_size()[0]/2,pos[1]-surf.get_size()[1]/2])
    
def distance(x1,y1,x2,y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

def getnew(img,z):
    size = list(img.get_size())
    
    for i in range(0,1281):
        size[0]+=1
        size[1]+=1
    return pygame.transform.scale(img,[size[0]-z,size[1]-z])

class Button:
    def __init__(self,surf,pos):
        self.surf = surf
        self.pos = pos
    def hover(self):
        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        sizex = self.surf.get_size()[0]
        sizey = self.surf.get_size()[1]
        if x>=self.pos[0] and x<=self.pos[0]+sizex:
            if y>=self.pos[1] and y<=self.pos[1]+sizey:
                return True
    def render(self,window):
        window.blit(self.surf,self.pos)
    def rendercenter(self,window):
        blitcenter(self.surf,self.pos)

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

    txt = font.render(kwargs['text'],0,kwargs['color'])

    return txt

def msg(message):
    okbutton = Button(load('ok.png'),[601,640])
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
                    click.play()
                    run = False

        fill([0,0,0])
        okbutton.render(screen)
        blitcenter(txt,[640,320])
        flip()

def titlescreen():
    music.load('music/Title.ogg')
    music.play(-1)
    bg = load('images/bg.jpg')
    title = text(text='Enchantika Island',size=128,color=[200,0,0])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        blit(bg,[0,0])
        blitcenter(title,[640,240])
        flip()

titlescreen()



