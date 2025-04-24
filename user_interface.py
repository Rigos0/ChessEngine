from search import *
import pygame
import os

pygame.init()
u_search = U_search()
monte = Monte_Carlo_Search()

white = (240, 217, 181)
brown = (181, 136, 99)


class Convert:
    def __init__(self):
        self.squares_to_x_y = {}

    # create a dictionary in the form {square: (x_pos_y_pos),...}
    def initialise_square_positions(self):
        size = 80
        current_square = 27
        x_pos = 100 + 2
        y_pos = 120+3+7*80

        for i in range(8):
            for x in range(8):
                self.squares_to_x_y[current_square] = (x_pos + x * size, y_pos - size*i)
                current_square += 1
            current_square += 4
            x_pos = 100 + 2

    # Convert nested list with possible moves to a dictionary form.
    # This dictionary will be used to show possible moves when
    # a square is selected.
    @staticmethod
    def nested_list_to_dictionary(nested_list_of_moves):
        moves_dict = {}
        for x in nested_list_of_moves:
            if x[0] in moves_dict.keys():
                moves_dict[x[0]].append(x[1])
            else:
                moves_dict[x[0]] = [x[1]]
        return moves_dict


# takes colour of the square, position of the square ("top_left") and number of the square
# every square is 80*80 pixels
class Square:
    def __init__(self, colour, top_left, number):
        self.colour = colour
        self.top_left = top_left
        self.number = number
        self.size = 80
        self.selected = False

    # draw a single square
    def draw_square(self, surface):
        pygame.draw.rect(surface, self.colour, [self.top_left[0],
                                                self.top_left[1], self.size, self.size])

    # If a piece is selected and it is possible to move it, then highlight possible
    # next squares.
    def draw_selected(self):
        if self.selected:
            pygame.draw.rect(main.surface, (93, 87, 85), [self.top_left[0], self.top_left[1], 80, 80], 5)


# Evaluation bar always shows evaluation of current position on the
# board. The evaluation is fetched from the neural network model.
class EvaluationBar:
    def __init__(self):
        # There is no need to load the model again.
        self.model = u_search.model
        # colours
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (155, 0, 0)
        self.yellow = (192, 183, 0)
        self.brown = brown
        self.prediction = None

    # Draw the evaluation bar. This function is called each cycle
    # in the main loop.
    def draw_bar(self, surface, side_to_move):
        # light brown border
        pygame.draw.rect(surface, self.brown, [52, 127, 30, 626])
        # fill the space with white
        pygame.draw.rect(surface, self.white, [55, 130, 24, 620])
        # if the prediction wasn't fetched from the model this cycle yet
        if not self.prediction:
            # get numpy array of current position
            position_matrix = convert_to_matrix(side_to_move)
            position_array = np.array([position_matrix])
            prediction = self.model.predict(position_array)
            self.prediction = float(prediction)
        # if prediction is higher than 1, the bar is fully white
        if 1 < self.prediction:
            self.prediction = 1
        # if prediction is lower than 0, the bar is fully black
        if 0 > self.prediction:
            self.prediction = 0
        # draw black rectangle on top the white
        # height of the black rectangle is based on the prediction
        pygame.draw.rect(surface, self.black, [55, 130, 24, 620 * (1-self.prediction)])
        # draw a red line in the middle of the bar
        pygame.draw.line(surface, self.red, (55, 440), (78, 440), 3)
        # draw yellow lines on the bar
        y_pos = 378
        y_pos_change = 62
        for x in range(2):
            for i in range(4):
                pygame.draw.line(surface, self.yellow, (55, y_pos), (78, y_pos), 2)
                y_pos -= y_pos_change
            y_pos = 502
            y_pos_change = -62


