import matplotlib.pyplot as plt
from copylot import CoPylot

## Minimum working example with a falling particle receiver -> Must update path to weather file
cp = CoPylot()
r = cp.data_create()
assert cp.data_set_string(
        r,
        "ambient.0.weather_file",
        "../climate_files/USA CA Daggett (TMY2).csv",
    )
cp.data_set_number(r, "solarfield.0.q_des", 100.)

# Receiver: falling particle (rec_type options: External cylindrical, Cavity, Flat plate, Falling particle)
assert cp.data_set_string(r, "receiver.0.rec_type", "Falling particle")
cp.data_set_number(r, "receiver.0.rec_azimuth", 0.)          # aperture faces north (0 deg = north, + clockwise)
cp.data_set_number(r, "receiver.0.rec_height", 21.6)         # aperture height [m]
cp.data_set_number(r, "receiver.0.rec_width", 17.)           # aperture width [m]

# Aperture acceptance window -> limits the field to what the aperture can see
assert cp.data_set_string(r, "receiver.0.accept_ang_type", "Rectangular")
cp.data_set_number(r, "receiver.0.accept_ang_x", 120.)       # horizontal acceptance [deg]
cp.data_set_number(r, "receiver.0.accept_ang_y", 90.)        # vertical acceptance [deg]

# Particle curtain geometry
assert cp.data_set_string(r, "receiver.0.curtain_type", "Flat")   # "Flat" or "Curved" (Curved uses curtain_radius)
cp.data_set_number(r, "receiver.0.norm_curtain_height", 1.)  # curtain height / aperture height
cp.data_set_number(r, "receiver.0.norm_curtain_width", 1.)   # curtain width / aperture width
cp.data_set_number(r, "receiver.0.max_curtain_depth", 1.5)   # curtain entrance depth behind aperture [m]

assert cp.generate_layout(r)
field = cp.get_layout_info(r)
assert cp.simulate(r)
results = cp.summary_results(r, save_dict=True)

# Flux surfaces: 0 = aperture plane, 1 = particle curtain (a curved curtain is split into several surfaces, 1..n)
flux_aperture = cp.get_fluxmap(r, rec_id=0, flux_surface=0)
flux_curtain = cp.get_fluxmap(r, rec_id=0, flux_surface=1)
assert cp.data_free(r)

for k, v in results.items():
    print(f"{k}: {v}")

# Plotting solar field
plt.scatter(field['x_location'], field['y_location'], s=1.5)
plt.xlabel('x (East) [m]')
plt.ylabel('y (North) [m]')
plt.axis('equal')
plt.tight_layout()
plt.show()

# Flux on aperture and particle curtain
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
for ax, flux, title in zip(axs, [flux_aperture, flux_curtain], ["Aperture", "Particle curtain"]):
    im = ax.imshow(flux)
    ax.set_title(title)
    fig.colorbar(im, ax=ax, label='Flux [kW/m$^2$]')
plt.tight_layout()
plt.show()
