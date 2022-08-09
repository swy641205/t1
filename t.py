import pickle
import matplotlib.cm as cm
import matplotlib.pyplot as plt

with open('dataset.pkl', 'rb') as f:
    train_set, valid_set, *test_set = pickle.load(f)
    # train_set, valid_set, test_set = pickle.load(f)

plt.imshow(train_set[0].reshape((28, 28)), cmap=cm.Greys_r)
plt.show()

#0