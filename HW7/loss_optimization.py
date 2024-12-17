# -*- coding: utf-8 -*-
"""loss_optimization.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dr6Cmg_iEIl4tZpqbe9860KtUKrf3Zk_
"""

# no imports beyond the ones below should be needed in answering this question
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

def sigmoid(z):
	"""sigmoid function"""
	result = 1 / (1 + np.exp(-z))

	assert np.all(0.0 <= result)

	assert np.all(result <= 1.0)

	return result

def log_loss(y, y_probs):
	"""log-loss function"""
	assert np.all(y_probs >= 0.0)

	assert np.all(y_probs <= 1.0)

	result = (-y * np.log(y_probs) - (1 - y) * np.log(1 - y_probs)).mean()

	return result

def log_loss_grad(X, y, w):
	"""gradient of the log-loss function"""
	assert len(X.shape)==2

	assert len(y.shape)==1

	assert X.shape[1] == w.shape[0]

	assert X.shape[0] == y.shape[0]

	y_probs = predict_probs(X, w)

	assert y_probs.shape[0] == y.shape[0]

	result = np.dot(X.T, (y_probs - y)) / y.shape[0]

	return result

def predict_probs(X, w):
	"""predict logistic regression probabilities"""
	assert X.shape[1] == w.shape[0]

	result = sigmoid(np.dot(X, w))

	return result

def predict(X, w, threshold=0.5):
	"""make logistic regression predictions using a specified threshold
	to binarize the probability threshold
	"""
	return 1.0 * (predict_probs(X, w) >= threshold)

def evaluate_accuracy(X, y, w):
	"""evaluate accuracy by making predictions
	and comparing with groundtruth"""
	y_predict = predict(X, w)

	result = (y == y_predict).mean()

	assert (0.0 <= result <= 1.0)

	return result

def gradient_descent(w, X, y, f_grad, lr = 1e-2):
	"""makes an update using gradient descent
	where the gradient is calculated using all the data
	Parameters:
		w: current weight parameter, shape = num_features
		X: input features, shape = num_datapoints, num_features
		y: binary output target, shape = num_datapoints
		f_grad: a Python function which computes the gradient of the log-loss function, use log_loss_grad here
		lr: learning rate for gradient descent
	"""
	# Do not edit any code outside the edit region
	# Edit region starts here
	#########################
  # Compute the gradient over the entire dataset
	grad = f_grad(X, y, w)
	# Update weights
	w -= lr * grad
	#########################
	# Edit region ends here

	assert X.shape[1] == w.shape[0]

def stochastic_gradient_descent(w, X, y, f_grad, lr = 1e-2):
	"""makes an update using stochastic gradient descent
	where the gradient is calculated using a randomly chosen datapoint

	Parameters:
		w: current weight parameter, shape = num_features
		X: input features, shape = num_datapoints, num_features
		y: binary output target, shape = num_datapoints
		f_grad: a Python function which computes the gradient of the log-loss function, use log_loss_grad here
		lr: learning rate for stochastic gradient descent
	"""
	# Do not edit any code outside the edit region
	# Edit region starts here
	#########################
  # Randomly select an index
	i = np.random.randint(X.shape[0])
  # Get the corresponding datapoint and label
	X_i = X[i:i+1]  # Keep the shape as (1, num_features)
	y_i = y[i:i+1]  # Keep the shape as (1,)
  # Compute the gradient for the selected datapoint
	grad = f_grad(X_i, y_i, w)
  # Update weights
	w -= lr * grad
	#########################
	# Edit region ends here

	assert X.shape[1] == w.shape[0]

