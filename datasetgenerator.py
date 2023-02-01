import numpy as np
import json
import random
import os
import jsonlines
# from openai.wandb_logger import WandbLogger
import wandb

ENTITY = "count-zr0"
PROJECT_NAME = "AvatarGenerator"
QUESTIONS_CSV = 'questions_cyborg.csv'
# MODEL = "ada"
# MODEL = "babbage"
# MODEL = "curie"
MODEL = "davinci"
LEARNING_RATE = .02
# LEARNING_RATE = .2
# EPOCHS = 200
EPOCHS = 4

# set environment variables
os.environ["WANDB_PROJECT"] = "openai-gpt-neo"
os.environ["WANDB_ENTITY"] = "openai-gpt-neo"
os.environ["WANDB_MODE"] = "dryrun"
os.environ["WANDB_WATCH"] = "false"

# with open("questions.csv", encoding="utf8") as questions_file:
with open(QUESTIONS_CSV, encoding="utf8") as questions_file:
    # with open("questions.csv") as questions_file:
    questions = np.loadtxt(questions_file, dtype=str, delimiter=">")
with open("prompts.csv", encoding="utf8") as prompts_file:
    # with open("prompts.csv") as prompts_file:
    prompts = np.loadtxt(prompts_file, dtype=str, delimiter="|")


class Dataset:
    def __init__(self, filename):
        self.filename = filename + ".json"
        self.counter = 0
        if os.path.exists(self.filename):
            self.getCount(), print("You have already generated: ", str(self.counter))
        else:
            self.createFile()
        self.question = ""
        self.answer = ""
        self.entry = None

    def getCount(self):
        with open(self.filename, 'r') as file:
            file_data = json.load(file)
            for entry in file_data:
                self.counter += 1
        return self.counter

    def createFile(self):
        with open(self.filename, 'w') as file:
            create = []
            json.dump(create, file, indent=4)

    def dumpData(self):
        with open(self.filename, 'r+') as file:
            file_data = json.load(file)
            file_data.append(self.entry)
            file.seek(0)
            json.dump(file_data, file, indent=4, ensure_ascii=False)

    def checkDuplicates(self):
        with open(self.filename, 'r') as json_file:
            json_data = json.load(json_file)
            for entry in json_data:
                if entry["question"] == self.question:
                    return True
            return False


class question(Dataset):
    def __init__(self, filename):
        super().__init__(filename)
        self.entry = None

    def get_question(self):
        self.question = random.choice(questions)

    def writeToFile(self):
        if self.answer == "skip":
            print("Skipping")
            return
        self.entry = {
            "prompt": self.question + "\nAI: ",
            "completion": self.answer + "\n",
            "question": self.question
        }
        self.dumpData()

    def get_answer(self):
        self.get_question()
        while self.checkDuplicates():
            self.get_question()
        print("\nQuestion:", self.question)
        self.answer = input("Answer: ")
        self.writeToFile()


class prompt(Dataset):
    def __init__(self, filename):
        super().__init__(filename)
        self.prompt = None
        self.entry = None
        self.context = ""

    def get_prompt(self):
        self.prompt = random.choice(prompts)
        self.question = self.prompt[1]
        self.context = self.prompt[0]

    def writeToFile(self):
        if self.answer == "skip":
            print("Skipping")
            return
        self.entry = {
            "prompt": self.question + "\nAI:\n\n###\n\n:",
            "completion": " " + self.answer + "\n",
            "question": self.question,
            "context": "Context: An AI and a human are speaking " + self.context + "\n",
        }
        self.dumpData()

    def get_answer(self):
        self.get_prompt()
        while self.checkDuplicates():
            self.get_prompt()
        print("\nYou are speaking", self.context)
        print("Person:", self.question)
        self.answer = input("Answer: ")
        self.writeToFile()


class FineTuneModel:
    def __init__(self):
        filename = input("Please enter your dataset filename: ")
        if filename.endswith(".json"):
            self.filename = filename
            self.format()
            self.filename = filename.replace(".json", ".jsonl")
        else:
            if os.path.exists(filename + ".json"):
                self.filename = filename + ".json"
                self.format()
                self.filename = filename + ".jsonl"
            else:
                self.filename = filename + ".jsonl"
        # self.epoch = 2
        self.epoch = EPOCHS
        # self.model = "curie"
        self.model = MODEL
        # self.learning_rate = 0.02
        self.learning_rate = LEARNING_RATE

    def format(self):
        with open(self.filename.replace(".jsonl", ".json"), "r") as old:
            odata = json.load(old)
        with jsonlines.open(self.filename.replace(".json", ".jsonl"), "w") as new:
            for entry in odata:
                line = [
                    {'prompt': entry["prompt"], 'completion': " " + entry["completion"]},
                ]
                new.write_all(line)

    def changeParameters(self):
        changeModel = input("\nDo you want to change the model? (y/n) ")
        if changeModel == "y":
            self.model = input("Please enter the model name: ")
        changeLearningRate = input("\nDo you want to change the learning rate? (y/n) ")
        if changeLearningRate == "y":
            self.learning_rate = float(input("Please enter the learning rate: "))
        chge = input("\nDo you want to change the epoch? (y/n) ")
        if chge == "y":
            self.epoch = int(input("Please enter the epoch: "))
        print("\n\nModel:", self.model + "\nLearning Rate:", str(self.learning_rate), "\nEpoch:", str(self.epoch))
        if input("Are these settings correct? (y/n)") == "y":
            return False
        else:
            return True

    def finetune(self):
        while self.changeParameters():
            continue

        command = "openai api fine_tunes.create -t " + str(
            self.filename) + " -m " + self.model + " --suffix " + self.filename.replace(".jsonl",
                                                                                        "") + " --n_epochs " + str(
            self.epoch) + " --learning_rate_multiplier " + str(self.learning_rate)
        try:
            os.system(str(command))
        except Exception as e:
            print(e)


def datasetcreator():
    _format = input("What format would you like to generate? (Question/Prompt) ")
    while _format != "Question" and _format != "Prompt":
        print("Answer not found, try again")
        _format = input("Please enter Question or Prompt: ")
    filename = input("please enter your dataset filename: ")

    if _format == "Question":
        client = question(filename)
        while __name__ == "__main__":
            client.get_answer()
    elif _format == "Prompt":
        client = prompt(filename)
        while __name__ == "__main__":
            client.get_answer()


def finetune():
    newModel = FineTuneModel()
    newModel.finetune()
    wandb.init(project=PROJECT_NAME, entity=ENTITY)
    wandb.config = {
        "learning_rate": LEARNING_RATE,
        "epochs": EPOCHS,
        "batch_size": 128
    }


print("Welcome to the AI dataset generator!")
useCase = input("Create Dataset (1) or Create Model (2)? ")
if useCase == "1":
    datasetcreator()
else:
    finetune()
