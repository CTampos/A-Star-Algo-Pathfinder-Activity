import colorama
import start
import Nodes
import pygame

from nodeClass import Node

from colorama import Fore, Back, Style
colorama.init()
pygame.init()
pygame.font.init()

size = [460, 200]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('TAMPOS - A* ALGO PATHFINDER')

clock = pygame.time.Clock()
fps = 30

a = Nodes.Node(20, 20, 0)
b = Nodes.Node(660, 660, 1)

grid = []
snap = []
for i in range(0, 200, 20):
    for j in range(0, 200, 20):
        grid.append(Node(j, i, 'hidden', a, b))
        snap.append(pygame.Rect(j, i, 20, 20))

open_nodes = []
closed_nodes = []

for cell in grid:
    if cell.g == 0:
        start_node = grid.index(cell)

done = False
font = pygame.font.SysFont('calibri', 81)
btn_start = start.Start([51,51,51], [70,70,70], 230, 65, 200, 70, font, "START")
counter = 0
step = 0
doOnce = 0

def uiDraw(screen):
    white = (255, 255, 255)
    screen.fill(white)
    pygame.draw.rect(screen, [51, 51, 51], (0, 0, 200, 200), 1)
    btn_start.show(screen)
    screen.blit(font.render(''.format(counter), 1, [255, 255, 255]), (710, 135))
    a.show(screen)
    b.show(screen)

start = False
locations = []

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()

    if not start:
        uiDraw(screen)
        pos = pygame.mouse.get_pos()
        pressed = pygame.mouse.get_pressed()
        key = pygame.key.get_pressed()
        uiDraw(screen)

        btn_start.onHover(pos)
        if btn_start.onPressed(pos, pressed):
            start = True

        if a.update(pos, pressed, snap) == False and b.update(pos, pressed, snap) == False:
            if pressed == (1, 0, 0):
                index = pygame.Rect(pos[0], pos[1], 1, 1).collidelist(snap)

                if snap[index][0] != a.x or snap[index][0] != b.x or snap[index][1] != a.y or snap[index][1] != b.y:
                    locations.append(snap[index])

        temp = []
        for loc in locations:
            pygame.draw.rect(screen, [100, 100, 100], loc, 0)

            if (loc[0] == a.x and loc[1] == a.y) or (loc[0] == b.x and loc[1] == b.y):
                pass
            else:
                temp.append(loc)
        locations = temp

    if start and doOnce == 0:
        for node in grid:
            node.recalculate(a, b)

            for loc in locations:
                if node.x == loc[0] and node.y == loc[1]:
                    node.mode = 'wall'
        
            if node.g == 0:
                start_node = grid.index(node)

        if counter < 0:
            counter = 0

        open_nodes.append(grid[start_node])
        grid[start_node].mode = 'open'

        doOnce += 1

    if start:
        if step == counter:

            if len(open_nodes) == 0:
                break


            for cell in grid:
                cell.show(screen)

            pygame.draw.rect(screen, [255, 255, 0], (a.x, a.y, 20, 20))
            pygame.draw.rect(screen, [255, 0, 255], (b.x, b.y, 20, 20))
            lowestF = 10**10
            lowestH = 10**10

            for node in open_nodes:
                if node.f < lowestF:
                    lowestF = node.f
                    lowestH = node.h
                    current_node = node

                if lowestF == node.f:
                    if node.h < lowestH:
                        lowestF = node.f
                        lowestH = node.h
                        current_node = node

            open_nodes.remove(current_node)
            closed_nodes.append(current_node)
            current_node.mode = 'closed'
            temp = []

            for node in grid:
                if node.x == current_node.x + 20 and node.y == current_node.y:
                    temp.append(node)
                if node.x == current_node.x - 20 and node.y == current_node.y:
                    temp.append(node)
                if node.x == current_node.x and node.y == current_node.y + 20:
                    temp.append(node)
                if node.x == current_node.x and node.y == current_node.y - 20:
                    temp.append(node)

            for node in temp:
                if closed_nodes.count(node) == 0 and node.mode != 'wall':
                    if open_nodes.count(node) == 0:
                        open_nodes.append(node)
                        node.mode = 'open'

                    node.parent = current_node

            if current_node.x == b.x and current_node.y == b.y:
                done = True

            step = 0
        else:
            step += 1

    pygame.display.update()
    clock.tick(fps)

path = []
x, y = current_node.x, current_node.y
while True:
    path.append((x + 10, y + 10))
    x, y = current_node.parent.x, current_node.parent.y

    current_node = current_node.parent

    if x == a.x and y == a.y:
        break
path.append((a.x + 10, a.y + 10))
path.reverse()

step = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()

    mousePos = pygame.mouse.get_pos()


    for cell in grid:
        cell.show(screen)
        cell.update(mousePos)


    for i in range(0, len(path) - 1):
        pygame.draw.line(screen, [0, 0, 200], path[i], path[i + 1], 5)
    pygame.draw.rect(screen, [255, 255, 0], (a.x, a.y, 20, 20))
    pygame.draw.rect(screen, [255, 0, 255], (b.x, b.y, 20, 20))
    pygame.draw.circle(screen, [255, 255, 255], (int(path[step][0]), int(path[step][1])), 5)

    if step != len(path) - 1:
        step += 1
    else:
        step = 0

    pygame.display.update()
    clock.tick(fps)