# This class draws the chessboard and all pieces.
class Board:
    def __init__(self):
        self.squares = [] # holds 64 instances of the class "Square"
        self.rows = 8
        self.ranks = 8
        self.x_pos = 20
        self.y_pos = 40
        self.size = 80
        self.brown = brown
        self.white = white
        # load images of the pieces and save them as attributes of this class
        self.pieces_names = ("knight3", "pawn3", "bishop3", "rook3", "queen3", "king3")
        self.image_path = os.path.dirname(os.path.abspath(__file__)) + "\\images\\"
        for name in self.pieces_names:
            setattr(self, name, self.load_image(self.image_path + "white{}.png".format(name)))
            setattr(self, "black" + name, self.load_image(self.image_path + "black{}.png".format(name)))

    # This function is called at the start of every run
    # to create a list of instances of the class "Square".
    def create_squares(self):
        size = 80 # each square is 80*80 pixels
        current_square = 27 # we start on the square with number 27 ("a1")
        x_pos = 100 # Initial x position
        y_pos = 120 + 7 * 80 # Initial y position

        # Calculate position and colour of each square and save it to self.squares
        for i in range(8): # for every rank
            if i % 2 == 0: # find out if current rank is odd or even
                coefficient = 0 # even
            else:
                coefficient = 1 # odd
            for x in range(8): # for every square in the row
                # calculate position of the square
                position = (x_pos + x * size, y_pos - size * i)
                # find colour of the square
                if x % 2 == coefficient:
                    colour = self.brown
                else:
                    colour = self.white
                # create an instance with the calculated properties
                square = Square(colour, position, current_square)
                # Append the instance in self.squares
                self.squares.append(square)
                current_square += 1 # increase notation of the square by one
            # when a row is finished, increase notation of the square by 4
            # because there are four empty "border" squares
            current_square += 4
            x_pos = 100

    # Loop over every instance of the class "Square" and draw it
    # based on its properties
    def draw_board(self, surface):
        for square in self.squares:
            square.draw_square(surface)

    def draw_pieces(self, surface, white_pieces_positions, black_pieces_positions):
        # Adjust these x, y pairs to center a piece type on the square
        offsets = ((0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, -2))
        w_pieces = (self.pawn3, self.knight3, self.bishop3, self.rook3, self.queen3, self.king3)
        b_pieces = (self.blackpawn3, self.blackknight3, self.blackbishop3,
                    self.blackrook3, self.blackqueen3, self.blackking3)
        # white_pieces_positions is passed to this function
        # it is a list taken from the "Generator" class, which holds
        # positions of all pieces
        pieces = ((w_pieces, white_pieces_positions), (b_pieces, black_pieces_positions))
        draw_last = False
        for i, colour in enumerate(pieces): # for white pieces and then for black pieces
            for index, piece_type in enumerate(colour[1]): # for positions of a piece type
                for square in piece_type: # for every position of every piece
                    # get x, y position of the square the piece is on
                    pos = convert.squares_to_x_y.get(square)
                    # Drag the piece
                    # If the piece is held down by the mouse, draw it based on
                    # position of the mouse.
                    if square == click.piece_selected:
                        x, y = pygame.mouse.get_pos()
                        pos = (x - 40, y - 40)
                        draw_last = [pos, i, index]
                    # Otherwise, draw the piece based on its actual location
                    else:
                        pos = (pos[0] + offsets[index][0], pos[1] + offsets[index][1])
                        surface.blit(pieces[i][0][index], pos)
        # If the piece is dragged, draw it on top of other pieces, so we don't
        # drag it underneath other pieces.
        if draw_last:
            surface.blit(pieces[draw_last[1]][0][draw_last[2]], draw_last[0])

    # Draw a small circle on the right of the chessboard to indicate
    # if it is white or black to move.
    @staticmethod
    def side_to_move_circle(surface, side_to_move):
        if side_to_move == "white":
            pygame.draw.circle(surface, (255, 255, 255), (760, 740), 12)
        else:
            pygame.draw.circle(surface, brown, (760, 140), 12)

    @staticmethod
    def load_image(filename):
        return pygame.image.load(filename)


# Buttons are used in the menu to select different opponents, change game
# mode and to close and open the menu
class Button:
    def __init__(self, pos, size, on_click_change):
        self.size = size
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.held_down = False
        # Each button changes one variable. If there is any logic like
        # only one of three buttons can be selected, it is not stored
        # directly in this class. The variable should be stored in a list
        # so we can make use of the Python connected lists.
        self.on_click_change = on_click_change
        self.body_colour = (225, 225, 225)
        self.border_colour = (173, 173, 173)
        self.text_colour = (0, 0, 0)

    # Check if the button is held down.
    def on_click(self, x, y):
        if self.x_pos < x < self.x_pos + self.size[0] and self.y_pos < y < self.y_pos + self.size[1]:
            self.held_down = True

    # The button changes the variable only if it is clicked on and then the mouse button is let go
    # on the position of the button.
    def on_mouse_up(self, x, y):
        # if mouse up on top of this button
        if self.x_pos < x < self.x_pos + self.size[0] and self.y_pos < y < self.y_pos + self.size[1]:
            # if the button was clicked on
            if self.held_down:
                # change it's variable
                if self.on_click_change[0]:
                    self.on_click_change[0] = False
                else:
                    self.on_click_change[0] = True
        # The mouse button is up, therefore the button is no longer held down
        self.held_down = False


