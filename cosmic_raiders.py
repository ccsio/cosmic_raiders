from kandinsky import *
from ion import keydown,KEY_RIGHT,KEY_LEFT,KEY_EXE, KEY_OK, KEY_ANS
from time import * 
from random import randrange 
black = color(0,0,0) 
white = color(248, 252, 248)
gray = color(56,60,56)
red = color(248,0,0)
blue = color(30,10,211)
green = color(30, 132, 73)
lime = color(24,209,18)
navy_blue = color(31,97,141)

action_list, moving_list, bullet_list, enemy_list = [], [], [], []
move_delay, fps_limit, action_delay = monotonic(), monotonic(), monotonic()

basic = ("basic",None,None) 
tank = ("tank",None,None)
shooterR = ("shooter",("r",115,5),None)
shooter5 = ("shooter",("f",5,5),None)
shooter3 = ("shooter",("f",3,5),None)
ram1 = ("ram",("r",200),("y",180,12,True,1))
ram2 = ("ram",("r",200),("y",144,12,True,1))
shield = ("shield",(200,5,3),None)

level = 0
levels = ( 
        (  ((("dead",)*8)), ("dead",basic,basic,"dead","dead",basic,basic,"dead")),
        (  (basic,basic,"dead","dead","dead","dead",basic,basic), (basic,"dead",basic,basic,basic,basic,"dead",basic)),
        (  ("dead",basic,basic,"dead","dead",basic,basic,"dead"), (basic,"dead","dead",shooterR,shooterR,"dead","dead",basic)),
        (  (shooterR,basic,basic,"dead","dead",basic,basic,shooterR), ("dead","dead",basic,shooterR,shooterR,basic,"dead","dead")),
        (  (shooter5,basic,basic,shooterR,shooterR,basic,basic,shooter5), (basic,"dead","dead",basic,basic,"dead","dead",basic)),
        (  (shooter3,shooterR,"dead","dead","dead","dead",shooterR,shooter3), (basic,basic,basic,shooterR,shooterR,basic,basic,basic)),
        (  (shooter5,"dead",basic,"dead","dead",basic,"dead",shooter5), (basic,basic,"dead",tank,tank,"dead",basic,basic)),
        (  (shooter5,basic,"dead",basic,basic,"dead",basic,shooter5), (tank,"dead",tank,shooterR,shooterR,tank,"dead",tank)),
        (  (shooter3,basic,"dead",shooter5,shooter5,"dead",basic,shooter3), (tank,"dead",basic,tank,tank,basic,"dead",tank)),
        (  (("shooter",("f",3,5),("x",84,4,True,1)),"dead","dead",shooter3,shooter3,"dead","dead",("shooter",("f",3,5),("x",84,-4,True,1))), (basic,basic,basic,tank,tank,basic,basic,basic)),\
        
        (  (("basic",None,("y",36,3,True,1)), ("shooter",("r",100,8),("x",42,3,True,1)), "dead",shooter3,shooter3,"dead",("shooter",("r",100,8),("x",42,-3,True,1)),("basic",None,("y",36,3,True,1))), ("dead","dead",tank,basic,basic,tank,"dead","dead")),
        (  (ram1,basic,basic,shooter3,shooter3,basic,basic,ram1), ("dead",basic,"dead",tank,tank,"dead",basic,"dead")),
        (  ("dead",shooter5,shooterR,basic,basic,shooterR,shooter5,"dead"), (ram2,tank,basic,ram2,ram2,basic,tank,ram2)),
        (  (ram1,shooter3,"dead",shooterR,shooterR,"dead",shooter3,ram1), ("dead",tank,ram2,tank,"dead",ram2,tank,"dead")),
        (  (ram1,basic,shooterR,shooterR,shooterR,shooterR,basic,ram1), ("dead",ram2,tank,basic,basic,tank,ram2,"dead")),
        (  (shooter5,shield,shooter3,basic,basic,shooter3,shield,shooter5), (tank,basic,tank,"dead","dead",tank,basic,tank)),
        (  (shield,shooter5,basic,ram1,ram1,basic,shooter5,shield), ((("shooter",("f",3,5),("x",84,4,True,1))),"dead","dead","dead","dead","dead","dead",(("shooter",("f",3,5),("x",84,-4,True,1))))),
        (  (basic,shield,shooter3,shield,shooterR,shooter3,shield,basic), (ram2,tank,shooter5,tank,ram2,shooter5,tank,ram2)),
        (  (shield,shooter3,("shooter",("r",100,10),None),"dead",shield,("shooter",("r",100,10),None),shooter3,shield), (ram2,tank,tank,ram2,ram2,tank,tank,ram2)),
        (  (shooterR,("shooter",("f",2,8),None),("shield",(180,4,4),None),("ram",("r",150),("y",180,18,True,1)),("ram",("r",150),("y",180,18,True,1)),("shield",(180,4,4),None),("shooter",("f",2,8),None),shooterR), (basic,tank,shooter5,"dead","dead",shooter5,tank,basic)),
)


