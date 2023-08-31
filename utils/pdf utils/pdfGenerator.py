from PIL import Image, ImageDraw, ImageFont
import random
import os
import time
import copy
from multiprocessing import Pool

class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coordinates = (self.x, self.y)

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

class Rectangle:
    def __init__(self, start:Coordinates, end:Coordinates , contents = [] , type = "section"):
        self.start = start
        self.end = end
        self.rectangle = (self.start.x, self.start.y, self.end.x, self.end.y)
        self.contents = contents
        self.type = type

    def getHeight(self):
        return self.end.y - self.start.y
    
    def getWidth(self):
        return self.end.x - self.start.x

    def iscolliding(self, rectangle):
        if self.start.x > rectangle.end.x or self.end.x < rectangle.start.x:
            return False
        if self.start.y > rectangle.end.y or self.end.y < rectangle.start.y:
            return False
        return True

    def __str__(self) -> str:
        return f"Start: {self.start.coordinates} End: {self.end.coordinates}  |  {self.type}"

class TextStyle:
    def __init__(self, font, size, color , background = "white"):
        self.font = font
        self.size = size
        self.color = color
        self.background = background

    def refreshColor(self):
        self.color = "#%06x" % random.randint(0, 0xFFFFFF)

class PDFDetails:
    def __init__(self):
        #Default values for PDF 
        self.DPI = 300
        self.width = 2480
        self.height = 3508
        self.size = (self.width, self.height)

    def setPDFSize(self, width, height):
        self.width = width
        self.height = height
        self.size = (self.width, self.height)

    def pickFont(self):
        fonts_path = os.path.join(r"data\fonts", self.pickFontStyle())
        fonts = os.listdir(fonts_path)
        font = random.choice(fonts)
        font = os.path.join(fonts_path, font)
        return font
    
    def pickFontSize(self,min,max):
        return random.randint(min,max)
    
    def pickFontColor(self):
        #Hexadecimal color code
        return "#%06x" % random.randint(0, 0xFFFFFF)
    
    def pickFontStyle(self):
        styles = ["normal","italic","bold","italic_bold"]
        return random.choice(styles)
    
    def pickFontBackground(self):
        if random.randint(0,100) <= 80:
            return "white"
        return "#%06x" % random.randint(0, 0xFFFFFF)
    
    def splitHeight(self,start:Coordinates,end:Coordinates ,splits= random.randint(2,4)):
        sections = []
        average_height = (end.y - start.y)/splits
        for section in range(splits):
            min_height = int(average_height - average_height*0.3)
            max_height = int(average_height + average_height*0.1)
            height = random.randint(min_height,max_height)
            top = start.y + section*average_height
            bottom = top + height
            area = Rectangle(Coordinates(start.x,top),Coordinates(end.x,bottom),contents=[])
            sections.append(area)
        return sections

    def splitWidth(self,start:Coordinates,end:Coordinates ,splits= random.randint(1,3)):
        sections = []
        average_width = (end.x - start.x)/splits
        for section in range(splits):
            min_width = int(average_width - average_width*0.3)
            max_width = int(average_width + average_width*0.1)
            width = random.randint(min_width,max_width)
            left = start.x + section*average_width
            right = left + width
            area = Rectangle(Coordinates(left,start.y),Coordinates(right,end.y),contents=[])
            sections.append(area)
        return sections

    def pageMainSections(self):
        page = Rectangle(Coordinates(0,0),Coordinates(self.width,self.height))
        if random.randint(0,100)<=70:
            page.contents.extend(self.splitHeight(Coordinates(0,0),Coordinates(self.width,self.height)))
        else:
            temp_list = copy.deepcopy(self.splitHeight(Coordinates(0,0),Coordinates(self.width/2,self.height),splits=random.randint(2,4))) + copy.deepcopy(self.splitHeight(Coordinates(self.width/2,0),Coordinates(self.width,self.height),splits=random.randint(2,4)))
            page.contents = copy.deepcopy(temp_list)
        return page
    
    def getFontHeight(self,font,size,word = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
        left, top, right, bottom = ImageFont.truetype(font,size).getbbox(word)
        return bottom - top
    
    def getFontWidth(self,font,size,word = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
        left, top, right, bottom = ImageFont.truetype(font,size).getbbox(word)
        return right - left

    def setTitle(self,section):
        title_height = self.getFontHeight(self.title.font,self.title.size)
        title_height = int(title_height*random.uniform(1.5,2.0))
        title_width = section.getWidth()
        title_top = section.start.y
        title_left = section.start.x
        title_top_left = Coordinates(title_left,title_top)
        title_bottom = title_top + title_height
        title_right = title_left + title_width
        title_bottom_right = Coordinates(title_right,title_bottom)

        r = Rectangle(title_top_left,title_bottom_right,type="title",contents=[])
        chance = random.randint(0,100)
        if chance <= 20:
            self.drawRectangle(r,self.title.background)
        elif chance <= 40:
            self.drawRectangle(section,self.title.background)

        self.addText(r,self.generateTitle(),self.title)

        return r
    
    def drawRectangle(self,rectangle,color):
        self.draw.rectangle([rectangle.start.coordinates,rectangle.end.coordinates],fill=color)

    def setLabel(self,section):
        label_height = self.getFontHeight(self.label.font,self.label.size)
        label_height = int(label_height*random.uniform(1.5,2.0))
        label_width = section.getWidth()
        label_top = section.start.y
        label_left = section.start.x
        label_top_left = Coordinates(label_left,label_top)
        label_bottom = label_top + label_height
        label_right = label_left + label_width
        label_bottom_right = Coordinates(label_right,label_bottom)

        word = self.generateLabel() + " : ..................."

        r = Rectangle(label_top_left,label_bottom_right,type="text_field",contents=[])
        self.addText(r,word,self.label)

        return r

    def pageElements(self):
        main_page = self.pageMainSections()
        j = 1
        for section in main_page.contents:
            j += 1
            elements = copy.deepcopy(self.splitHeight(section.start,section.end,splits=4))
            elements[0] = copy.deepcopy(self.setTitle(elements[0]))
            i = 1
            counter = 1
            while i < len(elements):
                if random.randint(0,1) == 0:
                    elements[i] = copy.deepcopy(self.setLabel(elements[i]))
                    counter += 1
                else:
                    elements[i].contents = copy.deepcopy(self.splitWidth(elements[i].start,elements[i].end,splits=random.randint(1,3)))
                    for item in range(len(elements[i].contents)):
                        elements[i].contents[item] = copy.deepcopy(self.setLabel(elements[i].contents[item]))
                        counter += 1
                i += 1
            section.contents = copy.deepcopy(elements)
        return main_page

    def chooseRandomeLine(self,file):
        with open(file) as f:
            lines = f.readlines()
        return random.choice(lines).strip()
    
    def generateTitle(self):
        title = self.chooseRandomeLine(r"data\titles.txt")
        return title

    def generateLabel(self):
        label = self.chooseRandomeLine(r"data\text.txt")
        return label    

    def addText(self, rectangle:Rectangle, text, style:TextStyle):
        font = ImageFont.truetype(style.font,style.size)
        width = rectangle.getWidth()
        height = rectangle.getHeight()
        text_width = self.getFontWidth(style.font,style.size,text)
        text_height = self.getFontHeight(style.font,style.size,text)
        text_left = int(random.uniform(rectangle.start.x ,rectangle.start.x + (width - text_width)/2))
        text_top = int(random.uniform(rectangle.start.y,rectangle.start.y + (height - text_height)/2))
        text_coordinates = Coordinates(text_left,text_top)
        self.draw.text(text_coordinates.coordinates,text,font=font,fill=style.color)

    def fillYoloLabels(self, rectangle:Rectangle):
        #this function will loop through the page contents and generate the yolo labels
        #for each rectangle in the page that have a type section go deeper infinitely
        labels = []

        # If the rectangle has type 'section', then we have nested rectangles
        if rectangle.type == "section":
            for content in rectangle.contents:
                labels.extend(copy.deepcopy(self.fillYoloLabels(content)))
        else:
            labels.append(self.generateYoloLabel(rectangle))

        return labels

    def constructPage(self):
        self.pageStyling()
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)
        page = self.pageElements()

        name = time.time_ns()

        yolo_labels = self.fillYoloLabels(page)

        with open("data/labels/" + str(name) + ".txt", "w") as f:
            for label in yolo_labels:
                f.write(label + "\n")

        self.image.save(f"data/images/{name}.png")

    def pageStyling(self):
        self.title = TextStyle(self.pickFont(),self.pickFontSize(80,100),self.pickFontColor(),self.pickFontBackground())
        self.label = TextStyle(self.pickFont(),self.pickFontSize(20,60),self.pickFontColor())
        
    def generateYoloLabel(self, rectangle: Rectangle):
        # YOLO format: <object-class> <x> <y> <width> <height>
        # object-class : Title = 0, Label = 1, Input = 2, Checkbox = 3

        # Get the center of the rectangle
        x = (rectangle.start.x + rectangle.end.x) / 2
        y = (rectangle.start.y + rectangle.end.y) / 2

        # Get the width and height of the rectangle
        width = rectangle.getWidth()
        height = rectangle.getHeight()

        # Normalize the values
        x /= self.width
        y /= self.height
        width /= self.width
        height /= self.height

        # Return the YOLO label

        if rectangle.type == "title":
            return f"0 {x} {y} {width} {height}"
        elif rectangle.type == "text_field":
            return f"1 {x} {y} {width} {height}"
        elif rectangle.type == "input":
            return f"2 {x} {y} {width} {height}"

def main(number):
    print("Generating page " + str(number+1) + "...")
    PDFDetails().constructPage()


if __name__ == "__main__":
    #No Threading
    # for i in range(150):
    #     print("Generating page " + str(i+1) + "...")
    #     PDFDetails().constructPage()

    #Use Multiprocessing to speed up the process
    with Pool(processes=4) as p:
        p.map(main, range(50))
    print("Done")
    