def adagrad(w, X, y, f_grad, gti, lr = 1e-2, eps_stable = 1e-8):
	"""makes an update using adagrad
	where the gradient is calculated using a randomly chosen datapoint
	and gti maintains the running sum of squared gradient magnitudes required for the adagrad update

	Parameters:
		w: current weight parameter, shape = num_features
		X: input features, shape = num_datapoints, num_features
		y: binary output target, shape = num_datapoints
		f_grad: a Python function which computes the gradient of the log-loss function, use log_loss_grad here
		gti: maintains the running sum of squared gradient magnitude, shape = num_features
		lr: learning rate for AdaGrad
	"""
	# Do not edit any code outside the edit region
	# Edit region starts here
	#########################
  # Add a constant feature at position 0 of datapoints EDIT BLOCK
	intercept = np.random.randint(0, X.shape[0])
	X_i = X[intercept:intercept + 1]
	y_i = y[intercept:intercept + 1]

	# Compute the gradient
	grad = f_grad(X_i, y_i, w)
  # Update the running sum of squared gradients
	gti += grad**2
  # Compute the adjusted learning rate
	adjusted_g = grad / (np.sqrt(gti) + eps_stable)
  # Update weights
	w -= lr * adjusted_g

	assert X.shape[1] == w.shape[0]
	return w, gti
	#########################
	# Edit region ends here

if __name__ == '__main__':
	# set numpy seed for reproducibility
	np.random.seed(666)

	# load well-known Iris dataset from scikit-learn package
	# convert from 3 to 2 classes for binary classification
	iris = load_iris()
	X = iris.data[:, :2]
	y = (iris.target != 0) * 1

	# add a constant feature at position 0 of datapoints
	# the first weight therefore corresponds to the bias term
	intercept = np.ones((X.shape[0], 1))
	X = np.concatenate((intercept, X), axis=1)

	# split data into train and test using a scikit-learn utility function
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=666)

	# number of epochs
	num_epochs = 10000

	# initialize weights for gradient descent, stochastic gradient descent, adagrad
	w_gd = np.zeros(X.shape[1])
	w_sgd = np.zeros(X.shape[1])
	w_adagrad = np.zeros(X.shape[1])

	# initialize G_tii for adagrad
	gti = np.zeros(X.shape[1])

	for epoch in range(num_epochs):
		# gradient descent is executed only once per epoch since it runs over entire data
		gradient_descent(w_gd, X_train, y_train, log_loss_grad)

		for i in range(X_train.shape[0]):
			# stochastic gradient descent and adagrad executed as many times in an epoch as the number of datapoints
			stochastic_gradient_descent(w_sgd, X_train, y_train, log_loss_grad)
			adagrad(w_adagrad, X_train, y_train, log_loss_grad, gti)

		# calculate and print train logistic loss using the three update methods at the end of each epoch
		train_logloss_gd = log_loss(y_train, predict_probs(X_train, w_gd))
		train_logloss_sgd = log_loss(y_train, predict_probs(X_train, w_sgd))
		train_logloss_adagrad = log_loss(y_train, predict_probs(X_train, w_adagrad))
		print('Train LogLoss (GD, SGD, AdaGrad):', train_logloss_gd, train_logloss_sgd, train_logloss_adagrad)

		# calculate and print train accuracies using the three update methods at the end of each epoch
		train_accuracy_gd = evaluate_accuracy(X_train, y_train, w_gd)
		train_accuracy_sgd = evaluate_accuracy(X_train, y_train, w_sgd)
		train_accuracy_adagrad = evaluate_accuracy(X_train, y_train, w_adagrad)
		print('Train Accuracies (GD, SGD, AdaGrad):', train_accuracy_gd, train_accuracy_sgd, train_accuracy_adagrad)

	# calculate test accuracies using the three update methods
	test_accuracy_gd = evaluate_accuracy(X_test, y_test, w_gd)
	test_accuracy_sgd = evaluate_accuracy(X_test, y_test, w_sgd)
	test_accuracy_adagrad = evaluate_accuracy(X_test, y_test, w_adagrad)
	print('Test Accuracies (GD, SGD, AdaGrad):', test_accuracy_gd, test_accuracy_sgd, test_accuracy_adagrad)

# ### PART 1 Q3 ###

# import matplotlib.pyplot as plt
# import numpy as np

# # Initialize lists to store trajectories
# trajectory_gd = []
# trajectory_sgd = []
# trajectory_adagrad = []

