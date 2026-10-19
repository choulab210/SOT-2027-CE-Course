"""Six reproducible 16:9 figures; saved results are validated before plotting."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
from sklearn.metrics import roc_curve
from .evaluation import metrics

BLUE, PURPLE, ORANGE, GRAY = '#0072B2','#8B5AA5','#D55E00','#596773'
NAMES = ['step1_initialize_network','step2_load_pretrained_weights',
         'step3_freeze_layers','step4_finetuning','figure5_training_vs_test','figure6_roc_curves']
MODELS = ['Random Forest','Scratch DNN','Transfer Learning']
COLORS = [GRAY, PURPLE, BLUE]

def style():
    plt.rcParams.update({'font.size':16,'axes.titlesize':24,'axes.labelsize':18,
                        'font.family':'DejaVu Sans','svg.fonttype':'none',
                        'figure.facecolor':'white','axes.spines.top':False,
                        'axes.spines.right':False})

def save(fig, folder, name):
    # Refuse overwrites, including generated assets.
    for ext in ['png','svg']:
        p=folder/f'{name}.{ext}'
        if p.exists(): raise FileExistsError(p)
        fig.savefig(p,dpi=300,facecolor='white')
    plt.close(fig)

def lock(ax,x,y):
    ax.add_patch(Rectangle((x-.011,y-.013),.022,.026,facecolor=GRAY))
    ax.add_patch(Arc((x,y+.012),.018,.025,theta1=0,theta2=180,color=GRAY,lw=2))

def network(ax,step, y=.47, scale=1.0, labels=True):
    xs=[.12,.31,.49,.69,.87]
    ns=[4,5,4,3,1]
    nodes=[np.linspace(y-.13*scale,y+.13*scale,n) if n>1 else [y] for n in ns]
    colors=[GRAY,BLUE,BLUE,ORANGE if step==4 else PURPLE,ORANGE if step==4 else PURPLE]
    for i in range(4):
        for a in nodes[i]:
            for b in nodes[i+1]:
                ax.plot([xs[i],xs[i+1]],[a,b],color='#CDD5DE',lw=.8,zorder=0)
    for i in range(5):
        for yy in nodes[i]:
            ax.add_patch(Circle((xs[i],yy),.014*scale,facecolor=colors[i],edgecolor='white',lw=1.5))
        if labels:
            titles=['Inputs\n7 descriptors','Shared 1\n256 + ReLU','Shared 2\n128 + ReLU',
                    'Task-specific hidden\n48 + ReLU','Output\n1 + sigmoid']
            ax.text(xs[i],y-.22,titles[i],ha='center',va='top',fontsize=15)
            if step>=3 and i in [1,2]:
                lock(ax,xs[i],y+.205)
                ax.text(xs[i],y+.245,'Frozen',ha='center',color=GRAY,fontsize=15)
            if step>=3 and i in [3,4]:
                ax.annotate('Updated' if step==4 else 'Trainable',xy=(xs[i],y+.04),
                            xytext=(xs[i],y+.245),ha='center',fontsize=15,color=colors[i],
                            arrowprops={'arrowstyle':'->','color':colors[i],'lw':2})
    return xs

def conceptual(folder):
    style()
    titles=['01  Initialize the neural network','02  Load pretrained nanoparticle weights',
            '03  Freeze the shared layers','04  Fine-tune on MNP observations']
    footers=['Shared feature extraction (blue)  |  Task-specific prediction head (purple)',
             'Reuse learned parameters instead of random initialization.',
             'Preserve pretrained shared layers; update task-specific layers.',
             'Adapt the prediction head using limited MNP data.']
    for step in range(1,5):
        fig,ax=plt.subplots(figsize=(16,9)); fig.subplots_adjust(left=0,right=1,top=1,bottom=0)
        ax.set(xlim=(0,1),ylim=(0,1)); ax.axis('off')
        ax.text(.055,.94,titles[step-1],fontsize=27,weight='bold',va='top')
        network(ax,step)
        if step==1:
            ax.text(.5,.79,'7 → 256 → 128 → 48 → 1',ha='center',fontsize=24,color=GRAY)
        if step==2:
            ax.text(.5,.84,'Pretrained nanoparticle DNN  →  transfer all 8 parameter tensors',ha='center',fontsize=20)
            network(ax,2,y=.755,scale=.22,labels=False)
            for x in [.31,.49,.69,.87]:
                ax.annotate('',xy=(x,.63),xytext=(x,.71),arrowprops={'arrowstyle':'->','lw':2,'color':ORANGE})
            ax.text(.12,.66,'MNP DNN',ha='center',fontsize=14)
        if step==4:
            ax.annotate('80 MNP training\nobservations',xy=(.12,.59),xytext=(.12,.78),
                        ha='center',fontsize=16,arrowprops={'arrowstyle':'->','color':GRAY,'lw':2})
        ax.text(.5,.13,footers[step-1],ha='center',fontsize=21)
        ax.text(.5,.065,'Representative neurons; actual dimensions labeled. Output: P(encoded class 1 = Negative).',
                ha='center',fontsize=13,color=GRAY)
        save(fig,folder,NAMES[step-1])

def validated_results(results):
    manifest=json.loads((results/'result_hashes.json').read_text())
    for name,digest in manifest.items():
        if hashlib.sha256((results/name).read_bytes()).hexdigest()!=digest:
            raise ValueError(f'Result integrity check failed: {name}')
    perf=pd.read_csv(results/'performance.csv')
    pred=pd.read_csv(results/'predictions.csv')
    for _,row in perf.iterrows():
        sub=pred[(pred.model==row.model)&(pred.partition==row.partition)]
        calculated=metrics(sub.y_true,sub.p_class1)
        for key in ['n','class0','class1','roc_auc','balanced_accuracy','mcc','tn','fp','fn','tp']:
            if not np.isclose(calculated[key],row[key],atol=1e-12,equal_nan=True):
                raise ValueError(f'Metric mismatch: {row.model}/{row.partition}/{key}')
    return perf,pred

def results_figures(results,folder):
    style(); perf,pred=validated_results(results)
    fig,ax=plt.subplots(figsize=(16,9)); fig.subplots_adjust(bottom=.22,top=.86,left=.10,right=.96)
    for j,(partition,color) in enumerate([('train',PURPLE),('test',BLUE)]):
        vals=[perf[(perf.model==m)&(perf.partition==partition)].roc_auc.iloc[0] for m in MODELS]
        bars=ax.bar(np.arange(3)+(j-.5)*.34,vals,.32,label=partition.title(),color=color)
        for b,v in zip(bars,vals):
            ax.text(b.get_x()+b.get_width()/2,v+.018,f'{v:.3f}',ha='center',fontsize=18)
    ax.set(xticks=np.arange(3),xticklabels=MODELS,ylim=(0,1.13),ylabel='ROC-AUC',
           title='05  Model fitting versus held-out performance')
    ax.legend(loc='upper center', bbox_to_anchor=(.5, 1.0), ncol=2); ax.grid(axis='y',alpha=.15); ax.set_axisbelow(True)
    fig.text(.5,.09,'N = 100 observations; train = 80, test = 20. Historical observation-level split.',ha='center',fontsize=16)
    fig.text(.5,.045,'Training performance alone does not establish predictive utility; study overlap and scaling leakage remain.',ha='center',fontsize=14)
    save(fig,folder,NAMES[4])
    fig,ax=plt.subplots(figsize=(16,9)); fig.subplots_adjust(bottom=.20,top=.87,left=.11,right=.95)
    for m,c in zip(MODELS,COLORS):
        sub=pred[(pred.model==m)&(pred.partition=='test')]
        if sub.y_true.nunique()==2:
            fpr,tpr,_=roc_curve(sub.y_true,sub.p_class1)
            a=metrics(sub.y_true,sub.p_class1)['roc_auc']
            ax.plot(fpr,tpr,lw=3,color=c,label=f'{m}: AUC = {a:.3f}')
        else: ax.plot([],[],color=c,label=f'{m}: AUC undefined')
    ax.plot([0,1],[0,1],'--',color='#999999',label='Chance reference')
    ax.set(xlim=(0,1),ylim=(0,1.03),xlabel='False positive rate',ylabel='True positive rate',
           title='06  Held-out ROC curves | same 20 observations')
    ax.legend(loc='lower right'); ax.grid(alpha=.15)
    fig.text(.5,.065,'Positive metric class = encoded 1 (CSV Negative). Single split; no uncertainty intervals.',ha='center',fontsize=16)
    save(fig,folder,NAMES[5])
    # Exact numerical inputs to the scientific figures, independently checkable.
    perf[['model','partition','roc_auc']].to_csv(folder/'figure5_values.csv',index=False)
    points=[]
    for m in MODELS:
        sub=pred[(pred.model==m)&(pred.partition=='test')]
        if sub.y_true.nunique()==2:
            fpr,tpr,threshold=roc_curve(sub.y_true,sub.p_class1)
            points.extend({'model':m,'fpr':f,'tpr':t,'threshold':h} for f,t,h in zip(fpr,tpr,threshold))
    pd.DataFrame(points).to_csv(folder/'figure6_values.csv',index=False)

def generate(results,folder):
    folder=Path(folder); folder.mkdir(parents=True,exist_ok=False)
    validated_results(Path(results))
    conceptual(folder); results_figures(Path(results),folder)

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--results',type=Path,default=Path('results'))
    p.add_argument('--out',type=Path,required=True); a=p.parse_args(); generate(a.results,a.out)
