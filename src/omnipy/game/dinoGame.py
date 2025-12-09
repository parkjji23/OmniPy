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

# 이미지
try:
    DINO_IMG = pygame.image.load('assets/game/dinoGame/dino.png').convert_alpha()
    OBSTACLE_IMG = pygame.image.load('assets/game/dinoGame/obstacle.png').convert_alpha()
    DINO_WIDTH, DINO_HEIGHT = 40, 40
    OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 40, 40
    DINO_IMG = pygame.transform.scale(DINO_IMG, (DINO_WIDTH, DINO_HEIGHT))
    OBSTACLE_IMG = pygame.transform.scale(OBSTACLE_IMG, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
except pygame.error as e:
    # 이미지 파일을 찾지 못하거나 로드할 수 없을 때 오류 메시지 출력
    print(f"이미지 로드 오류: {e}")
    # 프로그램 종료 또는 대체 사각형 사용 등의 후속 조치를 취할 수 있습니다.
    # 여기서는 간단히 오류를 출력하고 계속 진행한다고 가정합니다.
    pass

# ----------------- 공룡(Dino) 클래스 정의 -----------------
"""
- 공룡은 자신의 크기를 알고있다
- 공룡은 자신의 위치를 알고있다
- 공룡은 자신의 점프 상태를 알고있다
- 공룡은 중력을 받는다
"""
class Dino:
    def __init__(self):
        # self.rect = pygame.Rect(50, 300, 40, 40) # 공룡의 위치와 크기(왼/위/넓/높)
        self.rect = pygame.Rect(50, HEIGHT - DINO_HEIGHT, DINO_WIDTH, DINO_HEIGHT)
        self.jumping = False # 점프 상태
        self.velocity_y = 0 # 초기 수직 속도
        # 이미지 속성 추가
        self.image = DINO_IMG

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
        # self.rect = pygame.Rect(WIDTH, 300, 40, 40)
        self.rect = pygame.Rect(WIDTH, HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
        # 이미지 속성 추가
        self.image = OBSTACLE_IMG
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
        # pygame.draw.rect(screen, GREEN, dino.rect) # 그리기
        # 공룡 이미지 그리기 (수정된 부분)
        screen.blit(dino.image, dino.rect)


        # 장애물 그리기
        for obs in obstacles:
            # pygame.draw.rect(screen, RED, obs.rect)
            screen.blit(obs.image, obs.rect)

        pygame.draw.line(screen, (0, 0, 0), (0, HEIGHT), (WIDTH, HEIGHT), 2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

run_game()