def enemy_textures(x,y,col,bg=white):
    fill_rect(x+2,y,4,2,black)
    fill_rect(x+28,y,4,2,black)
    fill_rect(x,y+2,34,10,black)
    fill_rect(x+2,y+12,30,2,black)
    fill_rect(x+6,y+14,22,2,black)
    fill_rect(x+10,y+16,14,4,black)
    fill_rect(x+12,y+20,10,4,black)
    fill_rect(x+14,y+24,6,4,black)
    fill_rect(x+16,y+28,2,2,black)
    fill_rect(x+10,y+2,4,2,bg)
    fill_rect(x+20,y+2,4,2,bg)
    fill_rect(x+2,y+2,2,10,col)
    fill_rect(x+30,y+2,2,10,col)
    fill_rect(x+4,y+10,2,2,col)
    fill_rect(x+28,y+10,2,2,col)
    fill_rect(x+6,y+12,4,2,col)
    fill_rect(x+24,y+12,4,2,col)
    fill_rect(x+10,y+14,2,2,col)
    fill_rect(x+22,y+14,2,2,col)
    fill_rect(x+12,y+16,2,2,col)
    fill_rect(x+20,y+16,2,2,col)
    fill_rect(x+14,y+18,2,6,col)
    fill_rect(x+18,y+18,2,6,col)
    fill_rect(x+16,y+24,2,4,col)


class Bullet:
    def __init__(self,x,y,dir,speed,color=red):
        self.pos_x = x
        self.pos_y = y
        self.dir = dir
        self.speed = speed
        self.size = (2,6)
        self.col = color
        self.hidden = False
        fill_rect(self.pos_x,self.pos_y,self.size[0],self.size[1],self.col)
        
    def delete_bullet(self,index):
        fill_rect(self.pos_x,self.pos_y,self.size[0],self.size[1],white)
        del bullet_list[index]

class PlayerBullet(Bullet):
    def move(self,xx):
        if self.pos_y < 6:
            self.delete_bullet(xx)
            return
        
        elif get_pixel(self.pos_x,self.pos_y-6) != white and self.pos_y < 70:
            for idx,i in reversed(list(enumerate(enemy_list))):
                if i == "dead":
                    continue

                elif i.pos_x <= self.pos_x <= i.pos_x + 34:
                    self.delete_bullet(xx)
                    if i.is_shielded:
                        i._draw_shield()
                        return
                    return idx
           
        fill_rect(self.pos_x,self.pos_y,self.size[0],self.size[1],white)
        self.pos_y += self.dir*self.speed
        fill_rect(self.pos_x,self.pos_y,self.size[0],self.size[1],self.col)

class EnemyBullet(Bullet):
    def move(self,xx):
        if self.hidden:
            if self.pos_y > 70:
                self.hidden = False
            else:
                self.pos_y += self.dir*self.speed
            return

        elif self.pos_y > 210:
            self.delete_bullet(xx)
            return

        elif get_pixel(self.pos_x,self.pos_y+6) != white and self.pos_y < 150:
            for idx,i in reversed(list(enumerate(enemy_list))):
                if i == "dead":
                    continue
                elif i.pos_x <= self.pos_x <= i.pos_x + 34:
                    fill_rect(self.pos_x,self.pos_y,self.size[0],self.size[1],white) 
                    enemy_list[idx].load_texture()
                    self.hidden = True
                    return

        elif get_pixel(self.pos_x,self.pos_y+6) != white:
            self.delete_bullet(xx)
            return "player_hit"

        fill_rect(self.pos_x,self.pos_y,self.size[0],self.size[1],white)
        self.pos_y += self.dir*self.speed
        fill_rect(self.pos_x,self.pos_y,self.size[0],self.size[1],self.col)


class SpaceShip:
    def __init__(self,x,y,hitpoints,class_dat,move_dat):
        self.pos_x = x
        self.pos_y = y
        self.size = 34
        self.hp = hitpoints

    def hit(self) -> True or False:
        self.hp -= 1
        if self.hp <= 0:
            fill_rect(self.pos_x,self.pos_y,34,34,white)
            return True
        return False

