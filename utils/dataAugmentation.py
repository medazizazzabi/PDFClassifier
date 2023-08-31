import os
import cv2
import time
import imgaug as ia
from imgaug import augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage

# Randomized augmentation pipeline
# Randomized augmentation pipeline
seq = iaa.Sequential([
    iaa.SomeOf((2 , 7), [  # apply 2 to 4 of the augmentations below
        iaa.Fliplr(0.5),  # horizontal flip
        iaa.Flipud(0.2),  # vertical flip
        iaa.Affine(rotate=(-45, 45)),  # random rotations between -45 and 45 degrees
        iaa.Affine(scale=(0.5, 1.5)),  # random scale
        iaa.Multiply((0.8, 1.2)),  # change brightness
        iaa.AdditiveGaussianNoise(scale=0.05*255),  # gaussian noise
        iaa.GaussianBlur(sigma=(0.0, 3.0)),  # blur images
        iaa.ContrastNormalization((0.75, 1.5)),  # random contrast change
        iaa.Add((-40, 40)),  # add a value between -40 and 40 to each pixel
        iaa.LinearContrast((0.75, 1.25)),  # linear contrast adjustment
        iaa.AddToHueAndSaturation((-20, 20)),  # hue and saturation adjustment
        iaa.Grayscale(alpha=(0.0, 1.0)),  # randomly turn the image grayscale
    ], random_order=True)  # apply the augmentations in random order
])



def yolo_to_imgaug(yolo_boxes, img_shape):
    height, width = img_shape
    bbs = []
    for box in yolo_boxes:
        x_center, y_center, w, h = box
        x1 = (x_center - w / 2) * width
        y1 = (y_center - h / 2) * height
        x2 = (x_center + w / 2) * width
        y2 = (y_center + h / 2) * height
        bbs.append(BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2))
    return BoundingBoxesOnImage(bbs, shape=img_shape)

def imgaug_to_yolo(bbs, img_shape):
    height, width = img_shape
    yolo_boxes = []
    for bb in bbs.bounding_boxes:
        x_center = (bb.x1 + bb.x2) / 2 / width
        y_center = (bb.y1 + bb.y2) / 2 / height
        w = (bb.x2 - bb.x1) / width
        h = (bb.y2 - bb.y1) / height
        yolo_boxes.append((x_center, y_center, w, h))
    return yolo_boxes

images_path = "images/"
labels_path = "labels/"

for img_file in os.listdir(images_path):
    img_path = os.path.join(images_path, img_file)
    label_file = os.path.splitext(img_file)[0] + '.txt'
    label_path = os.path.join(labels_path, label_file)
    
    # Read image and label
    image = cv2.imread(img_path)
    with open(label_path, 'r') as f:
        yolo_labels = [tuple(map(float, line.strip().split()[1:])) for line in f.readlines()]
    
    # Convert YOLO labels to imgaug BoundingBoxes
    bbs = yolo_to_imgaug(yolo_labels, image.shape[:2])
    
    # Augment image and bounding boxes
    image_aug, bbs_aug = seq(image=image, bounding_boxes=bbs)
    
    # Convert augmented bounding boxes back to YOLO format
    yolo_labels_aug = imgaug_to_yolo(bbs_aug, image_aug.shape[:2])


    name = time.time()
    # Save augmented image and label
    cv2.imwrite(os.path.join(images_path, "aug_"+str(name) + img_file), image_aug)
    with open(os.path.join(labels_path, "aug_"+str(name) + label_file), 'w') as f:
        for i, (x, y, w, h) in enumerate(yolo_labels_aug):
            f.write(f"0 {x} {y} {w} {h}\n")
