import pygame
pygame.init() # initializes few things which we will need later


WIDTH , HEIGHT = 700 , 500 # width and height of window
FPS = 60 # frames per second
WHITE = (255,255,255)
BLACK = (0,0,0)
PADDLE_WIDTH , PADDLE_HEIGHT = 20,100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans",40)  # font of the text
WIN_SCORE = 5


WIN = pygame.display.set_mode((WIDTH , HEIGHT)) # creating a window 
pygame.display.set_caption("PONG")  #title of window / game


class Paddle:
    COLOR = WHITE # color of paddle 
    VEL = 4  # velocity of the paddle
    
    def __init__(self, x , y , width , height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height 
    
    def draw(self,win):
        pygame.draw.rect(win , self.COLOR , (self.x, self.y , self.width , self.height)) #draws a rectangle (where i want to draw it , color , (pass a rectanggle x,y,width,height))

    
    def move(self , up=True):
        if up:
            self.y -= self.VEL  # moves up 
        else:
            self.y += self.VEL  # moves down
            
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
    
            
class Ball:
    MAX_VEL = 7  # initial velocity of the ball 
    COLOR =WHITE
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius=radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0
    
    
    def draw(self,win):
        pygame.draw.circle(win , self.COLOR , (self.x , self.y) , self.radius)
        
        
    def move(self):
        self.x +=self.x_vel
        self.y +=self.y_vel


    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1  # if the ball went out on the left side then when we reset we want the ball to go right and voce versa
        self.y_vel = 0
        


def draw(win,paddles,ball,left_score,right_score):
    win.fill(BLACK) # background color (we put in a rgb value)
    
    left_score_text = SCORE_FONT.render(f"{left_score}" , 1 , WHITE)  # 1 stands for anti aliasing always keep 1 
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text , (WIDTH//4 - left_score_text.get_width()//2 , 20))  # drawing the left score (text , width , height)
    win.blit(right_score_text, ((WIDTH*(3/4)) - right_score_text.get_width()//2, 20))
    
    for paddle in paddles:
        paddle.draw(win)
    
    
    ball.draw(win)
    
    pygame.display.update() # updates the window should be done at last after all the changes because it takes time



def handle_paddle_movement(keys , left_paddle , right_paddle):   # lettered keys are all lowercase and other keys are uppercase like enter,shift,up,down
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >=0:    # to check if key pressed and the paddles dont exceed the window 
        left_paddle.move(up=True)
    if(keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height<= HEIGHT):
        left_paddle.move(up=False)
        
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if(keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT):
        right_paddle.move(up=False)



def handle_collision(ball,left_paddle,right_paddle):
    if ball.y + ball.radius >= HEIGHT:  # check if ball hits bottom ceiling and if yes then reverse the velocity
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:  # check if ball hits top ceiling and if yes then reverse the velocity
        ball.y_vel *= -1
        
        
        
        
    if ball.x_vel < 0:  # check left paddle
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:  # ball is within the height of left paddle
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:  # ball touches the right paddle 
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.height / 2  # finding middle of paddle at that moment
                difference_in_y = middle_y - ball.y   # difference between the ball and middle of paddle when collision
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL  # reduction factor to find appropriate y velocity
                ball.y_vel = -1 * difference_in_y / reduction_factor
                
    
    else:  # check right paddle 
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:  # ball is within the height of right paddle
            if ball.x + ball.radius >= right_paddle.x:   # ball touches the right paddle
                ball.x_vel *= -1
                 
                middle_y = right_paddle.y + right_paddle.height / 2 
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                ball.y_vel = -1 * difference_in_y / reduction_factor
        

def main():
    run = True
    clock = pygame.time.Clock() # regulates the frame rate of our game so that it runs at the same pace in every computer
    
    left_paddle =Paddle(10 , HEIGHT//2 - PADDLE_HEIGHT//2 , PADDLE_WIDTH , PADDLE_HEIGHT)   
    right_paddle =Paddle(WIDTH - 10 - PADDLE_WIDTH , HEIGHT//2 - PADDLE_HEIGHT//2 , PADDLE_WIDTH , PADDLE_HEIGHT)
     
    ball= Ball(WIDTH // 2 , HEIGHT // 2 , BALL_RADIUS)
    
    left_score = 0
    right_score = 0
    while run:  # main loop that handles the game (moving the paddle , moving the ball , handling collisions)
        clock.tick(FPS)  # limits the fps so it cant go any higher than the given value but can go lower in slow computers
        draw(WIN, [left_paddle, right_paddle],ball,left_score,right_score)
        for event in pygame.event.get():  # gets all the events like clicking mouse ,keyboard , closing window
            if event.type == pygame.QUIT: # quitting the window clicking the red button on top right
                run = False
                break
        
        keys = pygame.key.get_pressed()  # gives us a list of all the different keys pressed
        handle_paddle_movement(keys , left_paddle , right_paddle)
        
        ball.move()
        handle_collision(ball,left_paddle,right_paddle)
         
        if ball.x < 0:  # if ball moves past the left side 
            right_score += 1
            ball.reset()
            
        elif ball.x > WIDTH:  # if ball moves past the right side
            left_score += 1
            ball.reset()
        
        won = False
        
        if left_score >= WIN_SCORE:
            won = True
            win_text = "Left Player Won"
        elif right_score >= WIN_SCORE:
            won = True
            win_text = "Right Player Won"
        
        if won:
            text = SCORE_FONT.render(win_text , 1 , WHITE)
            WIN.blit(text ,(WIDTH//2 - text.get_width()//2 , HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000) 
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0
        
    pygame.quit() # quits pygame and closes the program
    

if __name__=='__main__':  # checks if this method is run from game.py and not imported in other file and run from there 
    main()
    