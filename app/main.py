#!/usr/bin/env python3
import pygame, json, os, time, math, random

W,H=1280,720
SAVE="/var/lib/pobar/pet.json"
pygame.init()
try: pygame.mixer.init()
except: pass
screen=pygame.display.set_mode((W,H), pygame.FULLSCREEN)
clock=pygame.time.Clock()
FONT=pygame.font.Font(None,42); SMALL=pygame.font.Font(None,30); BIG=pygame.font.Font(None,66)
BG=(105,178,208); PANEL=(29,34,43); PANEL2=(54,62,76); WHITE=(245,245,245)
BLACK=(20,22,25); CREAM=(247,211,161); BROWN=(150,97,62)
GREEN=(88,194,102); YELLOW=(235,190,68); RED=(220,84,89)

DEFAULT={"name":"Pobár","hunger":80,"hygiene":85,"energy":90,"mood":85,
"health":100,"coins":20,"poop":0,"age_hours":0,"food":3,"toys":1,"stage":0,
"highscore":0,"last":time.time()}

def clamp(x): return max(0,min(100,x))
def load():
    try:
        with open(SAVE,encoding="utf-8") as f:
            p=DEFAULT.copy(); p.update(json.load(f)); return p
    except: return DEFAULT.copy()
pet=load()
elapsed=max(0,time.time()-pet.get("last",time.time()))
h=elapsed/3600
pet["age_hours"]+=h
pet["hunger"]=clamp(pet["hunger"]-h*7); pet["hygiene"]=clamp(pet["hygiene"]-h*4)
pet["energy"]=clamp(pet["energy"]-h*2); pet["mood"]=clamp(pet["mood"]-h*2)
pet["poop"]=min(5,pet["poop"]+int(h/4))
pet["stage"]=0 if pet["age_hours"]<24 else 1 if pet["age_hours"]<72 else 2

def save():
    os.makedirs(os.path.dirname(SAVE),exist_ok=True)
    pet["last"]=time.time()
    tmp=SAVE+".tmp"
    with open(tmp,"w",encoding="utf-8") as f: json.dump(pet,f,ensure_ascii=False,indent=2)
    os.replace(tmp,SAVE)
save()

def t(s,x,y,font=FONT,color=WHITE,center=False):
    q=font.render(s,True,color); r=q.get_rect()
    r.center=(x,y) if center else r.center
    if not center:r.topleft=(x,y)
    screen.blit(q,r)

def bar(label,v,x,y,w=280):
    pygame.draw.rect(screen,(17,20,25),(x,y,w,30),border_radius=10)
    c=GREEN if v>=60 else YELLOW if v>=30 else RED
    pygame.draw.rect(screen,c,(x,y,max(4,int(w*v/100)),30),border_radius=10)
    t(f"{label}: {int(v)}",x+10,y+2,SMALL)

def dog(cx,cy,bob=0,closed=False):
    cy+=bob
    pygame.draw.ellipse(screen,(61,119,143),(cx-130,cy+125,260,30))
    pygame.draw.polygon(screen,BROWN,[(cx-65,cy-100),(cx-145,cy-55),(cx-110,cy+35),(cx-50,cy-15)])
    pygame.draw.polygon(screen,BROWN,[(cx+65,cy-100),(cx+145,cy-55),(cx+110,cy+35),(cx+50,cy-15)])
    pygame.draw.rect(screen,CREAM,(cx-100,cy+15,200,145),border_radius=45)
    pygame.draw.rect(screen,CREAM,(cx-112,cy-120,224,190),border_radius=55)
    pygame.draw.ellipse(screen,(255,225,180),(cx-55,cy-8,110,80))
    if closed:
        pygame.draw.line(screen,BLACK,(cx-62,cy-53),(cx-40,cy-53),6)
        pygame.draw.line(screen,BLACK,(cx+40,cy-53),(cx+62,cy-53),6)
    else:
        pygame.draw.circle(screen,BLACK,(cx-51,cy-52),11); pygame.draw.circle(screen,BLACK,(cx+51,cy-52),11)
    pygame.draw.rect(screen,BLACK,(cx-15,cy+13,30,20),border_radius=6)
    pygame.draw.line(screen,BLACK,(cx,cy+33),(cx-18,cy+45),4)
    pygame.draw.line(screen,BLACK,(cx,cy+33),(cx+18,cy+45),4)
    pygame.draw.rect(screen,CREAM,(cx-78,cy+125,55,35),border_radius=12)
    pygame.draw.rect(screen,CREAM,(cx+23,cy+125,55,35),border_radius=12)

screen_name="home"; message="AHOJ!"; action="idle"; until=0
focus=0; mini_score=0; mini_end=0; target=None; last_save=time.time()