# Text buttons
# This class inherits properties of the parent class Button and takes
# two additional properties - relative offset (for floating buttons) and caption.
class TextButton(Button):
    def __init__(self, pos, size, on_click_change, relative_offset, caption, text_offset):
        super().__init__(pos, size, on_click_change)
        self.caption = caption
        # For floating buttons in the menu
        self.x_difference = relative_offset[0]
        self.y_difference = relative_offset[1]
        self.x_pos = pos[0] + self.x_difference
        self.y_pos = pos[1] + self.y_difference
        self.text_offset = text_offset
    # draw the button
    def draw_button(self, surface):
        # make the button darker if it is held down by the mouse button
        if self.held_down:
            body_colour = (190, 190, 190)
            border_colour = (50, 50, 50)
        else:
            body_colour = self.body_colour
            border_colour = self.border_colour
        # draw border of the button
        pygame.draw.rect(surface, border_colour, [self.x_pos, self.y_pos, self.size[0], self.size[1]])
        # fill the inside of the button
        pygame.draw.rect(surface, body_colour, [self.x_pos + 1, self.y_pos + 1, self.size[0] - 2, self.size[1] - 2])
        # draw text on the button
        button_text = pygame.font.SysFont('Calibri', 15, False).render(self.caption, True, self.text_colour)
        surface.blit(button_text, (self.x_pos + self.text_offset[0], self.y_pos + self.text_offset[1]))


# Buttons for selecting the game mode in the menu.
class ImageButton(Button):
    def __init__(self, pos, size, on_click_change, difference, caption, colour, offset):
        super().__init__(pos, size, on_click_change)
        self.x_difference = difference[0]
        self.y_difference = difference[1]
        self.x_pos = pos[0] + self.x_difference
        self.y_pos = pos[1] + self.y_difference
        self.caption = caption
        self.colour = colour
        self.x_text_offset = offset[0]
        self.y_text_offset = offset[1]


# draw the button
    def draw_button(self, surface):
        body_colour = self.colour
        # if the button is selected
        if self.on_click_change[0]:
            border_colour = (30, 30, 30)
            border = 3
        else:
            border_colour = (50, 50, 50)
            border = 1

        pygame.draw.rect(surface, border_colour, [self.x_pos, self.y_pos, self.size[0], self.size[1]])
        pygame.draw.rect(surface, body_colour, [self.x_pos + border, self.y_pos + border,
                                                self.size[0] - 2*border, self.size[1] - 2*border])
        # draw text on the button
        button_text = pygame.font.SysFont('Calibri', 15, False).render(self.caption, True, self.text_colour)
        surface.blit(button_text, (self.x_pos + self.x_text_offset, self.y_pos + self.y_text_offset))

    # The four game-mode buttons have different selection logic than the original button class
    # Only one of the four buttons can be selected
    # This is done by rewriting the on_mouse_up function for this class
    def on_mouse_up(self, x, y):
        if self.x_pos < x < self.x_pos + self.size[0] and self.y_pos < y < self.y_pos + self.size[1]:
            if self.held_down:
                for option in menu.engine_options:  # for every option set it to False
                    option[0] = False
                # set this button to variable to True
                if self.on_click_change[0]:
                    self.on_click_change[0] = False
                else:
                    self.on_click_change[0] = True
        self.held_down = False