class Player(SpaceShip):
    def __init__(self,x,y,hitpoints,class_dat,move_dat):
        super().__init__(x,y,hitpoints,class_dat,move_dat)
        self.shot_delay = monotonic()
        self.speed = 3
        self.life_colors = [red, red, red]
        self.load_texture()

    def move_hor(self,dir):
        fill_rect(self.pos_x,self.pos_y,self.size,self.size,white)
        self.pos_x += dir*self.speed
        self.load_texture()

    def load_texture(self):
        x,y = self.pos_x, self.pos_y
        fill_rect(x+16,y,2,2,black)
        fill_rect(x+14,y+2,6,4,black)
        fill_rect(x+12,y+6,10,6,black)
        fill_rect(x+10,y+12,14,2,black)
        fill_rect(x+6,y+14,22,2,black)
        fill_rect(x+2,y+16,30,2,black)
        fill_rect(x,y+18,34,6,black)
        fill_rect(x+2,y+24,30,2,black)
        fill_rect(x+10,y+26,14,2,black)
        fill_rect(x+16,y+4,2,4,self.life_colors[2])
        fill_rect(x+14,y+8,2,6,self.life_colors[2])
        fill_rect(x+18,y+8,2,6,self.life_colors[2])
        fill_rect(x+12,y+14,2,2,self.life_colors[2])
        fill_rect(x+20,y+14,2,2,self.life_colors[2])
        fill_rect(x+2,y+18,2,6,self.life_colors[0])
        fill_rect(x+4,y+22,6,2,self.life_colors[0])
        fill_rect(x+10,y+24,4,2,self.life_colors[0])
        fill_rect(x+30,y+18,2,6,self.life_colors[1])
        fill_rect(x+24,y+22,6,2,self.life_colors[1])
        fill_rect(x+20,y+24,4,2,self.life_colors[1])
    
    def hit(self) -> True or False:
        self.hp -= 1
        if self.hp <= 0:
            fill_rect(self.pos_x,self.pos_y,34,34,white)
            return True
        self.life_colors[3 - self.hp] = gray 
        self.load_texture()
        return False
    
    def player_died(self):
        enemy_list.clear()
        action_list.clear()
        moving_list.clear()
        fill_rect(0,0,320,240,white)
        draw_string("Game Over",115,100,black)
        global player; player = None

    def shoot(self):
        if monotonic() - self.shot_delay > 0.9:
            bullet_list.append(PlayerBullet(self.pos_x+16,self.pos_y-6,-1,5))
            self.shot_delay = monotonic()


class Enemy(SpaceShip):
    def __init__(self,x,y,hitpoints,class_dat,move_dat):
        super().__init__(x,y,hitpoints,class_dat,move_dat)
        self.is_shielded = False
        if move_dat is not None:
            self.axis = move_dat[0]
            self.total_distance = move_dat[1]
            self.px_update = move_dat[2]
            self.rounds = abs(self.total_distance/self.px_update)

            self.loop = move_dat[3]
            self.wait_time = move_dat[4]
            self.delay = 0
            self.dir = 1

    def _move_x(self):
        if self.is_shielded:
            self._draw_shield(white)
        fill_rect(self.pos_x,self.pos_y,self.size,self.size,white)
        self.pos_x += int(self.dir * self.px_update)
        self.load_texture()
        if self.is_shielded:
            self._draw_shield()

    def _move_y(self,col=None):
        if self.is_shielded:
            self._draw_shield(white)
        fill_rect(self.pos_x,self.pos_y,self.size,self.size,white)
        self.pos_y += int(self.dir * self.px_update)
        if col is not None:
            self.load_texture(col)
        else:
            self.load_texture()
        if self.is_shielded:
            self._draw_shield()

    def move(self):
        if monotonic() - self.delay < self.wait_time:
            return
        elif self.axis == "x":
            self._move_x()
        else:
            self._move_y()
        self.rounds -= 1

        if self.rounds == 0:
            if not self.loop:
                return True
            self.dir *= -1
            self.rounds = abs(self.total_distance / self.px_update)
            self.delay = monotonic()

    def shoot(self):
        bullet_list.append(EnemyBullet(self.pos_x+16,self.pos_y+36,1,self.bullet_speed))

    def _draw_shield(self,col=blue):
        x,y, = self.pos_x, self.pos_y
        fill_rect(x+16,y+32,2,2,col)
        fill_rect(x+14,y+30,2,2,col)
        fill_rect(x+18,y+30,2,2,col)
        fill_rect(x+12,y+28,2,2,col)
        fill_rect(x+20,y+28,2,2,col)
        fill_rect(x+10,y+24,2,4,col)
        fill_rect(x+22,y+24,2,4,col)
        fill_rect(x+8,y+20,2,4,col)
        fill_rect(x+24,y+20,2,4,col)
        fill_rect(x+6,y+18,2,2,col)
        fill_rect(x+26,y+18,2,2,col)
        fill_rect(x+2,y+16,4,2,col)
        fill_rect(x+28,y+16,4,2,col)
        fill_rect(x,y+14,2,2,col)
        fill_rect(x+32,y+14,2,2,col)

