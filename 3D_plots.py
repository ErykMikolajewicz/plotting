import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from tqdm import tqdm  # tqdm function make a loop progress bar in console

from fluid_densities import ro_air

# conditions for which the chart will be drawn
temperature_start_point = 273
temperature_end_point = 373
temperature_points_number = 200
pressure_start_point = 10**5
pressure_end_point = 2*10**5
pressure_points_number = 200
humidity = 0.6

temperature_axis = np.linspace(temperature_start_point, temperature_end_point, temperature_points_number)

pressure_axis = np.linspace(pressure_start_point, pressure_end_point, pressure_points_number)

temperature_mesh, pressure_mesh = np.meshgrid(temperature_axis, pressure_axis)
printing_mesh = np.zeros_like(temperature_mesh)

for i1, (temperature_row, pressure_row) in tqdm(enumerate(zip(temperature_mesh, pressure_mesh))):
    
    for i2, (temperature, pressure) in enumerate(zip(temperature_row, pressure_row)):
        
        printing_mesh[i1][i2] = ro_air(temperature, pressure, humidity)
        
# Plot the surface.
fig = plt.figure()

ax = plt.axes(projection='3d')

surf = ax.plot_surface(temperature_mesh, pressure_mesh, printing_mesh,
                       cmap=cm.jet, linewidth=0, antialiased=False)

# Customize the z axis.
z_axis_minimum = np.min(printing_mesh)
z_axis_maximum = np.max(printing_mesh)
ax.set_zlim(z_axis_minimum, z_axis_maximum )
ax.set_xlim(temperature_start_point, temperature_end_point)
ax.set_ylim(pressure_start_point, pressure_end_point)
ax.set_xlabel('Temperature [K]', fontsize=15, rotation=30)
ax.set_ylabel('Pressure [Pa]', fontsize=15, rotation=0)
ax.yaxis.set_major_formatter(FormatStrFormatter('%.1e'))
ax.set_zlabel('Density [kg/m^3]', fontsize=15)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()