# the Menu is created entirely in pygame, but behaves like another window
class Menu:
    def __init__(self):
        self.menu_colour = (241, 241, 241)
        self.header_blue = (43, 87, 154)
        self.buttons = [] # floating buttons
        self.static_buttons = [] # static buttons outside the floating menu
        self.game_mode_buttons = [] # image buttons
        self.drag = False
        self.pos = (140, 260) # current position of the menu
        # these bool variables have to be in a list because we want to
        # use change them using Python connected lists
        self.monte_carlo = [False]
        self.minimax = [False]
        self.u_search = [True]
        self.analyse = [False]
        self.engine_options = [self.monte_carlo, self.minimax, self.u_search, self.analyse]

    # Create instances of the buttons and save them to appropriate lists
    def create_buttons(self):
        # OK button for closing the floating menu
        button = TextButton((self.pos[0], self.pos[1]), (80, 26), main.menu, (240, 270), "OK", (30, 6))
        self.buttons.append(button)
        # button to open the menu
        static_menu_button = TextButton((900, 120), (100, 30), main.menu, (0, 0), "Menu", (30, 7))
        x_diff = 40

        # play option buttons
        engine_options = (menu.monte_carlo, menu.minimax, menu.u_search)
        names = ["Carlos", "Matt", "Alex"]
        colours = ((97, 191, 50), (210, 219, 35), (207, 121, 17))
        center_text = ((12, 25), (16, 25), (18, 25))
        # create button for every engine
        for i, option in enumerate(engine_options):
            engine_button = ImageButton((self.pos[0], self.pos[1]), (66, 66), option, (x_diff, 54), names[i]
                                        , colours[i], center_text[i])
            x_diff += 76
            self.game_mode_buttons.append(engine_button)

        # analyse button
        analyse_button = ImageButton((self.pos[0], self.pos[1]), (66, 66), menu.analyse, (380, 54), "Analyse",
                                     (186, 183, 175), (9, 25))
        self.game_mode_buttons.append(analyse_button)

        self.static_buttons.append(static_menu_button)

        reset_button = TextButton((900, 730), (100, 30), main.reset, (0, 0), "New game", (20, 7))
        self.static_buttons.append(reset_button)


    # draw the floating menu
    def draw_menu(self, surface):
        # draw the blue header
        pygame.draw.rect(surface, self.header_blue, [self.pos[0] - 1, self.pos[1]-1, 562, 302])
        # fill the menu
        pygame.draw.rect(surface, self.menu_colour, [self.pos[0], self.pos[1], 560, 300])

        # White rectangles under different menu options
        # rect under "play" options
        pygame.draw.rect(surface, (255, 255, 255), [self.pos[0] + 5, self.pos[1]+35, 280, 120])
        # "play" text
        opponent_text = pygame.font.SysFont('Calibri', 13).render("Play", True, (0, 0, 0))
        surface.blit(opponent_text, (self.pos[0] + 134, self.pos[1] + 38))

        # rect under "analyse" option
        pygame.draw.rect(surface, (255, 255, 255), [self.pos[0] + 290, self.pos[1]+35, 265, 120])

        # rect under description
        pygame.draw.rect(surface, (255, 255, 255), [self.pos[0] + 5, self.pos[1]+160, 550, 100])

        self.draw_engine_description(surface)

        # blue header
        pygame.draw.rect(surface, self.header_blue, [self.pos[0], self.pos[1], 560, 30])
        menu_name = pygame.font.SysFont('Calibri', 20).render("Menu", True, self.menu_colour)
        surface.blit(menu_name, (self.pos[0]+10, self.pos[1]+6))

        for button in self.buttons + self.game_mode_buttons:
            button.draw_button(surface)

    # if we click on the header, change self.drag to True
    def on_click(self, x, y):
        if not self.drag:
            if self.pos[0] < x < self.pos[0] + 560 and self.pos[1] < y < self.pos[1] + 30:
                self.drag = True
                self.initial_pos = (x - self.pos[0], y - self.pos[1])

    # move around the floating menu based on mouse position
    def move(self, x, y):
        # calculate the position based on the position of the mouse in
        # respect to the menu
        self.pos = (x - self.initial_pos[0], y - self.initial_pos[1])
        # change the position of the menu
        for button in self.buttons + self.game_mode_buttons:
            button.x_pos = x - self.initial_pos[0] + button.x_difference
            button.y_pos = y - self.initial_pos[1] + button.y_difference

    # descriptions of the playing modes
    def draw_engine_description(self, surface):
        # dictionary with all descriptions
        descriptions = {0: "Carlos is a chess kibitzer from Monte Carlo. "
                           "He is a casual player and often misses tactics.",
                        1: "Matt is a mathematician and it also influences his playing style. He calculates every ",
                        2: "Alex is a robot that has taught himself how to play chess. He can play strong positional",
                        3: "This mode enables you to move pieces for both sides. Check the evaluation bar to see how",
                        4: "possible variation a few moves ahead!",
                        5: "chess, but it sometimes looks like he forgot to study tactics and endgames.",
                        6: "promising is the position!"}
        # find if any engine is selected
        description = False
        for index, i in enumerate(menu.engine_options):
            # find out which one is selected
            if i[0]:
                description = descriptions.get(index)
        # if not engine selected, we are in the mode "analyse"
        if not description:
            description = descriptions.get(3)

        second_line_text = False
        # For descriptions of Minimax, U-search and Analyse, we need two lines of text.
        if description.startswith("Matt"):
            second_line_text = descriptions.get(4)
        elif description.startswith("Alex"):
            second_line_text = descriptions.get(5)
        elif description.startswith("This"):
            second_line_text = descriptions.get(6)

        # Render first line of description.
        description_text = pygame.font.SysFont('Calibri', 14).render(description, True, (0, 0, 0))
        surface.blit(description_text, (self.pos[0] + 22, self.pos[1] + 170))
        # Render second line of description.
        if second_line_text:
            second_line = pygame.font.SysFont('Calibri', 14).render(second_line_text, True, (0, 0, 0))
            surface.blit(second_line, (self.pos[0] + 22, self.pos[1] + 185))

    def end_of_the_game_window(self, surface, checkmate, side_to_move):
        pygame.draw.rect(surface, self.header_blue, [289, 399, 262, 82])
        pygame.draw.rect(surface, (255, 255, 255), [290, 400, 260, 80])
        if checkmate:
            first_line = pygame.font.SysFont('Calibri', 24, bold=False).render("checkmate", True, (0, 0, 0))
            if side_to_move == "white":
                second_line = pygame.font.SysFont('Calibri', 24, bold=False).render("0-1, black wins", True, (0, 0, 0))

            else:
                second_line = pygame.font.SysFont('Calibri', 24, bold=False).render("1-0, white wins", True, (0, 0, 0))

        else:
            first_line = pygame.font.SysFont('Calibri', 24, bold=False).render("stalemate", True, (0, 0, 0))
            second_line = pygame.font.SysFont('Calibri', 24, bold=False).render("0.5-0.5, draw", True, (0, 0, 0))
        # center stalemate text
        if not checkmate:
            surface.blit(first_line, (368, 414))
            surface.blit(second_line, (350, 442))
        else:
            surface.blit(first_line, (358, 414))
            surface.blit(second_line, (340, 442))