class BasicShip(Enemy):
    def load_texture(self):
        enemy_textures(self.pos_x,self.pos_y,(160, 100, 0))

class TankShip(Enemy):
    def load_texture(self):
        enemy_textures(self.pos_x,self.pos_y,(104, 4, 160))

class ShooterShip(Enemy):
    def __init__(self, x, y, hitpoints, class_dat, move_dat):
        super().__init__(x, y, hitpoints, class_dat, move_dat)
        self.shooting_type = class_dat[0]
        self.type_param = class_dat[1]
        self.bullet_speed = class_dat[2]
        self.shot_delay = 6

    def load_texture(self):
        enemy_textures(self.pos_x,self.pos_y,red)

    def action(self,idx):
        if self.shooting_type == "f" and monotonic() - self.shot_delay > self.type_param:
            self.shoot()
            self.shot_delay = monotonic()
        elif self.shooting_type == "r" and randrange(self.type_param) == 1:
            self.shoot()

class RammingShip(Enemy):
    def __init__(self, x, y, hitpoints, class_dat, move_dat):
        super().__init__(x, y, hitpoints, class_dat, move_dat)
        self.ram_type = class_dat[0]
        self.type_param = class_dat[1]
        self.ram_delay = 6
        self.is_ramming = False
        self.rounds += 10

    def load_texture(self,col=green):
        enemy_textures(self.pos_x,self.pos_y,col)

    def ram(self):
        if monotonic() - self.delay < self.wait_time:
            return
        
        elif player.pos_x +34 >= self.pos_x and player.pos_x < self.pos_x +34 and self.dir == 1 and self.pos_y > 130:
            if player.hit():
                player.player_died()
            
            else:
                fill_rect(self.pos_x,self.pos_y,self.size,self.size,white)
                self.pos_y = 147
                self.load_texture()

                self.dir *= -1
                self.rounds = self.total_distance/ self.px_update -3
                self.delay = monotonic()

        elif self.total_distance / self.px_update < self.rounds:
            self.rounds -= 1
            return
        
        self._move_y(lime)
        self.rounds -= 1

        if self.rounds == 0:
            self.dir *= -1
            self.rounds = self.total_distance / self.px_update + 10
            if self.is_ramming and self.pos_y < 80:
                self.load_texture(green)
                self.is_ramming = False
                return
            self.delay = monotonic()

    def action(self,idx):
        if self.is_ramming:
            self.ram()
        elif self.ram_type == "f" and monotonic() - self.ram_delay > self.type_param:
            self.is_ramming = True
            self.load_texture(lime)
            self.ram()
        elif self.ram_type == "r" and randrange(self.type_param) == 1:
            self.is_ramming = True
            self.load_texture(lime)
            self.ram()

class ShieldingShip(Enemy):
    def __init__(self, x, y, hitpoints, class_dat, move_dat):
        super().__init__(x, y, hitpoints, class_dat, move_dat)
        self.shield_chance = class_dat[0]
        self.shield_time = class_dat[1]
        self.tot_ships = class_dat[2]

    def load_texture(self,col=navy_blue):
        enemy_textures(self.pos_x,self.pos_y,col)

    def _indexes(self):
        yield 0, 0
        yield -1, 1
        yield 1, 2
        yield 8, 3
        yield 7, 4
        yield 9, 5

    def activate_shield(self,idx):
        self.load_texture(blue)
        self.shield_timer = monotonic()
        for i,j in self._indexes():
            try:
                if j > self.tot_ships:
                    return
                elif enemy_list[idx+i] != "dead":
                    enemy_list[idx+i].is_shielded = True
                    enemy_list[idx+i]._draw_shield()
            except:
                continue

    def remove_shield(self,idx):
        self.load_texture()
        for i,j in self._indexes():
            if j > self.tot_ships:
                return
            elif enemy_list[idx+i] != "dead":
                enemy_list[idx+i].is_shielded = False
                enemy_list[idx+i]._draw_shield(white)
    
    def action(self,idx):
        if self.is_shielded and monotonic() - self.shield_timer > self.shield_time:
            self.remove_shield(idx)
        elif randrange(self.shield_chance) == 1 and not self.is_shielded:
            self.activate_shield(idx)


