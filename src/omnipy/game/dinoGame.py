import pygame
import random

# ----------------- Pygame 초기화 -----------------
pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dino Game')

# 색상
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# ----------------- 공룡(Dino) 클래스 정의 -----------------
"""
- 공룡은 자신의 크기를 알고있다
- 공룡은 자신의 위치를 알고있다
- 공룡은 자신의 점프 상태를 알고있다
- 공룡은 중력을 받는다
"""
class Dino:
    def __init__(self):
        self.rect = pygame.Rect(50, 300, 40, 40) # 공룡의 위치와 크기(왼/위/넓/높)
        self.jumping = False # 점프 상태
        self.velocity_y = 0 # 초기 수직 속도

    def jump(self):
        if not self.jumping: # 점프 중이 아닐때만 점프 가능(조정시, 더블 점프 구현가능)
            self.jumping = True
            self.velocity_y = -10 # 점프높이

    def update(self): # game은 매 프레임마다 데이터를 변경하여 그려주는 작업임
        self.rect.y += self.velocity_y
        self.velocity_y += 0.5 # 중력 효과(속도 증가시킴)

        if self.rect.y > 300: # 바닥에 닿으면 ?
            self.rect.y = 300 # 바닥에 고정시키고
            self.jumping = False # 점프 상태 초기화
            self.velocity_y = 0 # 속도 초기화

# ----------------- 장애물 클래스 정의 -----------------
class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH, 300, 40, 40)
    def update(self):
        self.rect.x -= 5

# ----------------- 메인 루프 -----------------
def run_game():
    """
    Dino Game의 전체 게임 루프 실행
    """
    clock = pygame.time.Clock() # 게임속도 조절
    dino = Dino() # class Dino 객체 생성
    running = True  # 게임 반복실행
    obstacles = []

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                dino.jump()

        # 장애물 생성
        if random.randint(1, 100) <= 3: # 1부터 100 사이의 난수를 생성하고 이 숫자가 3이하일 경우에만 장애물이 생성됩니다. 3%의 확률입니다.
            obstacles.append(Obstacle()) # 장애물 리스트에 장애물 객체를 생성하여 append
        # 장애물 업데이트
        for obs in obstacles[:]:
            obs.update()
            if obs.rect.x < 0: # x의 위치가 0이하가 되어 화면 밖으로 넘어가면
                obstacles.remove(obs) # 장애물을 리스트에서 제거
            if dino.rect.colliderect(obs): # 충돌 감지
                running = False

        dino.update() # 공룡 업데이트
        pygame.draw.rect(screen, GREEN, dino.rect) # 그리기
        # 장애물 그리기
        for obs in obstacles:
            pygame.draw.rect(screen, RED, obs.rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

run_game()