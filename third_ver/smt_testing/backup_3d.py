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