def place_enemies(data):
    for i in range(2):
        if len(data[i]) == 0:
            continue
        y_position = (i*36) + 3
        for j in range(8):
            x_position = j*40 + 2
            moving_dat = data[i][j][2]
            class_dat = data[i][j][1]

            if data[i][j] == "dead":
                enemy_list.append("dead")
                continue
            elif data[i][j][0] == "basic":
                enemy_list.append(BasicShip(x_position,y_position,1,class_dat,moving_dat))
            elif data[i][j][0] == "tank":
                enemy_list.append(TankShip(x_position,y_position,5,class_dat,moving_dat))
            elif data[i][j][0] == "shooter":
                enemy_list.append(ShooterShip(x_position,y_position,2,class_dat,moving_dat))
                action_list.append(enemy_list[8*i+j])
            elif data[i][j][0] == "ram":
                enemy_list.append(RammingShip(x_position,y_position,3,class_dat,moving_dat))
                action_list.append(enemy_list[8*i+j])
            elif data[i][j][0] == "shield":
                enemy_list.append(ShieldingShip(x_position,y_position,2,class_dat,moving_dat))
                action_list.append(enemy_list[8*i+j])

            if moving_dat is not None and not isinstance(enemy_list[-1],RammingShip):
                moving_list.append(enemy_list[8*i+j])

            enemy_list[8*i+j].load_texture()

def next_level(lvl):
    lvl += 1
    fill_rect(0,0,320,240,white)
    _ = "Level "+str(lvl+1)
    draw_string(_,int(160 - 5*len(_)),100,black)
    sleep(2)
    fill_rect(0,0,320,240,white)
    place_enemies(levels[lvl])
    player.load_texture()
    return lvl

def show_tips():
    draw_string("< > to move",105,75,black)
    draw_string("EXE to shoot",100,95,black)
    draw_string("SHIFT to pause",90,115,black)

    while True:
        if keydown(KEY_RIGHT) or keydown(KEY_LEFT) or keydown(KEY_EXE):
            fill_rect(0,74,320,60,white)
            break

def title_screen(text):
    fill_rect(0,0,320,250,navy_blue)
    enemy_textures(250,32,red,navy_blue)
    enemy_textures(50,68,green,navy_blue)
    Player(32,184,4,None,None)
    fill_rect(267,100,2,6,red)
    fill_rect(267,142,2,6,red)
    fill_rect(49,120,2,6,red)
    for i,j in zip(text,(85,105,150)):
        draw_string(i,int(160 - 5*len(i)),j,white,navy_blue)

    while True:
        if keydown(KEY_OK):
            fill_rect(0,0,320,250,white)
            break


title_screen(("Cosmic Raiders","by Krumpachnik","(OK) to continue"))
player = Player(143,184,4,None,None)
place_enemies(levels[level])
show_tips()

while True:
    if keydown(KEY_RIGHT) and player.pos_x < 296:
        player.move_hor(1)
    elif keydown(KEY_LEFT) and player.pos_x > -12:
        player.move_hor(-1)
    if keydown(KEY_EXE):
        player.shoot()
    elif keydown(KEY_ANS):
        draw_string("shift to unpause",80,100,black)
        sleep(0.2)
        while True:
            if keydown(KEY_ANS):
                fill_rect(0,100,320,20,white)
                break
        sleep(0.2)

    for idx,i in enumerate(bullet_list):
        entity_hit = i.move(idx)
        if entity_hit == "player_hit":
            if player.hit():
                player.player_died()
        elif entity_hit is None:
            pass
        else:
            if enemy_list[entity_hit].hit():
                for i in [moving_list,action_list]:
                    if enemy_list[entity_hit] in i:
                        i.remove(enemy_list[entity_hit])

                enemy_list[entity_hit] = "dead"
                if enemy_list.count("dead") == len(enemy_list):
                    bullet_list, enemy_list, moving_list,= [], [], []
                    if level+1 == len(levels):
                        title_screen(("Congratualtions!","You won!"))
                    level = next_level(level)
                    action_delay = monotonic()

    if monotonic() - action_delay > 1:
        for i in action_list:
            i.action(enemy_list.index(i))

    if monotonic()-move_delay > 0.10:
        for i in moving_list:
            if i.move():
                moving_list.remove(i)
        move_delay = monotonic()

    if monotonic() - fps_limit > 0.05:
        pass
    else:
        sleep(0.05 - (monotonic()- fps_limit))
    fps_limit = monotonic()
    display(True)
