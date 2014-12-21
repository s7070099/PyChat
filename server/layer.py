'''
Module Name : Command-line Output Draw
Author : Rungsimun Saenprasert
Date : 06/07/2014 17:25
Special Thanks: Chotipat Pornavalai             for creating pre-programing program.
                Naoki Meida                     for teach and assist.
                Sittipong Suwantri              for new algorithm and new idea.
                Sorrawut Kittikeereechaikun     for function line algorithm.
'''
CH = {  ' ' :   ["     ",
                 "     ",
                 "     ",
                 "     ",
                 "     ",
                 "     ",
                 "     "],
        
        'A' :   ["  *  ",
                 " * * ",
                 "*   *",
                 "*****",
                 "*   *",
                 "*   *",
                 "*   *"],
        
        'B' :   ["**** ",
                 "*   *",
                 "*   *",
                 "**** ",
                 "*   *",
                 "*   *",
                 "**** "],
        
        'C' :   [" *** ",
                 "*   *",
                 "*    ",
                 "*    ",
                 "*    ",
                 "*   *",
                 " *** "],
        
        'D' :   ["**** ",
                 "*   *",
                 "*   *",
                 "*   *",
                 "*   *",
                 "*   *",
                 "**** "],

        'E' :   ["*****",
                 "*    ",
                 "*    ",
                 "*****",
                 "*    ",
                 "*    ",
                 "*****"],

        'F' :   ["*****",
                 "*    ",
                 "*    ",
                 "*****",
                 "*    ",
                 "*    ",
                 "*    "],

        'G' :   ["*****",
                 "*    ",
                 "*    ",
                 "*  **",
                 "*   *",
                 "*   *",
                 "*****"],
        
        'H' :   ["*   *",
                 "*   *",
                 "*   *",
                 "*****",
                 "*   *",
                 "*   *",
                 "*   *"],
        
        'I' :   ["*****",
                 "  *  ",
                 "  *  ",
                 "  *  ",
                 "  *  ",
                 "  *  ",
                 "*****"],

        'J' :   ["  ***",
                 "    *",
                 "    *",
                 "    *",
                 "    *",
                 "*   *",
                 " *** "],

        'K' :   ["*   *",
                 "*  * ",
                 "* *  ",
                 "**   ",
                 "* *  ",
                 "*  * ",
                 "*   *"],

        'L' :   ["*    ",
                 "*    ",
                 "*    ",
                 "*    ",
                 "*    ",
                 "*    ",
                 "*****"],

        'M' :   ["** **",
                 "* * *",
                 "* * * ",
                 "* * * ",
                 "* * *",
                 "* * *",
                 "*   *"],

        'N' :   ["*   *",
                 "**  *",
                 "* * *",
                 "* * *",
                 "* * *",
                 "*  **",
                 "*   *"],

        'O' :   ["*****",
                 "*   *",
                 "*   *",
                 "*   *",
                 "*   *",
                 "*   *",
                 "*****"],

        'P' :   ["*****",
                 "*   *",
                 "*   *",
                 "*****",
                 "*    ",
                 "*    ",
                 "*    "],

        'Q' :   ["*****",
                 "*   *",
                 "*   *",
                 "*****",
                 "    *",
                 "    *",
                 "    *"],

        'R' :   ["**** ",
                 "*   *",
                 "*   *",
                 "**** ",
                 "* *  ",
                 "*  * ",
                 "*   *"],

        'S' :   ["*****",
                 "*    ",
                 "*    ",
                 "*****",
                 "    *",
                 "    *",
                 "*****"],

        'T' :   ["*****",
                 "  *  ",
                 "  *  ",
                 "  *  ",
                 "  *  ",
                 "  *  ",
                 "  *  "],

        'U' :   ["*   *",
                 "*   *",
                 "*   *",
                 "*   *",
                 "*   *",
                 "*   *",
                 "*****"],

        'V' :   ["*   *",
                 "*   *",
                 "*   *",
                 "*   *",
                 "*   *",
                 " * * ",
                 "  *  "],

        'W' :   ["*   *",
                 "* * *",
                 "* * *",
                 "* * *",
                 "* * *",
                 "* * *",
                 " * * "],

        'X' :   ["*   *",
                 "*   *",
                 " * *",
                 "  *  ",
                 " * * ",
                 "*   *",
                 "*   *"],

        'Y' :   ["*   *",
                 "*   *",
                 "*   *",
                 " * * ",
                 "  *  ",
                 "  *  ",
                 "  *  "],

        'Z' :   ["*****",
                 "    *",
                 "   * ",
                 "  *  ",
                 " *   ",
                 "*    ",
                 "*****"],

        'Z' :   ["*****",
                 "    *",
                 "   * ",
                 "  *  ",
                 " *   ",
                 "*    ",
                 "*****"],

        '0' :   [" *** ",
                 "*   *",
                 "**  *",
                 "* * *",
                 "*  **",
                 "*   *",
                 " *** "],

        '1' :   [" **  ",
                 "  *  ",
                 "  *  ",
                 "  *  ",
                 "  *  ",
                 "  *  ",
                 " *** "],

        '2' :   ["**** ",
                 "    *",
                 "    *",
                 " *** ",
                 "*    ",
                 "*    ",
                 " ****"],

        '3' :   ["**** ",
                 "    *",
                 "    *",
                 "**** ",
                 "    *",
                 "    *",
                 "**** "],

        '4' :   ["   * ",
                 "  ** ",
                 " * * ",
                 "*  * ",
                 "*****",
                 "   * ",
                 "   * "],

        '5' :   [" ****",
                 "*    ",
                 "*    ",
                 " *** ",
                 "    *",
                 "    *",
                 "**** "],

        '6' :   [" *** ",
                 "*   *",
                 "*    ",
                 "**** ",
                 "*   *",
                 "*   *",
                 " *** "],

        '7' :   ["*****",
                 "    *",
                 "   * ",
                 "  *  ",
                 "  *  ",
                 "  *  ",
                 "  *  "],

        '8' :   [" *** ",
                 "*   *",
                 "*   *",
                 " *** ",
                 "*   *",
                 "*   *",
                 " *** "],

        '9' :   [" *** ",
                 "*   *",
                 "*   *",
                 " ****",
                 "    *",
                 "*   *",
                 " *** "],

        ':' :   ["     ",
                 "  *  ",
                 "     ",
                 "     ",
                 "     ",
                 "  *  ",
                 "     "],

        '-' :   ["     ",
                 "     ",
                 "     ",
                 " *** ",
                 "     ",
                 "     ",
                 "     "],

        '!' :   [" *** ",
                 " *** ",
                 " *** ",
                 " *** ",
                 " *** ",
                 "     ",
                 " *** "],

        '=' :   ["     ",
                 "     ",
                 "*****",
                 "*****",
                 "*****",
                 "     ",
                 "     "],

        '>' :   ["*    ",
                 "**   ",
                 "***  ",
                 "**** ",
                 "***  ",
                 "**   ",
                 "*    "],

        '.' :   ["     ",
                 "     ",
                 "     ",
                 "     ",
                 "     ",
                 " *** ",
                 " *** "],

        '?' :   [" *** ",
                 "*   *",
                 "*   *",
                 "   * ",
                 "  *  ",
                 "     ",
                 "  *  "],
        
        }