# Selecting pieces by mouse click
class ClickLogic:
    def __init__(self):
        self.initial_square = None
        self.piece_selected = None

    # takes x and y positions of the click and dictionary with possible moves
    def mouse_click(self, x, y, moves_dict):
        # for every square
        for square in board.squares:
            square_x_pos = square.top_left[0]
            square_y_pos = square.top_left[1]
            # if the we click on this square
            if square_x_pos < x < square_x_pos + 80 and square_y_pos < y < square_y_pos + 80:
                # if the square is already highlighted
                if square.selected:
                    # return the move
                    return [self.initial_square, square.number]
                # if the square isn't selected, select it
                self.initial_square = square.number
        # rest all highlighted squares
        for square in board.squares:
            square.selected = False

        # find squares to highlight
        possible_destinations = moves_dict.get(self.initial_square)
        if possible_destinations:  # if there are any possible moves starting at this square
            self.piece_selected = self.initial_square # there is a piece on the initial square
            for square in board.squares:  # for every square
                # if the square is in the possible destinations
                if square.number in possible_destinations:
                    square.selected = True  # select it


class Main:
    def __init__(self):
        self.surface = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
        # initial selected engine
        self.search = u_search.assumption_search
        self.engines = [monte.search, minimax.search, u_search.assumption_search]
        self.menu = [False]  # start with the menu hidden
        self.checkmate = False
        self.stalemate = False
        self.reset = [False]

    # This function is called each turn.
    # After a move is made, it returns and it is called again with the other
    # side to move as a parameter.
    def run(self, side_to_move):
        # create possible moves for current side
        moves = create_moves(side_to_move)
        # convert the nested list of moves to dictionary
        moves_dictionary = convert.nested_list_to_dictionary(moves)
        if not moves:
            self.end_of_the_game(side_to_move)

        # the current position has not been evaluated by the neural network yet
        eval_bar.prediction = None
        # the main loop
        # break when a move is made
        while True:
            # stop the program after a click on the quit button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # resize the pygame window
                if event.type == pygame.VIDEORESIZE:
                    self.surface = pygame.display.set_mode((event.w, event.w), pygame.RESIZABLE)

                # if the mode is not analyse and the floating menu is closed
                if not menu.analyse[0] and not self.menu[0]:
                    if side_to_move == "black":
                        # draw the board, pieces etc.
                        self.draw_everything(side_to_move)
                        # for every engine option
                        for index, i in enumerate(menu.engine_options):
                            # find out which one is selected
                            if i[0]:
                                self.search = self.engines[index]
                        # run the search to find the best move
                        best_move = self.search()
                        # play the best move
                        generator.make_a_move(best_move)
                        return

                # mouse button down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()  # get position of the mouse
                    # if the floating menu is open
                    if self.menu[0]:
                        # check if we clicked on a button
                        for button in menu.buttons + menu.game_mode_buttons:
                            button.on_click(x, y)
                        # check if we clicked on the menu header to move it
                        menu.on_click(x, y)
                    # otherwise, check if clicked on a static button outside of the floating menu
                    else:
                        for button in menu.static_buttons:
                            button.on_click(x, y)
                        # call the piece selection function
                        # the function returns true if a move was completed by the mouse click
                        stop = self.piece_selecting(x, y, moves_dictionary)
                        if stop:
                            return

                # on mouse button up
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # if the floating menu is open
                    if self.menu[0]:
                        # call the on_mouse_up function of every button to find
                        # out if the button should change it's variable
                        for button in menu.buttons + menu.game_mode_buttons:
                            button.on_mouse_up(x, y)
                        menu.drag = False  # the menu is no longer dragged
                    # otherwise do the same thing for buttons outside the floating menu
                    else:
                        for button in menu.static_buttons:
                            button.on_mouse_up(x, y)
                        stop = self.piece_selecting(x, y, moves_dictionary)
                        click.piece_selected = None
                        if stop:
                            return

                if self.reset[0]:  # if reset
                    self.reset_game()
                    return True

            # draw everything on the screen
            self.draw_everything(side_to_move)

    @staticmethod
    def piece_selecting(x, y, moves_dictionary):
        # get a move that was completed by the click
        move = click.mouse_click(x, y, moves_dictionary)
        if move:  # if we completed a move
            generator.make_a_move(move)  # play the move on the board
            click.piece_selected = None
            # set all squares to "not selected"
            for square in board.squares:
                square.selected = False
            return True

    # b;it everything on the screen
    def draw_everything(self, side_to_move):
        self.surface.fill((48, 32, 24)) # background colour
        # draw side to move circle
        board.side_to_move_circle(self.surface, side_to_move)
        # draw the chessboard
        board.draw_board(self.surface)
        for square_draw in board.squares:
            square_draw.draw_selected()
        # draw the evaluation bar
        eval_bar.draw_bar(self.surface, side_to_move)
        # draw all pieces
        board.draw_pieces(self.surface, generator.white_pieces, generator.black_pieces)
        # draw all static buttons
        for static_button in menu.static_buttons:
            static_button.draw_button(self.surface)

        if self.checkmate or self.stalemate:
            menu.end_of_the_game_window(self.surface, self.checkmate, side_to_move)

        # if the menu is open, draw it
        if self.menu[0]:
            menu.draw_menu(self.surface)
            # if the menu is dragged, change it's position base on
            # the mouse pointer position
            if menu.drag:
                x, y = pygame.mouse.get_pos()
                menu.move(x, y)
        pygame.display.update()  # update pygame window

    def end_of_the_game(self, side_to_move):
        for engine in menu.engine_options:
            engine[0] = False
        menu.analyse[0] = True
        enemy_attacks = []
        enemy_side = enemy_colour(side_to_move)
        # generate squares that are attacked by black sliding pieces
        for move in generator.generate_moves(enemy_side, generate_only="only_sliding"):
            enemy_attacks.append(move[-1])
        # generate squares that are attacked by every other black piece
        for move in generator.generate_moves(enemy_side, generate_only="other_attacks"):
            enemy_attacks.append(move[-1])
        generator.set_up_attributes(side_to_move)
        checkmate = generator.detect_check(enemy_attacks)
        if checkmate:
            self.checkmate = True
        else:
            self.stalemate = True

    def reset_game(self):
        generator.reset_board()
        self.menu[0] = False
        self.reset[0] = False
        self.checkmate, self.stalemate = False, False


# instantiate all needed classes
minimax = ModifiedMinimax()
convert = Convert()
board = Board()
# create squares
convert.initialise_square_positions()
board.create_squares()
click = ClickLogic()
eval_bar = EvaluationBar()
main = Main()
menu = Menu()
# create buttons
menu.create_buttons()


# Run the program.
if __name__ == "__main__":
    while True:
        reset = main.run("white")
        if reset:
            continue
        main.run("black")

