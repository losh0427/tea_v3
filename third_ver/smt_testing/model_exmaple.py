import numpy as np

def kernel(x1, x2):
    sqdist = np.sum((x1 - x2) ** 2)
    return np.exp(-0.5 * sqdist)

def gaussian_kernel(X1, X2, gamma):
    sq_dists = np.sum((X1[:, np.newaxis, :] - X2[np.newaxis, :, :]) ** 2, axis=2)
    return np.exp(-gamma * sq_dists)

def kriging_model(X_train, y_train, X_test):
    n = X_train.shape[0]
    K = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            K[i, j] = kernel(X_train[i], X_train[j])

    k_star = np.array([kernel(X_train[i], X_test[0]) for i in range(n)])
    alpha = np.linalg.solve(K, y_train)
    m_star = np.dot(k_star, alpha)

    return m_star

def kpls_model(X_train, y_train, X_test):
    gamma = 0.5
    K = gaussian_kernel(X_train, X_train, gamma)
    N = K.shape[0]
    one_N = np.ones((N, N)) / N
    K_centered = K - one_N @ K - K @ one_N + one_N @ K @ one_N

    y_mean = np.mean(y_train)
    y_centered = y_train - y_mean

    w = K_centered @ y_centered
    w_norm = w / np.linalg.norm(w)
    t = K_centered @ w_norm
    c = (t @ y_centered) / (t @ t)
    beta = w_norm * c

    k_test = gaussian_kernel(X_test, X_train, gamma)
    k_train_mean = np.mean(K, axis=0)
    k_test_mean = np.mean(k_test)
    K_mean = np.mean(K)
    k_test_centered = k_test - k_train_mean + K_mean - k_test_mean

    y_test_pred_centered = k_test_centered @ beta
    y_test_pred = y_test_pred_centered + y_mean

    return y_test_pred[0]

def main():
    np.random.seed(0)
    test_data_size = 3
    X_test = np.random.uniform(-10, 10, (test_data_size, 2))
    y_test = np.sin(X_test[:, 0]) + np.cos(X_test[:, 1])

    training_sizes = [10, 100, 1000]
    for idx, train_size in enumerate(training_sizes):
        X_train = np.random.uniform(-10, 10, (train_size, 2))
        y_train = np.sin(X_train[:, 0]) + np.cos(X_train[:, 1])

        print(f"Iteration {idx + 1} with {train_size} training samples:\n")
        for i in range(len(X_test)):
            kriging_pred = kriging_model(X_train, y_train, X_test[i].reshape(1, -1))
            kpls_pred = kpls_model(X_train, y_train, X_test[i].reshape(1, -1))
            true_value = y_test[i]

            print(f"  Test Sample {i + 1}:")
            print(f"    True Value: {true_value:.4f}")
            print(f"    Kriging Prediction: {kriging_pred:.4f}")
            print(f"    KPLS Prediction: {kpls_pred:.4f}\n")

if __name__ == "__main__":
    main()
