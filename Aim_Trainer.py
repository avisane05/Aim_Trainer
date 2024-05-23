import math, random, time, pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGATE_INCREMENT = 400
TARGATE_EVENT = pygame.USEREVENT

TARGATE_PADDING = 30

BG_COLOR = (0, 25, 40)
LIVES = 3
TOP_BAR_HEIGHT = 50

LABLE_FONT = pygame.font.SysFont("comicsans", 24)

class Targate:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x , y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size

def format_time(sec):
    milli = math.floor(int(sec * 1000 % 1000) / 100)
    seconds = int(round(sec % 60, 1))
    minutes = int(sec // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli:02d}"

def draw_top_bar(win, elapsed_time, target_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))
    
    time_lable = LABLE_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    
    speed = round(target_pressed / elapsed_time, 1)
    speed_lable = LABLE_FONT.render(f"Speed: {speed} t/s", 1, "black")

    hits_lable = LABLE_FONT.render(f"Hits: {target_pressed}", 1, "black")

    live_lable = LABLE_FONT.render(f"Lives: {LIVES - misses}", 1, "black")
    
    win.blit(time_lable, (5, 5))
    win.blit(speed_lable, (200, 5))
    win.blit(hits_lable, (450, 5))
    win.blit(live_lable, (650, 5))

def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2

def end_screen(win, elapsed_time, target_pressed, clicks):
    win.fill(BG_COLOR)

    time_lable = LABLE_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    
    speed = round(target_pressed / elapsed_time, 1)
    speed_lable = LABLE_FONT.render(f"Speed: {speed} t/s", 1, "white")

    hits_lable = LABLE_FONT.render(f"Hits: {target_pressed}", 1, "white")

    accuracy = round(target_pressed / clicks * 100, 1)
    accuracy_lable = LABLE_FONT.render(f"Accuracy: {accuracy}", 1, "white")

    win.blit(time_lable, (get_middle(time_lable), 100))
    win.blit(speed_lable, (get_middle(speed_lable), 200))
    win.blit(hits_lable, (get_middle(hits_lable), 300))
    win.blit(accuracy_lable, (get_middle(accuracy_lable), 400))

    pygame.display.update()

    run =True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)


def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    targates_press = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGATE_EVENT, TARGATE_INCREMENT)

    
    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGATE_EVENT:
                x = random.randint(TARGATE_PADDING, WIDTH - TARGATE_PADDING)
                y = random.randint(TARGATE_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGATE_PADDING)
                target = Targate(x, y)
                targets.append(target)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
        
        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targates_press += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, targates_press, clicks)

        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targates_press, misses)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()

