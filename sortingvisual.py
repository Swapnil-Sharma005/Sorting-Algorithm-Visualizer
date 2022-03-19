from tarfile import LENGTH_PREFIX
import pygame
from pygame.locals import * 
import random
import time
import math
pygame.init()

# This class contain all the information related to the window screen drawing 
class ScreenInfo:
    WHITE   = 255,255,255
    BLACK   = 0,0,0
    RED     = 255,0,0
    CYAN    = 0,255,255
    SILVER	= 192,192,192 
    GREEN	= 0,128,0
    TEAL	= 0,128,128
    NAVY	= 0,0,128
    BUTTONC = 47,79,79
    BACKGROUND_COLOR = SILVER
    SIDE_PADDING = 100
    TOP_PADDING  = 150

    GRADIENTS = [
        CYAN,
        TEAL,
        NAVY
    ]

    def __init__ (self,width,height,lst):
        self.width = width
        self.height = height
        self.lst = lst

        self.window = pygame.display.set_mode((width,height)) # representing the window on screen
        pygame.display.set_caption("Sorting Visualizer")

        self.display_list(lst)
    
    def display_list(self,lst):
        self.lst = lst
        self.min_value = min(lst)
        self.max_value = max(lst)

        self.block_width = round((self.width-self.SIDE_PADDING)/len(lst)) # width of each element of list 
        self.block_height = round((self.height-self.TOP_PADDING)/(self.max_value-self.min_value)) #
        self.start_x = self.SIDE_PADDING//2

#This function is to generate the list of elements to visualize
def generate_list(n,min_value,max_value):
    lst = []
    for _ in range(n):
        val = random.randint(min_value,max_value)
        lst.append(val)

    return lst

#This function draw the generated elements on the screen 
def Drawing_list(screen, color_positions = {}, clear_bg=False):
    lst = screen.lst

    if clear_bg:
        clear_rect = (screen.SIDE_PADDING//2,screen.TOP_PADDING-50,screen.width-screen.SIDE_PADDING,screen.height)
        pygame.draw.rect(screen.window,screen.BACKGROUND_COLOR,clear_rect)

    for i , val in enumerate(lst):
        x = screen.start_x + i*screen.block_width
        y = screen.height - (val - screen.min_value) * screen.block_height

        color = screen.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        smallfont = pygame.font.SysFont('Corbel',screen.block_width)

        pygame.draw.rect(screen.window, color, (x,y,screen.block_width,screen.height))
        val = str(val)
        screen.window.blit(smallfont.render(val, True, screen.BLACK), (x,y))
    
    if clear_bg:
        pygame.display.update()


clicked = False

class button(ScreenInfo):

    width = 100
    height = 20
    win = pygame.display.set_mode((800,400))
    
    def __init__(self,x,y,text):
        self.x = x
        self.y = y
        self.text = text
    
    def draw_button(self):
        global clicked
        action = False

        pos = pygame.mouse.get_pos() # gets the mouse position

        button_rect = Rect(self.x,self.y,self.width,self.height) # pygame rect object for the button

        # checking mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(self.win, (95,158,160), button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(self.win, (176,224,230), button_rect)
        else:
            pygame.draw.rect(self.win, (0,206,209), button_rect)

        #add text to button
        font = pygame.font.SysFont('Constantia', 13)
        text_img = font.render(self.text, True, ScreenInfo.WHITE)
        text_len = text_img.get_width()
        self.win.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + (self.height/2-text_img.get_height()/2)))
        
        return action
		
Random_array = button(15,20,"Randomize Array")
Bubble_sort = button(125,20,"Bubble Sort")
Insertion_sort = button(235,20,"Insertion Sort")
Selection_sort = button(345,20,"Selection Sort")
Quick_sort = button(455,20,"Quick Sort")
Merge_sort = button(565,20,"Merge Sort")


def Drawing_screen(screen):
    screen.window.fill(screen.BACKGROUND_COLOR)
    Drawing_list(screen)

    Random_array.draw_button()
    Bubble_sort.draw_button()
    Insertion_sort.draw_button()
    Selection_sort.draw_button()
    Merge_sort.draw_button()
    Quick_sort.draw_button()
    pygame.display.update()



def Bubble_sorting(screen):
    lst = screen.lst
    
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):

            if lst[j] > lst[j+1]:
                lst[j],lst[j+1] = lst[j+1],lst[j]
                Drawing_list(screen,{j:screen.GREEN,j+1:screen.RED},True)
                time.sleep(0.1)
                #yield True # calling this function for each swap
    return lst

