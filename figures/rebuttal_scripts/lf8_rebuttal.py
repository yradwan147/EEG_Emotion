import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from common import *
from _lf_style import apply_lf_style, COLORS, save_dual, panel_label
apply_lf_style()
loo=np.array([A['loo'][t] for t in TAGS])
fig,axs=plt.subplots(1,2,figsize=(12,5.2),sharey=True)
info=[]
for ax,key,ck,lab,tt in zip(axs,['enc_test','enc_train'],['corr_enc_test_vs_loo','corr_enc_train_vs_loo'],['a','b'],
  ['Test-subject direction (as in original analysis)','Training-subject direction (stricter)']):
    x=np.array([A[key][t] for t in TAGS]); c=A[ck]
    r,p=pearsonr(x,loo); assert abs(r-c['pearson_r'])<1e-6 and abs(p-c['pearson_p'])<1e-6
    info.append((key,c['pearson_r'],c['pearson_p'],c['boot_ci95']))
    z=np.polyfit(x,loo,1); xl=np.linspace(x.min()-.01,x.max()+.01,50)
    ax.plot(xl,np.polyval(z,xl),'k-',lw=1.6,alpha=.65,zorder=2)
    for m,msk,nm,col in [('s',orig,'original seeds (n=5)',COLORS['darkblue']),('o',~orig,'new seeds (n=15)',COLORS['blue'])]:
        ax.scatter(x[msk],loo[msk],marker=m,s=110,c=col,edgecolors='white',linewidths=1,zorder=3,label=nm)
    ax.axhline(0,color='k',lw=.6,ls=':')
    ax.text(0.04,0.97,f"r = {c['pearson_r']:+.2f}, p = {c['pearson_p']:.3f}\n95% boot CI [{c['boot_ci95'][0]:+.2f}, {c['boot_ci95'][1]:+.2f}]\nn = 20",
            transform=ax.transAxes,va='top',fontsize=11,fontweight='bold',bbox=dict(boxstyle='round',fc='white',ec='#ccc'))
    ax.set_xlabel('residual encoding $|r|$ ('+('test' if key=='enc_test' else 'training')+' subjects)',fontsize=10.5)
    ax.set_title(tt,loc='left',fontsize=11); panel_label(ax,lab,x=-0.12 if lab=='b' else -0.15,y=1.04)
axs[0].set_ylabel('leave-one-out ensemble contribution $\\Delta$ BACC',fontsize=10.5)
axs[1].legend(loc='lower left',fontsize=9,frameon=False)
fig.suptitle('Residual encoding vs. ensemble value, 20 independent checkpoints',fontsize=12.5,fontweight='bold')
plt.tight_layout(); save_dual(fig,f'{OUT}/lf8_two_tier_ensemble_theory'); print(info)
