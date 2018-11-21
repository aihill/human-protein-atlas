import csv
import numpy as np

from torchvision import transforms
from torch.utils.data import DataLoader
from tqdm import tqdm

from .rather_small_net import Net
from .loss_functions import f1_loss, binary_cross_entropy_with_logits
from .transforms import *
from .datasets import TrainImageDataset, TestImageDataset

def get_dataset(image_dir, label_file, train=True, idxs=None):
    transform = transforms.Compose(
                    [CombineColors(),
                     ToTensor()])
    if train:
        dataset = TrainImageDataset(
                         image_dir=image_dir,
                         label_file=label_file,
                         transform=transform,
                         idxs=idxs)
    else:
        dataset = TestImageDataset(
                         image_dir=image_dir,
                         transform=transform,
                         idxs=idxs)
    return dataset

def get_train_test_split(train_image_dir,
                         train_image_csv,
                         val_split,
                         subsample,
                         n_subsample=100,
                         **kwargs
                         ):
    with open(train_image_csv, 'r') as f:
        n_images = sum(1 for row in f.readlines()) - 1 # -1 for header row
    if subsample:
        arr = np.random.choice(n_images, n_subsample, replace=False)
        train_idxs = arr[:int(n_subsample * (1 - val_split))]
        dev_idxs = arr[int(n_subsample * (1 - val_split)):]
    else:
        arr = np.random.choice(n_images, n_images, replace=False)
        train_idxs = arr[:int(n_images * (1 - val_split))]
        dev_idxs = arr[int(n_images * (1 - val_split)):]

    trainset = get_dataset(train_image_dir, train_image_csv, idxs=train_idxs)
    devset = get_dataset(train_image_dir, train_image_csv, idxs=dev_idxs)

    # trainset = []
    # testset = []
    # print('getting training set...')
    # for i in tqdm(train_idxs):
    #     sample = dataset[i]
    #     trainset.append(sample)
    # print('getting testing set...')
    # for i in tqdm(test_idxs):
    #     sample = dataset[i]
    #     testset.append(sample)
    trainloader = DataLoader(trainset, shuffle=True, **kwargs)
    devloader = DataLoader(devset, shuffle=False, **kwargs)
    return trainloader, devloader

def get_network(pretrained=False):
    if pretrained:
        pass # can't pass pretrained net yet
    else:
        net = Net()
        return net

def get_loss_function(lf='bce'):
    if lf == 'bce':
        return binary_cross_entropy_with_logits
    elif lf == 'f1':
        return f1_loss
    else:
        raise ModuleNotFoundError('loss function not found')
