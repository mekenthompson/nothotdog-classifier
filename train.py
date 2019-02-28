import os, sys
import time

from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient

try:  
   os.environ["TRAINING_KEY"]
except KeyError: 
   print ("*** ENVVAR Missing: Please set the environment variable TRAINING_KEY ***")
   sys.exit(1)

TRAINING_KEY = os.environ["TRAINING_KEY"]
SAMPLE_PROJECT_NAME = "nothotdog-classifier"

ENDPOINT = "https://australiaeast.api.cognitive.microsoft.com"

IMAGES_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")

def find_or_create_project():
    # Use the training API to find the SDK sample project created from the training example.
    trainer = CustomVisionTrainingClient(TRAINING_KEY, endpoint=ENDPOINT)

    for proj in trainer.get_projects():
        if (proj.name == SAMPLE_PROJECT_NAME):
            trainer.delete_project(proj.id)

    return trainer.create_project(SAMPLE_PROJECT_NAME)


def train_project():

    trainer = CustomVisionTrainingClient(TRAINING_KEY, endpoint=ENDPOINT)

    # Create a new project
    project = find_or_create_project()

    # Enumerate labels
    subdirs = [ f.path for f in os.scandir(IMAGES_FOLDER) if f.is_dir() ]

    for dir in subdirs:
        label = os.path.basename(dir)
        tag = trainer.create_tag(project.id, label.lower())
        print ("Adding images...", label)
        for image in os.listdir(dir):
            print (image)
            with open(os.path.join(dir, image), mode="rb") as img_data: 
                trainer.create_images_from_data(project.id, img_data.read(), [ tag.id ])

    print ("Training...")
    iteration = trainer.train_project(project.id)
    while (iteration.status == "Training"):
        iteration = trainer.get_iteration(project.id, iteration.id)
        print ("Training status: " + iteration.status)
        time.sleep(1)

    # The iteration is now trained. Make it the default project endpoint
    trainer.update_iteration(project.id, iteration.id, is_default=True)
    print ("Done!")
    return project

if __name__ == "__main__":
    train_project()