# # Training loop with trajectory tracking
# for epoch in range(num_epochs):
#     # Gradient Descent
#     gradient_descent(w_gd, X_train, y_train, log_loss_grad)
#     trajectory_gd.append(w_gd[1:3])  # Append w1, w2 (non-bias weights)

#     for i in range(X_train.shape[0]):
#         # Stochastic Gradient Descent
#         stochastic_gradient_descent(w_sgd, X_train, y_train, log_loss_grad)
#         # AdaGrad
#         adagrad(w_adagrad, X_train, y_train, log_loss_grad, gti)

#     # Track the final weights for SGD and AdaGrad at the end of each epoch
#     trajectory_sgd.append(w_sgd[1:3])
#     trajectory_adagrad.append(w_adagrad[1:3])

# # Convert trajectories to numpy arrays for easier plotting
# trajectory_gd = np.array(trajectory_gd)
# trajectory_sgd = np.array(trajectory_sgd)
# trajectory_adagrad = np.array(trajectory_adagrad)

# # Plot the trajectories
# plt.figure(figsize=(8, 6))
# plt.plot(trajectory_gd[:, 0], trajectory_gd[:, 1], label='Gradient Descent', marker='o', markersize=4)
# plt.plot(trajectory_sgd[:, 0], trajectory_sgd[:, 1], label='Stochastic Gradient Descent', marker='x', markersize=4)
# plt.plot(trajectory_adagrad[:, 0], trajectory_adagrad[:, 1], label='AdaGrad', marker='^', markersize=4)
# plt.xlabel('w1')
# plt.ylabel('w2')
# plt.title('Weight Trajectories in 2D Parameter Space')
# plt.legend()
# plt.grid(True)
# plt.show()

# ### PART 2 Q3 ###

# import matplotlib.pyplot as plt
# import numpy as np

# # Define a helper function to calculate the decision boundary
# def plot_decision_boundary(w, label, color):
#     """
#     Plots the decision boundary for a given weight vector w.
#     """
#     x_min, x_max = X_train[:, 1].min() - 1, X_train[:, 1].max() + 1
#     y_min, y_max = X_train[:, 2].min() - 1, X_train[:, 2].max() + 1
#     x_vals = np.linspace(x_min, x_max, 100)
#     # Decision boundary: w0 + w1 * x + w2 * y = 0 -> y = -(w0 + w1 * x) / w2
#     y_vals = -(w[0] + w[1] * x_vals) / w[2]
#     plt.plot(x_vals, y_vals, label=label, color=color)

# # Plot the dataset
# plt.figure(figsize=(8, 6))

# # Positive and negative points (Train)
# plt.scatter(X_train[y_train == 1][:, 1], X_train[y_train == 1][:, 2],
#             color='green', marker='o', label='Positive Train Points')
# plt.scatter(X_train[y_train == 0][:, 1], X_train[y_train == 0][:, 2],
#             color='red', marker='x', label='Negative Train Points')

# # Positive and negative points (Test)
# plt.scatter(X_test[y_test == 1][:, 1], X_test[y_test == 1][:, 2],
#             color='green', marker='s', label='Positive Test Points', alpha=0.6)
# plt.scatter(X_test[y_test == 0][:, 1], X_test[y_test == 0][:, 2],
#             color='red', marker='^', label='Negative Test Points', alpha=0.6)

# # Plot the decision boundaries
# plot_decision_boundary(w_gd, label='Gradient Descent', color='blue')
# plot_decision_boundary(w_sgd, label='Stochastic Gradient Descent', color='orange')
# plot_decision_boundary(w_adagrad, label='AdaGrad', color='purple')

# # Finalize the plot
# plt.xlabel('Feature 1')
# plt.ylabel('Feature 2')
# plt.title('Decision Boundaries and Data Points')
# plt.legend()
# plt.grid(True)
# plt.show()

# ### PART 3 Q3 ###

# import matplotlib.pyplot as plt

