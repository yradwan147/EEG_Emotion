import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from common import *
from _lf_style import apply_lf_style, COLORS, save_dual, panel_label
apply_lf_style()
x=np.array([R[t]['enc_train']['best_pc_abs_r'] for t in TAGS])
S={}
for k in ['ablate_v_train','ablate_v_orth']:
    d=np.array([R[t][k]['delta'] for t in TAGS]); nm=np.array([R[t][k]['null_mean'] for t in TAGS])
    sd=np.array([R[t][k]['null_sd'] for t in TAGS]); z=np.array([R[t][k]['z'] for t in TAGS]); pe=np.array([R[t][k]['p_emp'] for t in TAGS])
    S[k]=dict(d=d,nm=nm,sd=sd,z=z,drop=int((d<0).sum()),belowmin=int((pe<=1/51+1e-9).sum()),meand=d.mean(),meanz=z.mean())
    print(k,S[k]['drop'],S[k]['belowmin'],round(S[k]['meand'],4),round(S[k]['meanz'],2))
assert (S['ablate_v_train']['drop'],S['ablate_v_train']['belowmin'])==(20,20)
assert (S['ablate_v_orth']['drop'],S['ablate_v_orth']['belowmin'])==(18,14)
assert round(S['ablate_v_train']['meanz'],1)==-8.4 and round(S['ablate_v_orth']['meanz'],1)==-4.0
r,p=pearsonr(x,S['ablate_v_train']['d']); print('r,p',r,p); assert abs(r-0.35)<0.01 and abs(p-0.13)<0.01
fig,axs=plt.subplots(1,2,figsize=(11.5,4.6),sharey=True)
for ax,k,lab,col,L in zip(axs,S,['a','b'],[COLORS['red'],COLORS['blue']],
   [r'train-fit direction $v_{\rm train}$',r'orthogonalised direction $v_{\rm orth}$']):
    s=S[k]
    ax.errorbar(x,s['nm'],yerr=2*s['sd'],fmt='none',ecolor='#888',elinewidth=1.4,capsize=2.5,zorder=2)
    ax.scatter(x,s['nm'],marker='_',s=40,c='#888',zorder=2,label=r'random-direction null (mean $\pm$2 sd, 50 draws)')
    for m,msk,nm in [('s',orig,'original seeds (n=5)'),('o',~orig,'new seeds (n=15)')]:
        ax.scatter(x[msk],s['d'][msk],marker=m,s=70,c=col,edgecolors='white' if m=='o' else 'black',linewidths=.9,zorder=4,label=nm)
    ax.axhline(0,color='k',lw=.6,ls=':')
    ax.set_xlabel(r'residual encoding $|r|$ (train-subject fit)')
    ax.set_title(L,loc='left',fontsize=10.5); panel_label(ax,lab,x=-0.12 if lab=='b' else -0.16,y=1.04)
    txt=(f"mean $\\Delta$BACC = {s['meand']*100:+.2f} pts\ndrop: {s['drop']}/20\nbelow null min: {s['belowmin']}/20\nmean z = {s['meanz']:.1f}")
    ax.text(0.97,0.04,txt,transform=ax.transAxes,ha='right',va='bottom',fontsize=8.5,bbox=dict(boxstyle='round',fc='white',ec='#ccc'))
axs[0].set_ylabel(r'$\Delta$BACC under ablation (negative = hurts)')
axs[0].text(0.03,0.97,f"drop vs enc: r={r:.2f}, p={p:.2f}",transform=axs[0].transAxes,va='top',fontsize=9,bbox=dict(boxstyle='round',fc='white',ec='#ccc'))
axs[0].set_ylim(-0.036,0.008)
h,l=axs[0].get_legend_handles_labels()
fig.legend(h,l,loc='lower center',ncol=3,fontsize=8.5,frameon=False)
fig.suptitle('Causal ablation across 20 independent checkpoints',fontsize=12,fontweight='bold')
plt.tight_layout(rect=(0,0.06,1,1)); save_dual(fig,f'{OUT}/lf16_causal_ablation')
