from __future__ import print_function
import numpy as np
from netlearner.utils import min_max_normalize, accuracy, measure_prediction
from netlearner.stacked_rbm import StackedRBM


raw_train_dataset = np.load('NSLKDD/train_dataset.npy')
train_labels = np.load('NSLKDD/train_ref.npy')
raw_valid_dataset = np.load('NSLKDD/valid_dataset.npy')
valid_labels = np.load('NSLKDD/valid_ref.npy')
raw_test_dataset = np.load('NSLKDD/test_dataset.npy')
test_labels = np.load('NSLKDD/test_ref.npy')

[train_dataset, valid_dataset, test_dataset] = min_max_normalize(
    raw_train_dataset, raw_valid_dataset, raw_test_dataset)
train_dataset = np.concatenate((train_dataset, valid_dataset), axis=0)
train_labels = np.concatenate((train_labels, valid_labels), axis=0)
print('Training set', train_dataset.shape, train_labels.shape)
print('Test set', test_dataset.shape, test_labels.shape)

num_samples = train_dataset.shape[0]
feature_size = train_dataset.shape[1]
rbm_layer_sizes = [400, 400]
num_labels = train_labels.shape[1]
srbm = StackedRBM(feature_size, rbm_layer_sizes, num_labels,
                  ft_reg_factor=0.0, ft_lr=0.2)
batch_sizes = [200, 200]
num_steps = [100, 100]
ft_batch_size = 240
ft_num_steps = 8000
srbm.train(train_dataset, train_labels, batch_sizes, num_steps,
           ft_batch_size, ft_num_steps)
encoded_train_dataset = srbm.encode_dataset(train_dataset)
encoded_test_dataset = srbm.encode_dataset(test_dataset)
print('Encoded training set', encoded_train_dataset.shape)
print('Encoded test set', encoded_test_dataset.shape)
np.save('trainset.srbm.npy', encoded_train_dataset)
np.save('testset.srbm.npy', encoded_test_dataset)