def Insertion_sorting(screen):
    lst = screen.lst

    for i in range(1,len(lst)):
        key = lst[i]
        j = i-1

        while j>-1 and key<lst[j]:
            lst[j+1] = lst[j]
            Drawing_list(screen,{j:screen.GREEN,j+1:screen.RED},True)
            time.sleep(0.1)
            j=j-1

        lst[j+1]=key
        Drawing_list(screen,{key:screen.GREEN,j+1:screen.RED},True)
        time.sleep(0.1)
    
    return lst


def Selection_sorting(screen):
    lst = screen.lst
    
    for i in range(len(lst)-1):
        k=i
        for j in range(i,len(lst)):
            if lst[j]< lst[k]:
                k=j
        lst[i],lst[k] = lst[k],lst[i]
        Drawing_list(screen,{i:screen.GREEN,k:screen.RED},True)
        time.sleep(0.1)
    
    return lst

def partition(screen,low,high):
    lst = screen.lst
    pivot = lst[high]
    i = low-1
    for j in range (low,high):
        if lst[j]<pivot:
            i = i+1
            lst[i],lst[j] = lst[j],lst[i]
            Drawing_list(screen,{i:screen.GREEN,j:screen.RED},True)
            time.sleep(0.1)
    lst[i+1],lst[high]=lst[high],lst[i+1]
    Drawing_list(screen,{i+1:screen.GREEN,high:screen.RED},True)
    time.sleep(0.1)
    return i+1


def Quick_sorting(screen,low,high):
    lst = screen.lst
    if(low<high):
        pi= partition(screen,low,high)
        Quick_sorting(screen,low,pi-1)
        Quick_sorting(screen,pi+1,high)
    return lst

def merge(screen,lst, l, m, r):
    n1 = m - l + 1
    n2 = r - m
 
    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)
 
    # Copy data to temp arrays L[] and R[]
    for i in range(0, n1):
        L[i] = lst[l + i]
 
    for j in range(0, n2):
        R[j] = lst[m + 1 + j]
 
    # Merge the temp arrays back into lst[l..r]
    i = 0     # Initial index of first subarray
    j = 0     # Initial index of second subarray
    k = l     # Initial index of merged subarray
 
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            lst[k] = L[i]
            Drawing_list(screen,{i:screen.GREEN,k:screen.RED},True)
            time.sleep(0.1)
            i += 1
        else:
            lst[k] = R[j]
            Drawing_list(screen,{j:screen.GREEN,k:screen.RED},True)
            time.sleep(0.1)
            j += 1
        k += 1
 
    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        lst[k] = L[i]
        Drawing_list(screen,{i:screen.GREEN,k:screen.RED},True)
        time.sleep(0.1)
        i += 1
        k += 1
 
    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        lst[k] = R[j]
        Drawing_list(screen,{j:screen.GREEN,k:screen.RED},True)
        time.sleep(0.1)
        j += 1
        k += 1
 
# l is for left index and r is right index of the
# sub-array of lst to be sorted
 
 
def Merge_sorting(screen,lst, l, r):
    if l < r:
 
        # Same as (l+r)//2, but avoids overflow for
        # large l and h
        m = l+(r-l)//2
 
        # Sort first and second halves
        Merge_sorting(screen,lst, l, m)
        Merge_sorting(screen,lst, m+1, r)
        merge(screen,lst, l, m, r)
 

# this to render the screen (pygame event loop)
def main():
    run = True
    clock = pygame.time.Clock() # regulate how quickly the below loop is runing 

    n=50
    min_value=10
    max_value=100
    lst = generate_list(n,min_value,max_value)
    screen = ScreenInfo(800.,400,lst)
    
    while run:
        clock.tick(60)

        if Random_array.draw_button():
            print("Randomize Array")
            lst = generate_list(n,min_value,max_value)
            screen = ScreenInfo(800.,400,lst)
            screen.display_list(lst)

        if Bubble_sort.draw_button():
            print("Bubble Sort")
            Bubble_sorting(screen)

        if Insertion_sort.draw_button():
            print("Insertion Sort")
            Insertion_sorting(screen)

        if Selection_sort.draw_button():
            print("Selection Sort")
            Selection_sorting(screen)

        if Merge_sort.draw_button():
            print("Merge Sort")
            Merge_sorting(screen,lst,0,n-1)
            
        if Quick_sort.draw_button():
            print("Quick Sort")
            Quick_sorting(screen,0,n-1)

        pygame.display.update()
        Drawing_screen(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: # if the mouse click the button
                pass
    pygame.quit()

if __name__ == "__main__":
    main()



