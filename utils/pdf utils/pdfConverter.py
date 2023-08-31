#This tool will take a folder of pdf files and will convert them to images and plsit them by page
import pdf2image
import os
import argparse


#Function to convert pdf to images
def convertPDF2IMG(file,output_folder):
    file_name = os.path.splitext(os.path.basename(file))[0]
    #Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    #Split the pdf into pages
    pages = pdf2image.convert_from_path(file)
    #Save the pages
    for i in range(len(pages)):
        pages[i].save(output_folder + file_name+"_page_"+str(i) + ".png", "PNG")

#Function to convert a folder of pdf files to images
def convertFolderPDF2IMG(folder,output_folder):
    #Get all the files in the folder
    files = os.listdir(folder)
    #Convert each file
    for file in files:
        print("File "+file +": "+ str(files.index(file) + 1) + "/" + str(len(files)))
        convertPDF2IMG(folder + file,output_folder)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert pdf files to images')
    parser.add_argument('-f', '--file', help='The pdf file to convert')
    parser.add_argument('-d', '--directory', help='The directory of pdf files to convert')
    parser.add_argument('-o', '--output', help='The output directory')
    args = parser.parse_args()
    if args.file:
        convertPDF2IMG(args.file,args.output)
    elif args.directory:
        convertFolderPDF2IMG(args.directory,args.output)
    else:
        print("Please specify a file or a directory")

# Path: pdf2image.py