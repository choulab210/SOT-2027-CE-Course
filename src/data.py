"""Historical N=100 sampling and pre-split scaling; NOT leakage-free evaluation."""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

FEATURES = ['Coating','Shape','Dose','Size','Exposure Time','HOMO Energy','LUMO Energy']
# Published notebook constants; comments say eV, but unit provenance is unverified.
ORBITALS = {
    'PE': (-0.30393261512793585, 0.11592184908302908),
    'PP': (-0.2938916146961782, 0.10272616946283625),
    'PVC': (-0.2886950926400236, 0.002629107190461072),
    'PS': (-0.23323174962813908, 0.0022633605291856283),
    'PET': (-0.23589308197284242, -0.08382145000478655)}

def prepare_data(path):
    raw = pd.read_csv(path)
    raw['_source_row'] = np.arange(len(raw))
    required = ['Polymer type','Surface functionalization','Size (nm)',
                'Dose (μg/mL)','Shape','Exposure time (h)','Class']
    raw = raw.dropna(subset=required)
    if not set(raw['Class']).issubset({'Negative','Positive'}):
        raise ValueError('Unknown label')
    # Polymer concatenation order matters to the seed-42 sample.
    other = pd.concat([raw[raw['Polymer type']==p] for p in ['PET','PVC','PP']])
    pspe = pd.concat([raw[raw['Polymer type']==p] for p in ['PS','PE']])
    def sample(group, label, n):
        return group[group['Class']==label].sample(n=n, random_state=42)
    ds = pd.concat([sample(pspe,'Negative',33), sample(pspe,'Positive',35),
                    sample(other,'Negative',27), sample(other,'Positive',5)])
    ds = ds.sample(frac=1, random_state=42).reset_index(drop=True)
    if (ds[['Size (nm)','Dose (μg/mL)']].astype(float) <= 0).any().any():
        raise ValueError('Log transforms require positive values')
    x = pd.DataFrame({'Coating': (ds['Surface functionalization']!='Pristine').astype(int),
                      'Shape': (ds['Shape']!='Spherical').astype(int)})
    x['Dose'] = np.log10(ds['Dose (μg/mL)'].astype(float))
    x['Size'] = np.log10(ds['Size (nm)'].astype(float))
    x['Exposure Time'] = ds['Exposure time (h)'].astype(float)/24
    for i,col in enumerate(['HOMO Energy','LUMO Energy']):
        x[col] = ds['Polymer type'].map(lambda p: ORBITALS[p][i])
    ranges = {}
    for col in FEATURES[2:]:
        lo, hi = float(x[col].min()), float(x[col].max())
        if hi == lo: raise ValueError(f'Constant scaling feature: {col}')
        ranges[col] = {'min':lo,'max':hi}
        x[col] = (x[col]-lo)/(hi-lo)  # Historical leakage deliberately retained.
    y = (ds['Class']=='Negative').astype(int)
    train, test = train_test_split(np.arange(len(ds)), test_size=0.2, random_state=42)
    ds['partition'] = 'train'
    ds.loc[test,'partition'] = 'test'
    assert list(x.columns)==FEATURES and np.isfinite(x.to_numpy()).all()
    overlap = {col: len(set(ds.loc[train,col]) & set(ds.loc[test,col]))
               for col in ['Reference DOI','Particle ID','Article ID']}
    overlap['identical_feature_vectors'] = len(set(map(tuple,x.loc[train].to_numpy())) &
                                             set(map(tuple,x.loc[test].to_numpy())))
    return {'rows':ds,'x':x,'y':y,'train':train,'test':test,
            'scaling':ranges,'overlap':overlap}