class Layer(object):
    '''
    This class use for Command line drawing.
    Variable Type: Layer(int, int, str(Optional))
    Argument Require: Layer(width, height, default_one_charecters(Optional)) default_one_charecters default is white space.

    BUILT-IN VARIABLE:
        width
        height
        screen [Type:list]

    BUILT-IN FUNCTION:
        point(x, y, char(Optional))                         draw point into layer with 1 charecters. (char default is white space)
        line(x1, y2, x2, y2, text)                          draw line into layer with string.
        text(x, y, text, alpha(Optional))                   draw text into layer with string. (alpha default is False)
        rectangle(x1, y1, x2, y2, text, outline(Optional))  draw rectangle into layer with string. (outline default is False)
        circle(x1, y1, x2, y2, text, outline(Optional))     draw circle into layer with string. (outline default is False)
        clear()                                             clear layer.
        draw()                                              draw layer.
    
    FOR EXAMPLE:
        layer1 = Layer(100, 45)
    '''    
    def error(self, error_text):
        '''
        built-in print error message
        '''
        self.err = 1
        print "ERROR in", self.current_func, ":", error_text
    
    def __init__(self, width, height, char=" ", bg="FFFFFF", fg="000000"):
        '''
        init variable into Layer
        Variable Type: Layer(int, int, str)
        Argument Require: Layer(width, height, default_one_charecters)
        '''
        char = str(char)
        self.current_func = "Layer("+str(width)+","+str(height)+',"'+char+'")'
        if self.check_len(char, 1, 1):
            self.width = width
            self.height = height
            self.screen = []
            self.pixel_line = []
            self.screen_color = []
            self.pixel_color_line = []
            self.layer_char = char
            self.layer_bg = bg
            self.layer_fg = fg
            self.err = 0

            i = 0
            while(i <= self.width):
                self.pixel_line.append(char)
                self.pixel_color_line.append([bg, fg])
                i += 1

            i = 0
            while(i <= self.height):
                self.screen.append(list(self.pixel_line))
                self.screen_color.append(list(self.pixel_color_line))
                i += 1

    def check_len(self, char, length_min, length_max):
        '''
        built-in check length of string from length_min and length_max
        '''
        char = len(str(char))
        if (char >= length_min or length_min == -1) and (char <= length_max or length_max == -1):
            return True
        elif char < length_min:
            self.error("characters must be greater than "+str(length_min-1)+".")
        else:
            self.error("characters must not exceed "+str(length_max)+".")
        return False

    def check_area(self, num_x1=0, num_y1=0):
        '''
        built-in 
        '''
        if num_x1 >= 0 and num_x1 <= self.width:
            if num_y1 >= 0 and num_y1 <= self.height:
                return True
            else:
                self.error("y out of layer area. (layer height is "+str(self.height)+")")
        else:
            self.error("x out of layer area. (layer width is "+str(self.width)+")")
        return False

    def point(self, num_x1, num_y1, char="#", bg="FFFFFF", fg="000000"):
        '''
        point(int, int, str)
        Add Point into Layer
        Variable Type: text(int, int, str)
        Argument Require: text(x, y, text)
        '''        
        if self.err == 0:
            char = str(char)
            self.current_func = "point("+str(num_x1)+", "+str(num_y1)+', "'+str(char)+'")'
            if self.check_area(num_x1, num_y1) and self.check_len(char, 1, 1):
                self.screen[num_y1][num_x1] = char
                self.screen_color[num_y1][num_x1] = [bg, fg]

    def line(self, num_x1, num_y1, num_x2, num_y2, text="#", bg="FFFFFF", fg="000000"):
        '''
        Add Line into Layer
        Variable Type: line(int, int, int, int, str)
        Argument Require: line(int, int, int, int, str)
        '''
        from math import sqrt, floor
        
        if num_x1 > num_x2:
            num_x1,num_x2 = num_x2,num_x1
        if num_y1 > num_y2:
            num_y1,num_y2 = num_y2,num_y1
        linear = sqrt(num_x2-num_x1)
        #print linear
        t = 0
        t2 = len(text)
        i = num_y1
        while i <= num_y2:
            j = num_x1
            while j <= num_x2:
                #No Algorithm T_T
                if 1:
                    self.screen[i][j] = text[t]
                    self.screen_color[i][j] = [bg, fg]
                    t += 1
                    if t == t2:
                        t = 0
                j += 1
            i += 1

        slope = ((num_x2-num_x1)*(num_y2-num_y1))**0.5
        start_x = num_x1
        start_y = num_y1
        stop_x = num_x2
        for i in xrange(start_x,start_y+1):
            line = ''
            print_x_at = int(i / slope)
            next_x_at = int(i+1 / slope)
            half_gap = abs(next_x_at - print_x_at) / 2
            for j in xrange(start_x,stop_x+1):
                if print_x_at == j:
                    line += '#'
                else:
                    if j < print_x_at and j + half_gap >= print_x_at:
                        line +='#'
                    elif j > print_x_at and j < next_x_at - half_gap:
                        line +='#'
                    else:
                        print ' '
            print line
        '''
        self.screen[i][num_x2+jx] = text[t]
        t += 1
        if t == t2:
            t = 0
        i += 1
        '''

    def circle(self, num_x1, num_y1, num_x2, num_y2, text="#"):
        '''
        '''


    def text(self, num_x1, num_y1, text="#", alpha=0):
        '''
        Add Text into Layer
        Variable Type: text(int, int, str)
        Argument Require: text(x, y, text)
        '''
        if self.err == 0:
            char = str(text)
            text_len = len(text)
            self.current_func = "text("+str(num_x1)+", "+str(num_y1)+', "'+str(text)+'")'
            if self.check_area(num_x1, num_y1) and self.check_area(num_x1+text_len, num_y1):
                i = 0
                i_max = text_len
                while i < i_max:
                    if alpha == 0 or (alpha == 1 and text[i] != " "):
                        self.screen[num_y1][num_x1+i] = text[i]
                        self.screen_color[num_y1][num_x1+i] = [bg, fg]
                    i += 1

    def text_ex(self, x = 0, y = 0, text = "", char = "#", bg="FFFFFF", fg="000000"):
        t = 0
        t_max = len(text)
        while t < t_max:
            i = 0
            while i < 7:
                c = 0
                while c < 5:
                    if CH[text[t]][i][c] == "*":
                        self.point(x+c, y+i, char, bg, fg)
                    c += 1
                i += 1
            t += 1
            x += 6

    def rectangle(self, num_x1, num_y1, num_x2, num_y2, text="#", bg="FFFFFF", fg="000000", outline = 0):
        '''
        Add Rectangle into Layer
        Variable Type: rectangle(int, int, int, int, str)
        Argument Require: rectangle(x1, y1, x2, y2, charecters)
        '''
        if self.err == 0:
            text = str(text)
            self.current_func = "rectangle("+str(num_x1)+", "+str(num_y1)+", "+str(num_x2)+", "+str(num_y2)+', "'+str(text)+'", '+str(outline)+")"
            if self.check_area(num_x1, num_y1) and self.check_area(num_x2, num_y2) and self.check_len(text, 1, -1):
                if num_x1 > num_x2:
                    num_x1,num_x2 = num_x2,num_x1
                if num_y1 > num_y2:
                    num_y1,num_y2 = num_y2,num_y1
                t = 0
                t2 = len(text)
                i = num_y1
                while i <= num_y2:
                    j = num_x1
                    while j <= num_x2:
                        if outline == 0 or outline == 1 and (i == num_y1 or i == num_y2 or j == num_x1 or j == num_x2):
                            self.screen[i][j] = text[t]
                            self.screen_color[i][j] = [bg, fg]
                            t += 1
                            if t == t2:
                                t = 0
                        j += 1
                    i += 1

    def add_part(self, layer, num_x, num_y):
        i = 0
        while i <= layer.height:
            j = 0
            while j <= layer.width:
                if num_y+i >= 0 and num_y+i <= self.height and num_x+j >= 0 and num_x+j <= self.width:
                    self.screen[num_y+i][num_x+j] = layer.screen[i][j]
                    self.screen_color[num_y+i][num_x+j] = layer.screen_color[i][j]
                j += 1
            i += 1

    def move(self, move_x, move_y):
        '''
        Move Layer
        Variable Type: move(int, int)
        Argument Require: move(x, y)
        '''
        from copy import deepcopy
        screen_old = deepcopy(self.screen)
        screen_color_old = deepcopy(self.screen_color)
        self.clear()

        move_x = -move_x
        move_y = -move_y

        i = 0
        while i <= self.height:
            j = 0
            while j <= self.width:
                if i+move_y >= 0 and i+move_y <= self.height and j+move_x >= 0 and j+move_x <= self.width:
                    self.screen[i][j] = screen_old[i+move_y][j+move_x]
                    self.screen_color[i][j] = screen_color_old[i+move_y][j+move_x]
                j += 1
            i += 1

    def filp(self):
        '''
        Move Layer
        Variable Type: move(int, int)
        Argument Require: move(x, y)
        '''
        from copy import deepcopy
        screen_old = deepcopy(self.screen)
        screen_color_old = deepcopy(self.screen_color)
        self.clear()

        i = 0
        while i <= self.height:
            j = 0
            while j <= self.width:
                self.screen[i][j] = screen_old[self.height-i][self.width-j]
                self.screen_color[i][j] = screen_color_old[self.height-i][self.width-j]
                j += 1
            i += 1

    def clear(self):
        '''
        Clear Layer
        Variable Type: clear()
        Argument Require: clear()
        '''
        if self.err == 0:
            i = 0
            while i <= self.height:
                j = 0
                while j <= self.width:
                    self.screen[i][j] = self.layer_char
                    self.screen_color[i][j] = [self.layer_bg, self.layer_fg]
                    j += 1
                i += 1

    def draw(self):
        '''
        Draw Layer
        Variable Type: draw()
        Argument Require: draw()
        '''
        if self.err == 0:
            i = 0
            render = "";
            while i <= self.height:
                j = 0
                if i != 0: render += "\n"
                while j <= self.width:
                    render += self.screen[i][j]
                    j += 1
                i += 1
            print render

    def getdraw(self):
        '''
        Draw Layer
        Variable Type: draw()
        Argument Require: draw()
        '''
        screenlist = list()
        if self.err == 0:
            i = 0
            render = ""
            bg = ""
            fg = ""
            while i <= self.height:
                j = 0
                if i != 0:
                    screenlist.append(render)
                    render = ""
                    bg = ""
                    fg = ""
                while j <= self.width:
                    if self.screen_color[i][j][0] != bg:
                        bg = self.screen_color[i][j][0]
                        render += "{:%s}" % bg
                    if self.screen_color[i][j][1] != fg:
                        fg = self.screen_color[i][j][1]
                        render += "{%s}" % fg
                    render += self.screen[i][j]
                    j += 1
                i += 1
        return screenlist

'''
    layer1 = Layer(100, 45)
    layer1.rectangle(0, 0, 100, 45, "#", 1)
    layer1.rectangle(2, 2, 33, 8, ".")    
    layer1.rectangle(40, 12, 20, 6, "Boss")
    layer1.rectangle(4, 4, 35, 10, "#", 1)
    layer1.text(50, 20, "Yaranaika ?")
    layer1.point(0, 0, "+")
    layer1.point(0, 45, "+")
    layer1.point(100, 0, "+")
    layer1.point(100, 45, "+")
    layer1.line(20, 20, 30, 40, "#")
    #layer1.line(0, 0, 5, 5, "#")
    #layer1.line(0, 0, 0, 5, "#")
    #layer1.move(-1,5)
    layer1.move(-5,0)
    layer1.draw()
'''
