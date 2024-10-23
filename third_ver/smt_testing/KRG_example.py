import numpy as np

# Step 1: Define the Kernel Function
def kernel(x1, x2):
    sqdist = np.sum((x1 - x2) ** 2)
    return np.exp(-0.5 * sqdist)

# Step 2: Prepare the Training Data
X_train = np.array([[0, 0], [1, 0], [0, 1]])
y_train = np.array([1, 1.8415, 0.5403])

# Step 3: Prepare the Test Data
X_test = np.array([[1, 1]])


# Step 4: Compute the Covariance Matrix K for Training Data
n = X_train.shape[0]
K = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        K[i, j] = kernel(X_train[i], X_train[j])

# Step 5: Compute the Covariance Vector k_* Between Training and Test Data
k_star = np.array([kernel(X_train[i], X_test[0]) for i in range(n)])

# Step 6: Compute the Predictive Mean
# Solve for alpha: K * alpha = y_train
alpha = np.linalg.solve(K, y_train)

# Compute predictive mean
m_star = np.dot(k_star, alpha)


print(f"Predictive mean: {m_star:.4f}")