# # Initialize lists to store log-loss values for each epoch
# log_loss_gd_values = []
# log_loss_sgd_values = []
# log_loss_adagrad_values = []

# # Training loop with log-loss tracking
# for epoch in range(num_epochs):
#     # Gradient Descent
#     gradient_descent(w_gd, X_train, y_train, log_loss_grad)
#     log_loss_gd_values.append(log_loss(y_train, predict_probs(X_train, w_gd)))

#     for i in range(X_train.shape[0]):
#         # Stochastic Gradient Descent
#         stochastic_gradient_descent(w_sgd, X_train, y_train, log_loss_grad)
#         # AdaGrad
#         adagrad(w_adagrad, X_train, y_train, log_loss_grad, gti)

#     # Track log-loss for SGD and AdaGrad at the end of each epoch
#     log_loss_sgd_values.append(log_loss(y_train, predict_probs(X_train, w_sgd)))
#     log_loss_adagrad_values.append(log_loss(y_train, predict_probs(X_train, w_adagrad)))

# # Plot the log-loss curves
# plt.figure(figsize=(8, 6))
# plt.plot(range(num_epochs), log_loss_gd_values, label='Gradient Descent', color='blue')
# plt.plot(range(num_epochs), log_loss_sgd_values, label='Stochastic Gradient Descent', color='orange')
# plt.plot(range(num_epochs), log_loss_adagrad_values, label='AdaGrad', color='purple')

# # Add labels, title, and legend
# plt.xlabel('Epoch')
# plt.ylabel('Train Logistic Loss')
# plt.title('Train Logistic Loss vs Epoch for Different Optimizers')
# plt.legend()
# plt.grid(True)
# plt.show()

# ### PART 4 Q3 ###

# # Initialize lists to store accuracy values for each epoch
# accuracy_gd_values = []
# accuracy_sgd_values = []
# accuracy_adagrad_values = []

# # Training loop with accuracy tracking
# for epoch in range(num_epochs):
#     # Gradient Descent
#     gradient_descent(w_gd, X_train, y_train, log_loss_grad)
#     accuracy_gd_values.append(evaluate_accuracy(X_train, y_train, w_gd))

#     for i in range(X_train.shape[0]):
#         # Stochastic Gradient Descent
#         stochastic_gradient_descent(w_sgd, X_train, y_train, log_loss_grad)
#         # AdaGrad
#         adagrad(w_adagrad, X_train, y_train, log_loss_grad, gti)

#     # Track accuracy for SGD and AdaGrad at the end of each epoch
#     accuracy_sgd_values.append(evaluate_accuracy(X_train, y_train, w_sgd))
#     accuracy_adagrad_values.append(evaluate_accuracy(X_train, y_train, w_adagrad))

# # Plot the accuracy curves
# plt.figure(figsize=(8, 6))
# plt.plot(range(num_epochs), accuracy_gd_values, label='Gradient Descent', color='blue')
# plt.plot(range(num_epochs), accuracy_sgd_values, label='Stochastic Gradient Descent', color='orange')
# plt.plot(range(num_epochs), accuracy_adagrad_values, label='AdaGrad', color='purple')

# # Add labels, title, and legend
# plt.xlabel('Epoch')
# plt.ylabel('Train Accuracy')
# plt.title('Train Accuracy vs Epoch for Different Optimizers')
# plt.legend()
# plt.grid(True)
# plt.show()

# # Calculate test accuracies using the trained weights
# test_accuracy_gd = evaluate_accuracy(X_test, y_test, w_gd)
# test_accuracy_sgd = evaluate_accuracy(X_test, y_test, w_sgd)
# test_accuracy_adagrad = evaluate_accuracy(X_test, y_test, w_adagrad)

# # Print the test accuracies
# print("Test Accuracy (Gradient Descent):", test_accuracy_gd)
# print("Test Accuracy (Stochastic Gradient Descent):", test_accuracy_sgd)
# print("Test Accuracy (AdaGrad):", test_accuracy_adagrad)