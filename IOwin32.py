import os, pygame
from pygame.locals import *
from pygame.compat import geterror
from event import EventControllerMember, Event


main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'graphics')

def load_imageBAK(name, colorkey=None):
	fullname = os.path.join(data_dir, name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error:
		print ('Cannot load image:', fullname)
		raise SystemExit(str(geterror()))
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()
	
def load_image(name, colorkey=None):
	fullname = os.path.join(data_dir, name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error:
		print ('Cannot load image:', fullname)
		raise SystemExit(str(geterror()))
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image

class SatSprite(pygame.sprite.Sprite):
	def __initBAK__(self, sat):
		pygame.sprite.Sprite.__init__(self) #call Sprite initializer
		fileName=sat.name+'small.jpg'
		#self.image, self.rect = load_image(fileName, -1)
		self.image, self.rect = load_image(fileName, -1)
		#rawImage = load_image(fileName)
		print(self.image)
		self.image = pygame.transform.scale(self.image, (20, 20))
		
	def __init__(self, sat):
		pygame.sprite.Sprite.__init__(self)
		rawImage=load_image(sat.name+'.jpg')
		self.image = pygame.transform.scale(rawImage, (20, 20))
		self.rect = self.image.get_rect()
		
	def update(self):
		"move the sprite based on the mouse position"
		pos = pygame.mouse.get_pos()
		self.rect.center = pos
		
class MainGameBackground:
	def __init__(self, game):
		
		self.game=game

		#Initialise everything
		self.game=game
		pygame.init()
		#iphone 8+ screen 1920*1080
		self.display=(int(1920/2), int(1080/2))
		self.screen = pygame.display.set_mode(self.display)
		pygame.display.set_caption('twentyfifty')
		pygame.mouse.set_visible(True)
		
		#Create The Backgound
		background = pygame.Surface(self.screen.get_size())
		background = background.convert()
		background.fill((0, 0, 0))
		
		#Display The Background
		self.screen.blit(background, (0, 0))
		pygame.display.flip()
		
		#Prepare Game Objects
		clock = pygame.time.Clock()
		satSprite = SatSprite(game.system)
		allsprites = pygame.sprite.RenderPlain((satSprite))
		
		going = True
		while going:
			clock.tick(60)
			
			#Handle Input Events
			for event in pygame.event.get():
				if event.type == QUIT:
					going = False
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					going = False
				elif event.type == MOUSEBUTTONDOWN:
					pass
				elif event.type == MOUSEBUTTONUP:
					pass
				else:
					pass

			allsprites.update()

			#Draw Everything
			self.screen.blit(background, (0, 0))
			allsprites.draw(self.screen)
			pygame.display.flip()
			
		pygame.quit()
		
	def screenCenter(self):
		centre=tuple(int(x/2) for x in self.screenSize())
		return centre
		
	def screenSize(self):
		return self.screen.get_size()

		
if __name__ == "__main__":
	print('IOwin32.py is being run directly')
	vc=VideoController()
else:
    print('IOwin32.py loaded.')	   