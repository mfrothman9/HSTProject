import numpy as np
import matplotlib.pyplot as plt
import os

# INPUT FILE
# input_filename = "YZ_CMi_BBfit_100-3100A.csv" 
# input_filename = "AD_Leo_BBfit_100-3100A.csv"
input_filename = "AU_Mic_BBfit_100-3100A.csv"
# INPUT PATH
input_filepath = "./" 

#pulling the comments from the first couple lines
comments = []
with open(os.path.join(input_filepath, input_filename), 'r') as f:
    for line in f:
        if line.startswith('#'):
            comments.append(line.strip())
        else:
            break

#extracting the parameter fit from the headers
fit_info = comments[1] if len(comments) > 1 else ""
print(fit_info)
legend_text = fit_info.replace('#', '').strip()
idx = legend_text.index(",")
temp_info = legend_text[0:idx]
scale_info = legend_text[idx+2:len(legend_text)]

#reading the data in
data = np.genfromtxt(os.path.join(input_filepath, input_filename), 
                     delimiter=',', 
                     skip_header=3, #skipping the commented lines
                     names=['wavelength', 'flux', 'error'])

wavelength = data['wavelength']
flux = data['flux']
error = data['error']

#plotting the data with two panels
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

#flux vs wavelength in log space
ax1.plot(wavelength, flux, 'b-', linewidth=2, label=f'Blackbody Fit\n{temp_info}\n{scale_info}')
ax1.fill_between(wavelength, flux - error, flux + error, 
                alpha=0.3, color='blue', label='1σ Error')
ax1.set_ylabel('Flux [erg / (Å s cm²)]', fontsize=12)
ax1.set_title('Blackbody Temperature Fit', fontsize=14, fontweight='bold')
ax1.set_yscale('log')
ax1.grid(True, alpha=0.3, which='both')
ax1.legend(fontsize=10)

#bottom panel - same data, in lin space
ax2.plot(wavelength, flux, 'b-', linewidth=2)
ax2.fill_between(wavelength, flux - error, flux + error, 
                alpha=0.3, color='blue')
ax2.set_xlabel('Wavelength [Å]', fontsize=12)
ax2.set_ylabel('Flux [erg / (Å s cm²)]', fontsize=12)
ax2.grid(True, alpha=0.3, which='both')

plt.tight_layout()

plt.show()