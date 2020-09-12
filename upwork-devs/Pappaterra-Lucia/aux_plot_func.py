import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph


# Colors
a,b,c,d,e,f,g,h,i,j,k,l,m = [plt.cm.tab20(0), plt.cm.tab20(2), 
                             plt.cm.tab20(4), plt.cm.tab20(6), 
                             plt.cm.tab20(8), plt.cm.tab20(10), 
                             plt.cm.tab20(12), plt.cm.tab20(14), 
                             plt.cm.tab20(16), plt.cm.tab20(18), 
                             plt.cm.tab20(7), plt.cm.tab20(11), 
                             plt.cm.tab20(5)]


def graph(df):
    g = Digraph('OrgChart', filename='org_chart.gv')

    for p, i in zip(df['project_name'], range(len(df))):
        g.node(p, color='red')
    
        pm = df[df['project_name'] == p]['project_manager'][i]  
        rnr = df[df['project_name'] == p]['resource_and_responsibility'][i]
    
        if isinstance(rnr, list):
            rnr = "\n".join(rnr)
        if rnr != None:
            g.node(rnr, color='green', shape='rectangle')
    
        if isinstance(pm, list):
            for elem in pm:
                g.node(elem, color='blue')
                g.edge(p, elem)
                if rnr != None:
                    g.edge(elem, rnr)
        else:
            g.node(pm, color='blue')
            g.edge(p, pm)
            if rnr != None:
                g.edge(pm, rnr)
    return g
    

def bar_plot(df):
    proj = list(df['project_name'])
    rnr = list(df['resource_and_responsibility'])
    rnr_counts=[]  
    for elem in rnr:
        if elem is not None:
            rnr_counts.append(len(elem))
        else:
            rnr_counts.append(0)
            
      
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    langs = proj
    students = rnr_counts
    ax.bar(langs, students, color=(a,b,c,d,e,f,g,h,i,j,k,l,m))
       
    # Make some labels
    labels = [str(elem) for elem in rnr_counts]
    rects = ax.patches

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height, label,
                ha='center', va='bottom')
    
    
    plt.title('Amount of resources per project', fontsize=20)
    plt.xticks(rotation=90)
    plt.show()


def pie_chart(df):
    rnr = list(df['resource_and_responsibility'])
    rnr_size = []
    for elem in rnr:
        if isinstance(elem, list):
            n = len(elem) + 1
            rnr_size.append(n)
        elif elem==None:
            rnr_size.append(1)   
        else:
            rnr_size.append(2)

    group_names = list(df['project_name'])
    group_size = rnr_size

    pms = list(df['project_manager'])
    pms_size = []
    for elem in pms:
        if isinstance(elem, list):
            n = len(elem) 
            pms_size.append(n) 
        else:
            pms_size.append(1) 

    for elem in pms:
        if isinstance(elem, list):
            n = pms.index(elem)
            for e, i in zip(elem, range(n, n + len(elem))):
                pms.insert(i, e)
            pms.remove(elem)

    subgroup_names = pms
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
    a,b,c,d,e,f,g,h,i,j,k,l,m = [plt.cm.tab20(0), plt.cm.tab20(2), 
                                plt.cm.tab20(4), plt.cm.tab20(6), 
                                plt.cm.tab20(8), plt.cm.tab20(10), 
                                plt.cm.tab20(12), plt.cm.tab20(14), 
                                plt.cm.tab20(16), plt.cm.tab20(18), 
                                plt.cm.tab20(7), plt.cm.tab20(11), 
                                plt.cm.tab20(5)]

    # First Ring (Inside)
    mypie, _ = ax.pie(group_size, radius=1-0.3,
                      colors=[a, b, c, d, e, f, g, h, i, j, k, l, m])
    plt.setp(mypie, width=0.3, edgecolor='white')
 
    # Second Ring (Outside)
    mypie2, _ = ax.pie(subgroup_size, radius=1, 
                       #labels=subgroup_names, labeldistance=0.7, 
                       colors=[a, b, c, c, d, e, e, f, f, g, h, i, j, k, l, m])
    plt.setp(mypie2, width=0.4, edgecolor='white')

    ax.legend(mypie, group_names,
              title="Projects",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")
      
    total_res = 0           
    for elem in rnr:
        if isinstance(elem, list):
            n = len(elem) 
            total_res += n
        elif elem==None:
            pass          
        else:
            total_res += 1
                    
              
    resources = []
    for elem in rnr:
        if isinstance(elem, list):
            n = len(elem) 
            resources.append(str(n) + ' resources ({d}%)'.format(d=round(n/total_res*100)))
        elif elem==None:
            resources.append('0 resources (0%)')  
        else:
            resources.append('1 resource ({d}%)'.format(d=round(1/total_res*100))) 

    for i, p in enumerate(mypie):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(resources[i], xy=(x, y), xytext=(1.15*np.sign(x), 
                    1.25*y), horizontalalignment=horizontalalignment, **kw)
 
    plt.margins(0,0)    

    # show it
    plt.show()   
