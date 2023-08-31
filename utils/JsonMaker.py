#Create a gui that will show a pdf file and allow the user to select a region of interest
#The user will name that region and will be added to a list of regions json file [name, x, y, width, height]

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import json
import cv2
import pdf2image

class JsonMaker:
    def __init__(self, app):
        self.app = app
        self.app.title("Json Maker")
        self.app.geometry("800x600")
        self.app.resizable(False, False)

        #Canvas to display the pdf and don't allow click events on the canvas
        self.canvas = tk.Canvas(self.app, width=600, height=600)
        self.canvas.pack(side=tk.LEFT)
        #Disable the click events on the canvas
        self.canvas.bind("<Button-1>", lambda event: "break")
        
        
        #Frame to hold the buttons
        self.frame = tk.Frame(self.app, width=200, height=600)
        self.frame.pack(side=tk.RIGHT)

        #Label to show the selected pdf file
        self.pdfLabel = tk.Label(self.frame, text="No PDF Selected")
        self.pdfLabel.pack(side=tk.TOP, pady=10)

        #Button to select the pdf file
        self.selectPdfButton = tk.Button(self.frame, text="Select PDF", command=self.selectPdf)
        self.selectPdfButton.pack(side=tk.TOP, pady=10)

        #Label to show the page currently being displayed
        self.pageLabel = tk.Label(self.frame, text="Page: 0")
        self.pageLabel.pack(side=tk.TOP, pady=10)

        #Button to go to the previous page
        self.previousPageButton = tk.Button(self.frame, text="Previous Page", command=self.previousPage)
        self.previousPageButton.pack(side=tk.TOP, pady=10)

        #Button to go to the next page
        self.nextPageButton = tk.Button(self.frame, text="Next Page", command=self.nextPage)
        self.nextPageButton.pack(side=tk.TOP, pady=10)

        #Button to select the region of interest
        self.selectRegionButton = tk.Button(self.frame, text="Select Region", command=self.selectRegion)
        self.selectRegionButton.pack(side=tk.TOP, pady=10)

        #Entry to enter the name of the region of interest
        self.regionNameEntry = tk.Entry(self.frame)
        self.regionNameEntry.pack(side=tk.TOP, pady=10)

        #Button to cancel the selection of the region of interest
        self.cancelButton = tk.Button(self.frame, text="Cancel", command=self.cancel)
        self.cancelButton.pack(side=tk.TOP, pady=10)

        #Button to save the regions of interest
        self.saveRegionsButton = tk.Button(self.frame, text="Save Regions", command=self.saveRegions)
        self.saveRegionsButton.pack(side=tk.TOP, pady=10)

        #Button to exit the application
        self.exitButton = tk.Button(self.frame, text="Exit", command=self.exit)
        self.exitButton.pack(side=tk.TOP, pady=10)

        #Variables to hold the pdf file ,page number and the regions of interest
        self.pdfFile = None
        self.currentPage = 0
        self.regions = []

        #Disable all buttons except the select pdf button
        self.disableButtons()
        self.selectPdfButton.config(state=tk.NORMAL)

        #Start the application
        self.app.mainloop()

    #Function to select the pdf file
    def selectPdf(self):
        self.pdfFile = filedialog.askopenfilename(initialdir="/", title="Select PDF", filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
        #Convert pdf to images and split it into pages
        self.pages = pdf2image.convert_from_path(self.pdfFile)
        #Fit the images to the canvas
        self.pages = [page.resize((600, 600)) for page in self.pages]
        self.pdfLabel.config(text=self.pdfFile)
        self.pageLabel.config(text="Page: " + str(self.currentPage + 1) + "/" + str(len(self.pages)))
        #Enable the buttons
        self.enableButtons()

        #Display the first page
        self.displayPage()

    #Function to display the page
    def displayPage(self):
        #Convert the image to a tkinter image
        self.page = ImageTk.PhotoImage(self.pages[self.currentPage])
        #Display the image
        self.canvas.create_image(0, 0, image=self.page, anchor=tk.NW)
        #Display the regions of interest
        self.displayRegions()

    #Function to display the regions of interest
    def displayRegions(self):
        #Delete all the regions of interest
        self.canvas.delete("region")
        #Display the regions of interest
        for page in self.regions:
           for region in page:
               self.canvas.create_rectangle(region["x"], region["y"], region["x"] + region["width"], region["y"] + region["height"], outline="red", tags="region")


    #Function to go to the previous page
    def previousPage(self):
        #Check if the current page is not the first page
        if self.currentPage > 0:
            self.currentPage -= 1
            self.pageLabel.config(text="Page: " + str(self.currentPage + 1) + "/" + str(len(self.pages)))
            self.displayPage()
            self.canvas.delete("all")

    #Function to go to the next page
    def nextPage(self):
        #Check if the current page is not the last page
        if self.currentPage < len(self.pages) - 1:
            self.currentPage += 1
            self.pageLabel.config(text="Page: " + str(self.currentPage + 1) + "/" + str(len(self.pages)))
            self.displayPage()
            self.canvas.delete("all")

    def loadCurrentPageRegions(self):
        #Check if the current page has regions of interest
        if len(self.regions) > self.currentPage:
            self.currentPageRegions = self.regions[self.currentPage]
            for region in self.currentPageRegions:
                self.canvas.create_rectangle(region["x"], region["y"], region["x"] + region["width"], region["y"] + region["height"], outline="red", tags="region")
        else:
            self.currentPageRegions = []

    #Function to select the region of interest will allow the user to click on the canvas twice then re dsiable it
    def selectRegion(self):
        self.click = 0
        #Disable the buttons
        self.disableButtons()
        #Enable cancel button
        self.cancelButton.config(state=tk.NORMAL)
        #Bind the click event to the canvas
        self.canvas.bind("<Button-1>", self.clickEvent)

    #Function to handle the click event
    def clickEvent(self, event):
        #Check if the click event is the first click
        if self.click == 0:
            #Set the x and y coordinates
            self.x = event.x
            self.y = event.y
            #Increment the click
            self.click += 1
        #Check if the click event is the second click
        elif self.click == 1:
            #Set the width and height
            self.width = event.x - self.x
            self.height = event.y - self.y
            #Increment the click
            self.click += 1
            #Disable the canvas
            self.canvas.unbind("<Button-1>")
            #Enable the buttons
            self.enableButtons()

        #Draw the rectangle
        self.canvas.create_rectangle(self.x, self.y, event.x, event.y, outline="red", tags="region")

        #Check if the array for the page exists
        if len(self.regions) < self.currentPage + 1:
            self.regions.append([])

        #Add the region to the list of regions
        self.regions[self.currentPage].append({"x": self.x, "y": self.y, "width": self.width, "height": self.height, "lines": self.regionNameEntry.get()})
        #Clear the entry
        self.regionNameEntry.delete(0, tk.END)

    #Function to cancel the selection of the region of interest
    def cancel(self):
        #Enable the buttons
        self.enableButtons()
        #Disable the cancel button
        self.cancelButton.config(state=tk.DISABLED)
        #Clear the entry
        self.regionNameEntry.delete(0, tk.END)
        #Unbind the click event
        self.canvas.unbind("<Button-1>")

    #Function to save the regions of interest
    def saveRegions(self):
        #Get the name of the file
        fileName = filedialog.asksaveasfilename(initialdir="/", title="Save File", filetypes=(("json files", "*.json"), ("all files", "*.*")))
        #Check if the file name is not empty
        if fileName:
            #Open the file
            with open(fileName, "w") as file:
                #Dump the regions of interest
                json.dump(self.regions, file, indent=4)

    #Function to exit the application
    def exit(self):
        self.app.destroy()

    #Function to disable all buttons except the select pdf button
    def disableButtons(self):
        self.previousPageButton.config(state=tk.DISABLED)
        self.nextPageButton.config(state=tk.DISABLED)
        self.selectRegionButton.config(state=tk.DISABLED)
        self.saveRegionsButton.config(state=tk.DISABLED)

    #Function to enable all buttons
    def enableButtons(self):
        self.previousPageButton.config(state=tk.NORMAL)
        self.nextPageButton.config(state=tk.NORMAL)
        self.selectRegionButton.config(state=tk.NORMAL)
        self.saveRegionsButton.config(state=tk.NORMAL)

#Main function
def main():
    root = tk.Tk()
    JsonMaker(root)

if __name__ == "__main__":
    main()