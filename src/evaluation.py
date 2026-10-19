"""Metrics for encoded class 1 = CSV Negative, not verified toxic-positive."""
import numpy as np
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, matthews_corrcoef, confusion_matrix

def metrics(y, probability):
    y, p = np.asarray(y).ravel(), np.asarray(probability).ravel()
    if len(y)!=len(p) or not len(y) or not np.isfinite(p).all() or ((p<0)|(p>1)).any():
        raise ValueError('Invalid predictions')
    pred = (p>0.5).astype(int)  # Original neural threshold; RF ties also select class 0.
    two_classes = len(np.unique(y))==2
    cm = confusion_matrix(y,pred,labels=[0,1])
    tn,fp,fn,tp = map(int,cm.ravel())
    # MCC denominator vanishes for constant true labels OR constant predictions.
    mcc_defined = two_classes and len(np.unique(pred))==2
    return {'n':len(y),'class0':int((y==0).sum()),'class1':int((y==1).sum()),
            'roc_auc':float(roc_auc_score(y,p)) if two_classes else np.nan,
            'balanced_accuracy':float(balanced_accuracy_score(y,pred)) if two_classes else np.nan,
            'mcc':float(matthews_corrcoef(y,pred)) if mcc_defined else np.nan,
            'tn':tn,'fp':fp,'fn':fn,'tp':tp,
            'constant_probability':bool(np.ptp(p)==0),
            'collapsed_classes':bool(len(np.unique(pred))==1),
            'metric_note': ('single true class: AUC/BA/MCC undefined' if not two_classes else
                            'constant predicted class: MCC undefined' if not mcc_defined else 'defined')}