def action_do(k):
    global message,action,until
    if k=="feed":
        if pet["food"]>0:
            pet["food"]-=1; pet["hunger"]=clamp(pet["hunger"]+25); pet["mood"]=clamp(pet["mood"]+5)
            message="MNAM!"; action="eat"
        else: message="DOSLO JIDLO"
    elif k=="wash":
        pet["hygiene"]=clamp(pet["hygiene"]+38); pet["mood"]=clamp(pet["mood"]+5); message="BUBLINKY!"; action="bath"
    elif k=="play":
        if pet["energy"]>=12 and pet["toys"]>0:
            pet["energy"]=clamp(pet["energy"]-12); pet["mood"]=clamp(pet["mood"]+20); message="JUPI!"; action="play"
        else: message="JSEM UNAVENY"
    elif k=="sleep":
        pet["energy"]=clamp(pet["energy"]+40); pet["mood"]=clamp(pet["mood"]+4); message="ZZZ..."; action="sleep"
    elif k=="clean":
        if pet["poop"]:
            pet["poop"]=0; pet["hygiene"]=clamp(pet["hygiene"]+18); pet["coins"]+=2; message="CISTO!"; action="happy"
        else: message="NIC TU NENI"
    until=time.time()+2; save()

def home():
    screen.fill(BG); pygame.draw.rect(screen,PANEL,(20,20,1240,610),border_radius=30)
    t("POBAR OS",45,38,BIG); t(f"Stadium: {['STENE','MLADY PEJSEK','DOSPELAK'][pet['stage']]}",850,55,SMALL)
    t(f"Mince: {pet['coins']}   Jidlo: {pet['food']}   Hracek: {pet['toys']}   Hovinka: {pet['poop']}",45,105,SMALL)
    bar("HLAD",pet["hunger"],45,155); bar("HYGIENA",pet["hygiene"],45,205)
    bar("ENERGIE",pet["energy"],45,255); bar("NALADA",pet["mood"],45,305); bar("ZDRAVI",pet["health"],45,355)
    pygame.draw.rect(screen,WHITE,(850,120,330,75),border_radius=18); t(message,1015,157,FONT,BLACK,True)
    dog(1015,335,math.sin(time.time()*9)*7 if action=="play" else 0,action=="sleep")
    labels=["KRMIT","KOUPAT","HRAT","SPAT","UKLIDIT","MENU"]
    rects=[pygame.Rect(25,650,180,55),pygame.Rect(220,650,180,55),pygame.Rect(415,650,180,55),
           pygame.Rect(610,650,180,55),pygame.Rect(805,650,180,55),pygame.Rect(1000,650,250,55)]
    for i,(lab,r) in enumerate(zip(labels,rects)):
        pygame.draw.rect(screen,PANEL2 if i==focus else (44,51,63),r,border_radius=14); t(lab,r.centerx,r.centery,SMALL,WHITE,True)

def menu():
    screen.fill(BG); pygame.draw.rect(screen,PANEL,(90,50,1100,610),border_radius=30); t("MENU",640,100,BIG,WHITE,True)
    items=["MINIHRA","OBCHOD","STATISTIKY","ZPET","VYPNOUT"]
    for i,l in enumerate(items):
        r=pygame.Rect(250,150+i*85,780,62); pygame.draw.rect(screen,PANEL2 if i==focus else (44,51,63),r,border_radius=14); t(l,640,r.centery,FONT,WHITE,True)

def shop():
    screen.fill(BG); pygame.draw.rect(screen,PANEL,(90,50,1100,610),border_radius=30); t("OBCHOD",640,100,BIG,WHITE,True)
    t(f"Mince: {pet['coins']}",980,95,SMALL)
    items=[("JIDLO +3",5),("HRAJICKA +1",8),("LUXUSNI KOUPEL",10)]
    for i,(l,cost) in enumerate(items):
        r=pygame.Rect(180+i*315,210,275,100); pygame.draw.rect(screen,PANEL2,r,border_radius=15); t(l,318+i*315,245,FONT,WHITE,True); t(f"{cost} minci",318+i*315,285,SMALL,WHITE,True)
    t("Klikni / sipky + Enter. ESC = zpet",640,550,SMALL,WHITE,True)

def stats():
    screen.fill(BG); pygame.draw.rect(screen,PANEL,(90,50,1100,610),border_radius=30); t("STATISTIKY",640,100,BIG,WHITE,True)
    lines=[f"Jmeno: {pet['name']}",f"Vek: {pet['age_hours']/24:.1f} dni",
           f"Stadium: {['Stene','Mlady pejsek','Dospelak'][pet['stage']]}",
           f"Mince: {pet['coins']}",f"Rekord minihry: {pet['highscore']}"]
    for i,l in enumerate(lines): t(l,180,180+i*60,FONT)
    t("ESC = zpet",640,550,SMALL,WHITE,True)

