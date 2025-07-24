import pygame

# create the game screen
screen = pygame.display.set_mode((500, 500))
# Window title
pygame.display.set_caption('Wordle')
clock = pygame.time.Clock()
run = True
wordle_array = []
alphabet = ['A', 'B', 'C', 'D', 'E', 'F',
            'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R',
            'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z']
word_of_day = "PLATE"
user_row = 0

# vars
sq_dimensions = 50
sq_border_width = 2
sq_spacing_from_each = 5

screen_bg_color = [255, 255, 255]
no_letter_outline_color = [143, 143, 143]
green = [30, 191, 25]
yellow = [237, 240, 60]
gray = [69, 69, 68]

# pygame setup
pygame.init()

# create a font object
font = pygame.font.Font('freesansbold.ttf', 32)


# wordle letter object
class Letter:
    def __init__(self, has_letter:bool=False, letter:chr=None):
        self.has_letter = has_letter
        self.letter = letter
        # status relative to the word of the day
        # unknown, not in word, wrong pos, right pos
        self.status = "unknown"

        # for formatting/looks
        self.screen = screen
        self.dimensions = 50
        self.border_width = 2
        self.no_letter_outline_color = [143, 143, 143]
        self.yes_letter_outline_color = [0, 0, 0]

    
    def show(self, x:float, y:float):
        if self.status == "right pos":
            pygame.draw.rect(screen, green, (x, y, self.dimensions, self.dimensions))
        elif self.status == "wrong pos":
            pygame.draw.rect(screen, yellow, (x, y, self.dimensions, self.dimensions))
        elif self.status == "not in word":
            pygame.draw.rect(screen, gray, (x, y, self.dimensions, self.dimensions))

        if self.has_letter == True:
                pygame.draw.rect(screen, self.yes_letter_outline_color, (x, y, self.dimensions, self.dimensions), self.border_width)
        else:
            pygame.draw.rect(screen, self.no_letter_outline_color, (x, y, self.dimensions, self.dimensions), self.border_width)
        
        # draw letter
        text = font.render(wordle_array[r][c].letter, True, (0, 0, 0))
        # text rect is like a thing for text to sit on/be seen on
        textRect = text.get_rect()
        textRect.center = (110 + c*55 + wordle_array[r][c].dimensions/2, 100+ wordle_array[r][c].dimensions/2)
        screen.blit(text, textRect)
        




# setup
def setup():
    for r in range(0, 6, 1):
        word_array = []
        for c in range(0, 5, 1):
            word_array.append(Letter())
        wordle_array.append(word_array)

# assigns statuses to different boxes
def check_word(word_array):
    for i in range(len(word_array)):
        # first check if the letter is in the correct position
        if word_array[i].letter == word_of_day[i:i+1]:
            print("correct pos!")
            word_array[i].status = "right pos"
        # 2nd, check if letter is in the word
        elif word_array[i].letter in word_of_day:
            print("in there but wrong pos")
            word_array[i].status = "wrong pos"
        # if none, then must not be in word
        else:
            print("not there")
            word_array[i].status = "not in word"
        

setup()

# draw loop
while run:
    screen.fill(screen_bg_color)
    # draw the lil boxes
    for r in range(0, 6, 1):
        for c in range(0, 5, 1):
            wordle_array[r][c].show(110 + c*55, 100)
        

    # event handler. basically takes all events
    # its seen, runs through them, and then the 
    # if statements we write filters thru them 
    # based on what we want to happen
    for event in pygame.event.get():
        # print(event)
        # close window --> stop running
        if event.type == pygame.QUIT:
            run = False

        # type in a letter to spell a word
        if event.type == pygame.KEYDOWN:
            # find out which key it was
            print(event.unicode.upper())
            # this turns events/keys you pressed into a string
            key = event.unicode.upper()
            # if the key was "enter/return", check how correct the word is
            # we use event.key because it's not really a character..
            if event.key == pygame.K_RETURN:
                print("enter key pressed !")
                # check if all boxes have a letter
                all_boxes_have_letters = True
                for i in range(len(wordle_array[user_row])):
                    if wordle_array[user_row][i].has_letter == False:
                        all_boxes_have_letters = False
                if all_boxes_have_letters == True:
                    check_word(wordle_array[user_row])
            
            # if the key was "backspace", delete the most recent letter in the word
            if event.key == pygame.K_BACKSPACE:
                print("backspace pressed")
                # traverse through the letters in reverse order
                for i in range(len(wordle_array[user_row])-1, -1, -1):
                    if wordle_array[user_row][i].has_letter == True:
                        wordle_array[user_row][i].has_letter = False
                        wordle_array[user_row][i].letter = None
                        # we only want to adjust the most recent letter of the word (the last written existing letter)
                        # so terminate before the code can get to the previous letters, so it only deletes the most recent
                        break


            # if its not enter, and its some sort of alphabetic letter, fill it into the space
            if key in alphabet:
                for letter in wordle_array[user_row]:
                    if letter.has_letter == False:
                        print("this box doesn't have a letter and ur pressing key " + key)
                        letter.has_letter = True
                        letter.letter = str(key)
                        # we only want to adjust the first letter of the wordle thats free when we press a button, not the rest.
                        # so terminate before the code can loop through the other letters.
                        # breaks out of the for loop
                        break
        
            
            
        

    # update the screen
    pygame.display.flip()

#NOTE: idk what this is for
pygame.quit()

""" for i in range(0, 5, 1):
        # the starting point of 110 is arbitrary, just looked the best
        pygame.draw.rect(screen, no_letter_outline_color, (110 + i*55, 50, sq_dimensions, sq_dimensions), sq_border_width)"""
