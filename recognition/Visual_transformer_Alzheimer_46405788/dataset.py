from torchvision.datasets import ImageFolder
from torchvision.datasets import ImageFolder
import torch
from torch.utils.data import Dataset
from torchvision import datasets
import random

def get_datasets(data_dir, transform=None):
    train_dataset = ImageFolder(root=data_dir + '/train', transform=transform)
    test_dataset = ImageFolder(root=data_dir + '/test', transform=transform)
    return train_dataset, test_dataset
    
class TripletImageFolder(Dataset):
    def __init__(self, root, transform=None):
        self.root = root
        self.transform = transform
        self.image_folder = datasets.ImageFolder(root, transform=None)  # Do not apply transforms initially
        self.labels = self.image_folder.targets

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        anchor, label1 = self.image_folder[idx]  # Get the PIL image
        while True:
            idx2 = torch.randint(0, len(self), (1,)).item()
            positive, label2 = self.image_folder[idx2]
            if label1 == label2:
                break
        while True:
            idx3 = torch.randint(0, len(self), (1,)).item()
            negative, label3 = self.image_folder[idx3]
            if label1 != label3:
                break
        # Apply transforms to PIL images
        if self.transform is not None:
            anchor = self.transform(anchor)
            positive = self.transform(positive)
            negative = self.transform(negative)
        
        return anchor, positive, negative
    
class TripletImageTestFolder(Dataset):
    def __init__(self, root, transform=None):
        random.seed(42)
        self.root = root
        self.transform = transform
        self.image_folder = datasets.ImageFolder(root, transform=None)  # Do not apply transforms initially
        self.labels = self.image_folder.targets
        self.indexsPoitive = random.sample(range(0, len(self)), len(self))
        self.indexsNegative = random.sample(range(0, len(self)), len(self))

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        anchor, label1 = self.image_folder[idx]  # Get the PIL image
        idx2 = 0
        while True:
            if idx + idx2 >= len(self):
                idx = -idx2
            positive, label2 = self.image_folder[self.indexsPoitive[idx + idx2]]
            if label1 == label2:
                break
            idx2 += 1
        idx3 = 0
        while True: 
            if idx + idx3 >= len(self):
                idx = -idx3
            negative, label3 = self.image_folder[self.indexsNegative[idx + idx3]]
            if label1 != label3:
                break
            idx3 += 1
        # Apply transforms to PIL images
        if self.transform is not None:
            anchor = self.transform(anchor)
            positive = self.transform(positive)
            negative = self.transform(negative)
        
        return anchor, positive, negative