def mini():
    screen.fill(BG); pygame.draw.rect(screen,PANEL,(90,50,1100,610),border_radius=30)
    t("MINIHRA: CHYT SYR",640,100,BIG,WHITE,True)
    left=max(0,int(mini_end-time.time())); t(f"Skore: {mini_score}    Cas: {left}",640,150,FONT,WHITE,True)
    if target: pygame.draw.circle(screen,YELLOW,target,32)
    t("Klikni na zluty syr!   ESC = konec",640,585,SMALL,WHITE,True)

running=True
while running:
    dt=clock.tick(30)/1000; now=time.time()
    pet["hunger"]=clamp(pet["hunger"]-dt/520); pet["hygiene"]=clamp(pet["hygiene"]-dt/900); pet["mood"]=clamp(pet["mood"]-dt/1200)
    if pet["hunger"]<15 or pet["hygiene"]<10: pet["health"]=clamp(pet["health"]-dt/20)
    if now>until: action="idle"; message="AHOJ!"
    for e in pygame.event.get():
        if e.type==pygame.QUIT: running=False
        elif e.type==pygame.KEYDOWN:
            if e.key in (pygame.K_ESCAPE,pygame.K_q):
                if screen_name=="home": running=False
                else: screen_name="home"
            elif screen_name=="home":
                if e.key in (pygame.K_LEFT,pygame.K_a): focus=(focus-1)%6
                elif e.key in (pygame.K_RIGHT,pygame.K_d): focus=(focus+1)%6
                elif e.key in (pygame.K_RETURN,pygame.K_SPACE):
                    ["feed","wash","play","sleep","clean","menu"][focus] == "menu" and None
                    k=["feed","wash","play","sleep","clean","menu"][focus]
                    screen_name="menu" if k=="menu" else action_do(k)
                elif e.key==pygame.K_1: action_do("feed")
                elif e.key==pygame.K_2: action_do("wash")
                elif e.key==pygame.K_3: action_do("play")
                elif e.key==pygame.K_4: action_do("sleep")
                elif e.key==pygame.K_5: action_do("clean")
                elif e.key==pygame.K_m: screen_name="menu"; focus=0
            elif screen_name=="menu":
                if e.key in (pygame.K_UP,pygame.K_w): focus=(focus-1)%5
                elif e.key in (pygame.K_DOWN,pygame.K_s): focus=(focus+1)%5
                elif e.key in (pygame.K_RETURN,pygame.K_SPACE):
                    if focus==0: screen_name="mini"; mini_score=0; mini_end=time.time()+20; target=(random.randint(250,1030),random.randint(210,500))
                    elif focus==1: screen_name="shop"; focus=0
                    elif focus==2: screen_name="stats"
                    elif focus==3: screen_name="home"; focus=0
                    elif focus==4: running=False
        elif e.type==pygame.MOUSEBUTTONDOWN and e.button==1:
            x,y=e.pos
            if screen_name=="home":
                rs=[pygame.Rect(25,650,180,55),pygame.Rect(220,650,180,55),pygame.Rect(415,650,180,55),pygame.Rect(610,650,180,55),pygame.Rect(805,650,180,55),pygame.Rect(1000,650,250,55)]
                for i,r in enumerate(rs):
                    if r.collidepoint(x,y):
                        focus=i; k=["feed","wash","play","sleep","clean","menu"][i]
                        screen_name="menu" if k=="menu" else action_do(k)
            elif screen_name=="menu":
                for i in range(5):
                    r=pygame.Rect(250,150+i*85,780,62)
                    if r.collidepoint(x,y):
                        focus=i
                        if i==0: screen_name="mini";mini_score=0;mini_end=time.time()+20;target=(random.randint(250,1030),random.randint(210,500))
                        elif i==1: screen_name="shop"
                        elif i==2: screen_name="stats"
                        elif i==3: screen_name="home";focus=0
                        elif i==4: running=False
            elif screen_name=="shop":
                for i in range(3):
                    r=pygame.Rect(180+i*315,210,275,100)
                    if r.collidepoint(x,y):
                        if i==0 and pet["coins"]>=5:pet["coins"]-=5;pet["food"]+=3
                        elif i==1 and pet["coins"]>=8:pet["coins"]-=8;pet["toys"]+=1
                        elif i==2 and pet["coins"]>=10:pet["coins"]-=10;pet["hygiene"]=clamp(pet["hygiene"]+55)
                        save()
            elif screen_name=="mini":
                if target and time.time()<mini_end and math.hypot(x-target[0],y-target[1])<55:
                    mini_score+=1; target=(random.randint(250,1030),random.randint(210,500))
                elif time.time()>=mini_end:
                    pet["highscore"]=max(pet["highscore"],mini_score); save(); screen_name="menu"
    if screen_name=="home": home()
    elif screen_name=="menu": menu()
    elif screen_name=="shop": shop()
    elif screen_name=="stats": stats()
    elif screen_name=="mini": mini()
    pygame.display.flip()
    if now-last_save>10: save(); last_save=now
save(); pygame.quit()
