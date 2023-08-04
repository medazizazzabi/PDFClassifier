import random
import os
import argparse

def removeUnlabelledImages(images,labels):
    #Get all the images in the folder
    files = os.listdir(images)
    #Remove the extension from the names
    files = [(os.path.splitext(file)[0],os.path.splitext(file)[1]) for file in files]
    #Get all the labels in the folder
    labels = os.listdir(labels)
    #Remove the extension from the names
    labels = [os.path.splitext(label)[0] for label in labels]
    #Remove the images that don't have a label 
    for file,extention in files:
        if file not in labels:
            os.remove(images+file+extention)
            print("Removed "+file)
    
def removeUnusedLabels(images,labels):
    #Get all the images in the folder
    files = os.listdir(images)
    #Remove the extension from the names
    files = [os.path.splitext(file)[0] for file in files]
    #Get all the labels in the folder
    labels = os.listdir(labels)
    #Remove the extension from the names
    labels = [(os.path.splitext(label)[0],os.path.splitext(label)[1]) for label in labels]
    #Remove the labels that don't have an image
    for label,extention in labels:
        if label not in files:
            os.remove(labels+label+extention)
            print("Removed "+label)

def cleanDataset(images,labels):
    removeUnlabelledImages(images,labels)
    removeUnusedLabels(images,labels)


def settingDirectory(output):
    #Create the output folder if it doesn't exist
    if not os.path.exists(output):
        os.makedirs(output)

    #Create the train 0 test folders if they don't exist
    if not os.path.exists(output+"/train"):
        os.makedirs(output+"/train")
    if not os.path.exists(output+"/test"):
        os.makedirs(output+"/test")

    #Create the images and labels folders if they don't exist
    if not os.path.exists(output+"/train/images"):
        os.makedirs(output+"/train/images")
    if not os.path.exists(output+"/train/labels"):
        os.makedirs(output+"/train/labels")
    if not os.path.exists(output+"/test/images"):
        os.makedirs(output+"/test/images")
    if not os.path.exists(output+"/test/labels"):
        os.makedirs(output+"/test/labels")

def splitDataset(dataset,output,train,test):
    if(train+test != 100):
        print("The sum of the train and test percentages must be 100")
        exit(1)
    else:
        print("Splitting dataset...")

    #Initiliazing the output directory
    settingDirectory(output)

    #Clean the dataset
    cleanDataset(dataset+"/images/",dataset+"/labels/")

    #Get all the images in the folder
    files = os.listdir(dataset+"/images/")
    #Remove the extension from the names
    files = [os.path.splitext(file)[0] for file in files]

    #Get the number of images
    num_images = len(files)

    #Get the number of images for the train and test sets
    num_train = int(num_images*train/100)
    num_test = int(num_images*test/100)

    #Rnadomly select the images for the train and test sets
    train_images = random.sample(files,num_train)
    test_images = [image for image in files if image not in train_images]

    #Copy the images to the train and test folders
    for image in train_images:
        os.rename(dataset+"/images/"+image+".png",output+"/train/images/"+image+".png")
        os.rename(dataset+"/labels/"+image+".txt",output+"/train/labels/"+image+".txt")
    for image in test_images:
        os.rename(dataset+"/images/"+image+".png",output+"/test/images/"+image+".png")
        os.rename(dataset+"/labels/"+image+".txt",output+"/test/labels/"+image+".txt")
    

    print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split Dataset')
    dataset = parser.add_argument('-dataset', '--dataset', help='The dataset')
    try:
        train = parser.add_argument('-train', '--train', help='The train dataset',type=int)
    except Exception as e:
        print("Please specify the trainig percentage")
        exit(1)
    try:
        test= parser.add_argument('-test', '--test', help='The test dataset',type=int)
    except:
        print("Please specify the test percentage")
        exit(1)
    
    parser.add_argument('-o', '--output', help='The output directory')
    args = parser.parse_args()
    if args.dataset:
        splitDataset(args.dataset,args.output,args.train,args.test)
    else:
        print("Please specify a dataset")
