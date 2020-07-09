import pygame, sys, logging
from pygame.sprite import Group

#logging.disable(logging.CRITICAL)
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')

class Square(pygame.sprite.Sprite):
    def __init__(self,screen,square_size,cellx,celly,colour):
        super(Square,self).__init__()
        self.screen=screen
        self.colour=colour
        self.rect=pygame.Rect(cellx,celly,square_size,square_size)
    def draw_sq(self):
        pygame.draw.rect(self.screen, self.colour, self.rect)

class Piece(pygame.sprite.Sprite):
    def __init__(self, screen, image, px, py,code):
        super(Piece,self).__init__()
        self.screen = screen
        self.image = pygame.image.load('pieces_img/'+image)
        self.rect = self.image.get_rect()
        self.rect.centerx = px
        self.rect.bottom = py
        self.nature=code
    def blitme(self):
        self.screen.blit(self.image, self.rect)

class Game():
    square_size=80
    width=square_size*8
    height=width
    white=(255,255,255)
    black=(105,105,105)
    def __init__(self, side,n):
        pygame.init()
        pygame.display.set_caption("Chess Game")
        self.screen=pygame.display.set_mode((Game.width,Game.height))
        self.grid=Group()
        self.wpieces=Group()
        self.bpieces=Group()
        self.spawn=True
        self.play=False
        self.whites=True
        self.side=side
        self.server=n
        self.last_move="0"
        #self.side="blacks"
    def run(self):
        while True:
            self.listen_for_commands()
            self.update_screen()
    def listen_for_commands(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.play=True
                self.moving()
    def spawn_squares(self):
        if self.spawn:
            #spawn odd white and black squares
            for lin in range(4):
                for col in range(4):
                    cellx=col*Game.square_size*2
                    celly=lin*Game.square_size*2
                    new_square=Square(self.screen, Game.square_size, cellx, celly, Game.white)
                    self.grid.add(new_square)
                    cellx=Game.square_size+col*Game.square_size*2
                    celly=lin*Game.square_size*2
                    new_square=Square(self.screen, Game.square_size, cellx, celly, Game.black)
                    self.grid.add(new_square)
            #spawn even white and black squares
            for lin in range(4):
                for col in range(4):
                    cellx=col*Game.square_size*2
                    celly=Game.square_size+lin*Game.square_size*2
                    new_square=Square(self.screen, Game.square_size, cellx, celly, Game.black)
                    self.grid.add(new_square)
                    cellx=Game.square_size+col*Game.square_size*2
                    celly=Game.square_size+lin*Game.square_size*2
                    new_square=Square(self.screen, Game.square_size, cellx, celly, Game.white)
                    self.grid.add(new_square)
    def update_screen(self):
            self.spawn_squares()
            self.spawn_pieces()
            self.spawn=False

            print('self.server.send(self.last_move)')
            self.server.send(self.last_move)
            
            print('antes')
            try:
                foreign_play=self.server.receive()
                print('foreign_play:')
                print(foreign_play)
                if foreign_play!='0':
                    foreign_play=foreign_play.split(',')
                    print(foreign_play)
                    foreign_play[0]=foreign_play[0][:2]+str((7-int(foreign_play[0][2:])))
                    if self.side=="whites":
                        for otherpiece in self.bpieces.sprites():
                            if foreign_play[0][:2] in ['wq','wk','bq','bk']:
                                foreign_play[0]=foreign_play[0][:2]
                                control=otherpiece.nature[:2]
                            else:
                                control=otherpiece.nature
                            if control==foreign_play[0]:
                                otherpiece.rect.centerx=int(foreign_play[1])
                                otherpiece.rect.centery=int(foreign_play[2])
                                for mypiece in self.wpieces.sprites():
                                    if (mypiece.rect.centerx,mypiece.rect.centery)==(otherpiece.rect.centerx,otherpiece.rect.centery):
                                        self.wpieces.remove(mypiece)
                                break
                    else:
                        for otherpiece in self.wpieces.sprites():
                            if foreign_play[0][:2] in ['wq','wk','bq','bk']:
                                foreign_play[0]=foreign_play[0][:2]
                                control=otherpiece.nature[:2]
                            else:
                                control=otherpiece.nature
                            if control==foreign_play[0]:
                                otherpiece.rect.centerx=int(foreign_play[1])
                                otherpiece.rect.centery=int(foreign_play[2])
                                for mypiece in self.bpieces.sprites():
                                    if (mypiece.rect.centerx,mypiece.rect.centery)==(otherpiece.rect.centerx,otherpiece.rect.centery):
                                        self.bpieces.remove(mypiece)
                                break
            except Exception as e:
                print('update_screen')
                print(e)
            print('depois')
            for sq in self.grid.sprites():
                sq.draw_sq()
            if self.side=='whites':
                for piece in self.bpieces.sprites():
                    piece.blitme()
                for piece in self.wpieces.sprites():
                    piece.blitme()
            else:
                for piece in self.wpieces.sprites():
                    piece.blitme()
                for piece in self.bpieces.sprites():
                    piece.blitme()
            pygame.display.flip()
            pygame.display.update()
    def spawn_pieces(self):
        if self.side=="whites":
            if self.spawn:
                for bpawn in range(8):
                    bpawn=Piece(self.screen,'bp.png',int(Game.square_size*bpawn+Game.square_size/2),int(Game.square_size*1+Game.square_size), 'bp'+str(bpawn))
                    self.bpieces.add(bpawn)
                blackline=['br', 'bh', 'bb', 'bk', 'bq', 'bb', 'bh', 'br']
                for bline in range(8):
                    bpiece=Piece(self.screen, str(blackline[bline])+'.png',int(Game.square_size*bline+Game.square_size/2),int(Game.square_size*1), str(blackline[bline])+str(bline))
                    self.bpieces.add(bpiece)
                for wpawn in range(8):
                    wpawn=Piece(self.screen,'wp.png',int(Game.square_size*wpawn+Game.square_size/2),int(Game.square_size*6+Game.square_size), 'wp'+str(wpawn))
                    self.wpieces.add(wpawn)
                whiteline=['wr', 'wh', 'wb', 'wq', 'wk', 'wb', 'wh', 'wr']
                for wline in range(8):
                    wpiece=Piece(self.screen, str(whiteline[wline])+'.png',int(Game.square_size*wline+Game.square_size/2),int(Game.square_size*8), str(whiteline[wline])+str(wline))
                    self.wpieces.add(wpiece)
        else:
            if self.spawn:
                for bpawn in range(8):
                    bpawn=Piece(self.screen,'bp.png',int(Game.square_size*bpawn+Game.square_size/2),int(Game.square_size*6+Game.square_size), 'bp'+str(bpawn))
                    self.bpieces.add(bpawn)
                blackline=['br', 'bh', 'bb', 'bq', 'bk', 'bb', 'bh', 'br']
                for bline in range(8):
                    bpiece=Piece(self.screen, str(blackline[bline])+'.png',int(Game.square_size*bline+Game.square_size/2),int(Game.square_size*8), str(blackline[bline])+str(bline))
                    self.bpieces.add(bpiece)
                for wpawn in range(8):
                    wpawn=Piece(self.screen,'wp.png',int(Game.square_size*wpawn+Game.square_size/2),int(Game.square_size*1+Game.square_size), 'wp'+str(wpawn))
                    self.wpieces.add(wpawn)
                whiteline=['wr', 'wh', 'wb', 'wk', 'wq', 'wb', 'wh', 'wr']
                for wline in range(8):
                    wpiece=Piece(self.screen, str(whiteline[wline])+'.png',int(Game.square_size*wline+Game.square_size/2),int(Game.square_size*1), str(whiteline[wline])+str(wline))
                    self.wpieces.add(wpiece)
    def moving(self):
        pos=pygame.mouse.get_pos()
        #acquire moved piece
        for piece in self.bpieces.sprites():
            if piece.rect.collidepoint(pos):
                move=piece
                break
        for piece in self.wpieces.sprites():
            if piece.rect.collidepoint(pos):
                move=piece
                break
        #save tuple for eventual snapback
        try:
            base=(move.rect.centerx, move.rect.centery)
            #drag's loop
            while self.play:
                pos=pygame.mouse.get_pos()
                #drag sprite
                move.rect.centerx, move.rect.centery=pos
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        #stop dragging sprite
                        self.play=False
                        #snap sprite onto square
                        for sq in self.grid.sprites():
                            if sq.rect.collidepoint((move.rect.centerx, move.rect.centery)):
                                move.rect.centerx, move.rect.centery=(sq.rect.centerx, sq.rect.centery)
                        #reset to base square if moved pieces's new square overlaps moved piece with another piece of the same color
                        if self.side=='whites':
                            self.snap_back(move,base,self.wpieces.sprites())
                        else:
                            self.snap_back(move,base,self.bpieces.sprites())
                        #eats piece in case of collision between pieces of different colours
                        if move in self.wpieces:
                            pygame.sprite.groupcollide(self.wpieces, self.bpieces, False, True)
                        else:
                            pygame.sprite.groupcollide(self.wpieces, self.bpieces, True, False)
                    make_play=str(move.nature)+','+str(Game.square_size*8-move.rect.centerx)+','+str(Game.square_size*8-move.rect.centery)
                    print(make_play)
                    self.last_move=make_play
                    self.update_screen()
        except UnboundLocalError:
            pass
    

    def snap_back(self,move,base,sprite):
        for piece in sprite:
            if piece!=move:
                if (piece.rect.centerx,piece.rect.centery)==(move.rect.centerx, move.rect.centery):
                    move.rect.centerx, move.rect.centery=base
                    break


from network import Network

n=Network()
side=n.get_p()[:6]
print(side)
session=Game(side,n)
session.run()

#implement last_move