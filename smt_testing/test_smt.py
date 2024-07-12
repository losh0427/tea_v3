from smt.sampling_methods import LHS, Random
from smt.surrogate_models import KRG, KPLS
import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

def initial_LHS_model():
    # Define the limits for the sampling
    xlimits = np.array([[0, 500], [0, 500], [-300, 300]])
    
    # Create the sampling method instance
    sampling_method = Random(xlimits=xlimits)
    
    # Sample a point
    sampling_value = sampling_method(1)[0]
    
    return sampling_value

def sample(num):
    samples = []
    for i in range(num):
        samples.append(initial_LHS_model())
    return samples

def plot_3d(data, model, title, zlim):
    # Clear the plot
    plt.clf()
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create the meshgrid
    x1 = np.linspace(0, 500, 100)
    x2 = np.linspace(0, 500, 100)
    X1, X2 = np.meshgrid(x1, x2)
    X = np.hstack((X1.reshape(-1, 1), X2.reshape(-1, 1)))
    
    # Predict the values
    y = model.predict_values(X)
    Y = y.reshape(100, 100)
    
    # Plot the surface with color mapping to Y values
    surf = ax.plot_surface(X1, X2, Y, cmap='viridis', edgecolor='none', vmin=zlim[0], vmax=zlim[1])
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    # Plot the data points in red
    ax.scatter(data['x1'], data['x2'], data['y'], color='red')
    
    # Set the limits for the x, y, and z axes
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 500)
    ax.set_zlim(zlim[0], zlim[1])
    
    ax.set_title(title)
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('y')

    # Save the plot
    plt.savefig(f'{title}.png')

if __name__ == '__main__':
    # Sample 50 points
    samples = sample(50)
    
    # Save it to csv
    with open('sample.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["x1", "x2", "y"])
        for sample in samples:
            # Generate dummy y values for demonstration
            y_value = np.sin(sample[0]) + np.cos(sample[1]) + np.tan(sample[2])
            writer.writerow([sample[0], sample[1], y_value])

    # Load the data
    data = pd.read_csv('sample.csv')
    data.columns = ['x1', 'x2', 'y']
    
    # Create the kriging model
    krg = KRG(print_global=False)
    krg.set_training_values(data[['x1', 'x2']].values, data['y'].values)
    krg.train()

    # Create the kpls model
    kpls = KPLS(print_global=False)
    kpls.set_training_values(data[['x1', 'x2']].values, data['y'].values)
    kpls.train()
    
    # Determine the color limits
    zlim = [data['y'].min(), data['y'].max()]
    
    # Plot the results
    plot_3d(data, krg, 'KRG', zlim)
    plot_3d(data, kpls, 'KPLS', zlim)
