import numpy as np

# 1. Prepare the Training Data
X_train = np.array([[0, 0], [1, 0], [0, 1]])

y_train = np.array([1, 1.8415, 0.5403])

# 2. Prepare the Testing Data
X_test = np.array([[1, 1]])

# 3. Set the Gamma Parameter for the Gaussian Kernel
gamma = 0.5

# 4. Compute the Gaussian Kernel Matrix
def gaussian_kernel(X1, X2, gamma):
    sq_dists = np.sum((X1[:, np.newaxis, :] - X2[np.newaxis, :, :]) ** 2, axis=2)
    return np.exp(-gamma * sq_dists)

K = gaussian_kernel(X_train, X_train, gamma)
# 5. Center the Kernel Matrix
N = K.shape[0]
one_N = np.ones((N, N)) / N
K_centered = K - one_N @ K - K @ one_N + one_N @ K @ one_N

# 6. Center the Output Vector
y_mean = np.mean(y_train)
y_centered = y_train - y_mean


# 7. Compute the Weight Vector
w = K_centered @ y_centered

# 8. Normalize the Weight Vector
w_norm = w / np.linalg.norm(w)

# 9. Compute the Scores
t = K_centered @ w_norm
# 10. Compute the Regression Coefficient
c = (t @ y_centered) / (t @ t)
# 11. Compute the Final Model Coefficients
beta = w_norm * c

# 12. Compute the Kernel Vector for the Test Sample
k_test = gaussian_kernel(X_test, X_train, gamma)

# 13. Center the Kernel Vector
k_train_mean = np.mean(K, axis=0)
k_test_mean = np.mean(k_test)
K_mean = np.mean(K)
k_test_centered = k_test - k_train_mean + K_mean - k_test_mean

# 14. Predict the Centered value
y_test_pred_centered = k_test_centered @ beta

# 15. Add the Mean to Get the Final Prediction
y_test_pred = y_test_pred_centered + y_mean

# 16. Output the Result
print("Predicted y for the test sample:", y_test_pred[0])
