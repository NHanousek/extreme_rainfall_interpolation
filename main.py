from InterpolationCurves import CoercedQuadratic, GEV
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Assign the rainfall data - this bit will be project specific
depth_1000 = 200
depth_2000 = 250
pmp_depth = 900
pmp_aep = 500000

# Get the interpolations for Siriwardena & Weinmann (1998)
sw = CoercedQuadratic('SiriwardenaWeinmann1998')
sw.setup_rainfall_boundaries(aep_2000=depth_2000, aep_1000=depth_1000,
                             pmp_depth=pmp_depth, pmp_aep=pmp_aep)
sw.fit_curve()
slope_ratio = sw.Sgc / sw.Sgap
if slope_ratio > 2.0:
    print('\nSiriwardena & Weinmann (1998) method is outside the range of application')
else:
    print('\nSiriwardena & Weinmann (1998) method is inside the range of application')

# Get the interpolations for Hill et al. (2000)
hill = CoercedQuadratic('HillAndOthers2000')
hill.setup_rainfall_boundaries(aep_2000=depth_2000, aep_1000=depth_1000,
                               pmp_depth=pmp_depth, pmp_aep=pmp_aep)
hill.fit_curve()
slope_ratio = hill.Sgc / hill.Sgap
if slope_ratio > 2.0:
    print('\nHill et al. (2000) method is outside the range of application')
else:
    print('\nHill et al. (2000) method is inside the range of application')

# Get the interpolations for GEV as per Sharpe (2024)
print('\nFitting the GEV curve...')
gev = GEV()
gev.setup_rainfall_boundaries(aep_2000=depth_2000, aep_1000=depth_1000,
                              pmp_depth=pmp_depth, pmp_aep=pmp_aep)
gev.fit_curve()

# Compute rainfall estimates
aeps = [1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000]
header = ['SW depth', 'Hill depth', 'GEV depth']
df = pd.DataFrame(index=aeps, columns=header)
for aep in aeps:
    df.loc[aep, 'SW depth'] = np.around(sw.get_quantile(aep), 1)
    df.loc[aep, 'Hill depth'] = np.around(hill.get_quantile(aep), 1)
    df.loc[aep, 'GEV depth'] = np.around(gev.get_quantile(aep), 1)
print('\nRainfall estimates:')
print(df)

# Plot the results
plot = df.plot(logx=True)
plt.xlabel('AEP (1 in X)')
plt.ylabel('Rainfall depth (mm)')
plt.show()
