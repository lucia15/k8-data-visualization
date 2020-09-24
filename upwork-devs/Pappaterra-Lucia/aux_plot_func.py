import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph


# Colors
a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,aa,bb,cc,dd,ee,ff,gg = [plt.cm.tab20(0), 
        plt.cm.tab20(2), plt.cm.tab20(4), plt.cm.tab20(6), plt.cm.tab20(8), 
        plt.cm.tab20(10), plt.cm.tab20(12), plt.cm.tab20(14), plt.cm.tab20(16), 
        plt.cm.tab20(18), plt.cm.tab20(1), plt.cm.tab20(3), plt.cm.tab20(5), 
        plt.cm.tab20(7), plt.cm.tab20(9), plt.cm.tab20(11), plt.cm.tab20(13), 
        plt.cm.tab20(15), plt.cm.tab20(17), plt.cm.tab20(19), plt.cm.tab20(0), 
        plt.cm.tab20(2), plt.cm.tab20(4), plt.cm.tab20(6), plt.cm.tab20(8), 
        plt.cm.tab20(10), plt.cm.tab20(12), plt.cm.tab20(14), plt.cm.tab20(16), 
        plt.cm.tab20(18), plt.cm.tab20(1), plt.cm.tab20(3), plt.cm.tab20(5)]


def graph(df, df2):
    df['delivery_manager'].replace('', float("NaN"), inplace=True)
    df['delivery_manager'].fillna('No Delivery Managers yet', inplace=True)

    g = Digraph('OrgChart', filename='org_chart.gv')
   
    for p in df['project_name']:
        g.node(p, color='red')
    
        pm = df[df['project_name'] == p]['delivery_manager'].values[0]       
        if pm=='':
            pm = []
        else:
            pm = pm.split(', ')   
         
        rnr = list(df2[df2['project_name'] == p]['resource'])
        
        if len(rnr)>0:
            rnr = "\n".join(rnr)
            g.node(rnr, color='green', shape='rectangle')
    
            for elem in pm:
                g.node(elem, color='blue')
                g.edge(p, elem)
                if rnr is not None:
                    g.edge(elem, rnr)
    
    # save graph to pdf                
    g.render('outputs/teams_graph.gv', view=True)
    
    return g
    

def bar_plot(df, df2):

    proj = list(df['project_name'])
    
    rnr = []
    for pr in proj:
        rnr.append(list(df2[df2['project_name']==pr]['resource']))
        
    rnr_counts=[]  
    for elem in rnr:
        rnr_counts.append(len(elem))

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    langs = proj
    
    ax.bar(langs, rnr_counts, color=(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,aa,bb,cc,dd,ee,ff,gg))
       
    # Make some labels
    labels = [str(elem) for elem in rnr_counts]
    rects = ax.patches

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')    
    
    plt.title('Amount of resources per project', fontsize=20)
    plt.xticks(rotation=90)
    plt.savefig('outputs/bar_plot.png' , format='png', bbox_inches = 'tight')  
    plt.show()


def pie_chart(df, df2):
    df['delivery_manager'].replace('', float("NaN"), inplace=True)
    df['delivery_manager'].fillna('No Delivery Managers yet', inplace=True)  

    proj = list(df['project_name'])
    
    rnr = []
    for p in proj:
        rnr.append(list(df2[df2['project_name']==p]['resource']))  
    
    pms = convert_to_lists(df['delivery_manager'])
    
    rnr_size = []
    pms_size = []
    group_names = []    
    
    for elem, elem2, elem3 in zip(rnr, pms, proj):
        n = len(elem) 
        if n>0:
            rnr_size.append(n)           
            m = len(elem2) 
            pms_size.append(m)
            group_names.append(elem3)       
            
    group_size = rnr_size

    subgroup_size = []
    for i, j in zip(rnr_size, pms_size):
        if j == 1:
            subgroup_size.append(i)
        else:
            for x in range(j):
                subgroup_size.append(i/j)
 
    fig, ax = plt.subplots(figsize=(12,7))
    ax.set_title("GlassWall Projects \nResources proportion", fontsize=20)

    ax.axis('equal')
    
    # Colors
    # Colors
    a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,aa,bb,cc,dd,ee,ff,gg = [plt.cm.tab20(0), 
        plt.cm.tab20(2), plt.cm.tab20(4), plt.cm.tab20(6), plt.cm.tab20(8), 
        plt.cm.tab20(10), plt.cm.tab20(12), plt.cm.tab20(14), plt.cm.tab20(16), 
        plt.cm.tab20(18), plt.cm.tab20(1), plt.cm.tab20(3), plt.cm.tab20(5), 
        plt.cm.tab20(7), plt.cm.tab20(9), plt.cm.tab20(11), plt.cm.tab20(13), 
        plt.cm.tab20(15), plt.cm.tab20(17), plt.cm.tab20(19), plt.cm.tab20(0), 
        plt.cm.tab20(2), plt.cm.tab20(4), plt.cm.tab20(6), plt.cm.tab20(8), 
        plt.cm.tab20(10), plt.cm.tab20(12), plt.cm.tab20(14), plt.cm.tab20(16), 
        plt.cm.tab20(18), plt.cm.tab20(1), plt.cm.tab20(3), plt.cm.tab20(5)]
    
    colors=[]
    pms2 = []     
    for cr, i in zip([a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,aa,bb,cc,dd,ee,ff,gg], range(len(rnr))):
        rs = rnr[i]           
        if len(rs)>0:
            colors.append(cr)
            pms2.append(pms[i])
           
    # First Ring (Inside)
    mypie, _ = ax.pie(group_size, radius=1-0.3, colors=colors) #radius=
    plt.setp(mypie, width=0.4, edgecolor='white')
   
    
    colors_=[]
    for cr, pr, j in zip(colors, group_names, range(len(pms2))):
        pm = pms2[j]
        if len(pm)>0:
            colors_ = colors_ + [cr] * len(pm)
        else:
            colors_ = colors_ + [cr]    
    
    # Second Ring (Outside)
    mypie2, _ = ax.pie(subgroup_size, radius=1, colors=colors_)                        
    plt.setp(mypie2, width=0.4, edgecolor='white')

    ax.legend(mypie, group_names,
              title="Projects",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")
     
    total_res = sum(rnr_size)
                                 
    resources = []
    for elem in rnr_size:
        resources.append(str(elem) + ' resources ({d}%)'.format(d=round(elem/total_res*100)))
    
    for i, p in enumerate(mypie):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(resources[i], xy=(x, y), xytext=(1.2*np.sign(x), 1.1*y), 
            horizontalalignment=horizontalalignment, **kw)
 
    plt.margins(0,0)  
    
    plt.savefig('outputs/pie_chart.png' , format='png', bbox_inches = 'tight')  

    # show it
    plt.show() 
    
    
def convert_to_lists(df_col):
    ll=[]
    for elem in df_col:
        if elem=='':
            ll.append([]) 
        else:
            ll.append(elem.split(', '))
    return list(ll)  