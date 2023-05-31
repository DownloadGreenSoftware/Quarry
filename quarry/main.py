import pygame
import json
print("All modules imported")

with open("gameInfo.json", "r") as f:
    gameInfo = json.load(f)
print("All resource packs loaded")

def error(code):
    print("An error occured! Read troubleshoot.txt for more information. Error code: " + code)
    errorCode = code
    pygame.quit()

pygame.init()
errorCode = "0"
level = "1"
quarry = "Tutorial Quarry"
rsrc = gameInfo["resource pack"]
gridded = gameInfo["gridded"]
try:
    stonePath = "rsrc/" + rsrc + "/stone.png"
    stone = pygame.image.load(stonePath)
    icon = pygame.image.load("rsrc/" + rsrc + "/" + gameInfo["icon"])
    pick = pygame.image.load("rsrc/" + rsrc + "/pick.png")
    spike = pygame.image.load("rsrc/" + rsrc + "/spike.png")
except:
    error("1")
size = 1280
win = pygame.display.set_mode((size, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Quarry")
pygame.display.set_icon(icon)
pygame.display.toggle_fullscreen()
cameraX = 50
cameraY = 50
print("Initialized main game")

with open("levels/" + quarry + "/" + level + ".json", "r") as f:
    rawInfo = json.load(f)

readableData = []
rows = rawInfo["height"]
rawData = rawInfo["blocks"]
tileSize = size // rows
for key in rawData:
    readableData.append(rawData[key])

class World():
    def __init__(self, data):
        self.tileList = []
        
        rowCount = 0
        for row in data:
            columnCount = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(stone, (tileSize, tileSize))
                    imgRectangle = img.get_rect()
                    imgRectangle.x = columnCount * tileSize
                    imgRectangle.y = rowCount * tileSize
                    tile = (img, imgRectangle)
                    self.tileList.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(spike, (tileSize, tileSize))
                    imgRectangle = img.get_rect()
                    imgRectangle.x = columnCount * tileSize
                    imgRectangle.y = rowCount * tileSize
                    tile = (img, imgRectangle)
                    self.tileList.append(tile)
                columnCount += 1
            rowCount += 1

    def renderTiles(self):
        for tile in self.tileList:
            modifiedLocation = tile[1]
            mls1 = list(modifiedLocation)
            mls1[0] = mls1[0] - cameraX
            mls1[1] = mls1[1] - cameraY
            mls1[2] = mls1[2] - cameraX
            mls1[3] = mls1[3] - cameraY
            modifiedLocation = tuple(mls1)
            win.blit(tile[0], modifiedLocation)
            

world = World(readableData)

def render(window):
    global size, rows, tileSize
    window.fill((0, 0, 0))
    world.renderTiles()
    if gridded:
        grid(window, size, rows)

def grid(window, size, rows):
    gX = 0 - cameraX
    gY = 0 - cameraY

    for one in range(rows):
        gX += tileSize
        gY += tileSize
        pygame.draw.line(window, (255, 255, 255), (gX, 0), (gX, size))
        pygame.draw.line(window, (255, 255, 255), (0, gY), (size, gY))


print("Started game loop")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_LEFT or pygame.K_a:
                cameraX -= 1
                print(cameraX)
            if event.type == pygame.K_RIGHT or pygame.K_d:
                cameraX += 1
            if event.type == pygame.K_UP or pygame.K_w:
                cameraY -= 1
            if event.type == pygame.K_DOWN or pygame.K_s:
                cameraY += 1 
    cameraX += 1
    win.fill("black")
    render(win)
    pygame.display.update()
    clock.tick(60)        
print("Flawless! The game closed without any issues! Error code: " + errorCode)
pygame.quit()
