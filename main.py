# -*- coding: gbk -*-
import jieba
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import networkx as nx
from wordcloud import WordCloud
import random

FILE_PATH='童年.txt'
STOPWORDS_PATH='stop_words.txt'
OUTPUT_FREQ_WORD_NUM=500
NAME_FILE_PATH='name.txt'
MAX_NODE_SIZE=3000
MIN_NODE_SIZE=600

def read_file():
    file=open(FILE_PATH,'r',encoding='utf-8')
    with file:
        string=file.read()
    list_words=jieba.lcut(string)
    list_section0 = string.split('\n'*2)
    list_section=[''for _ in range(411)]
    w=0
    string=''
    for i in range(4101):
        list_section[w]=list_section[w]+list_section0[i]
        if i%10==0:
            w+=1
    return list_words,list_section
def read_stopwords_file():
    file=open(STOPWORDS_PATH,'r',encoding='utf-8')
    list_stopwords=[]
    for line in file:
        list_stopwords.append(line.strip())
    return list_stopwords
def same_word(word):
    samewordic = {'妈妈': 0,'爸爸':1,'老太婆':2,'老爷':3,'我':4}
    replacelst = ['母亲', '父亲','老婆子','姥爷','阿廖沙']
    if word in samewordic:word=replacelst[samewordic[word]]
    return word
def word_freq(list_words):
    list_stopwords=read_stopwords_file()
    dict_count={}
    for word in list_words:
        if len(word)==1:continue
        word=same_word(word)
        dict_count[word]=dict_count.get(word,0)+1
    for stopword in list_stopwords:dict_count.pop(stopword,None)
    list_count=list(dict_count.items())
    list_count.sort(key=lambda  item:item[1],reverse=True)
    output_freq(list_count[:OUTPUT_FREQ_WORD_NUM])
    return list_count
def output_freq(list_count):
    split_name=FILE_PATH.rsplit('.',1)
    file_path=split_name[0]+'_词频'+'.txt'
    file=open(file_path,'w',encoding='utf-8')
    for word,freq in list_count:
        file.write('{}    {}\n'.format(word,freq))

#画词云图
def cloud_figure_config(title):
    plt.switch_backend('TKAgg')
    mng=plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.figure(num=title)
    plt.axis('off')

def make_cloud(list_count):
    mask_pic=mpimg.imread('百合.jpg')
    cloud=WordCloud('deng.ttf',
                    max_words=600,
                    background_color='white',
                    scale=3,
                    mask=mask_pic,
                    colormap=plt.get_cmap('brg')
                    )
    cloud.fit_words(dict(list_count))
    split_name=FILE_PATH.rsplit('.',1)
    title=split_name[0]+'_词云图'
    cloud.to_file(title+'.png')
    cloud_figure_config(title)
    plt.imshow(cloud)
    plt.show()

#人物关系图
def is_name_in_section(list_section):
    dict_relations = {}
    namelst = read_name_file()
    for line in list_section:
        for name1 in namelst:
            name1=same_word(name1)
            if name1 in line:
                for name2 in namelst:
                    name2=same_word(name2)
                    if name1 == name2:
                        continue
                    elif name2 in line:
                        dict_relations[(name1, name2)] = dict_relations.get((name1, name2), 0) + 1
            else:continue
    return dict_relations

def read_name_file():
    file=open(NAME_FILE_PATH,'r',encoding='utf-8')
    list_name=[]
    for name in file:
        list_name.append(name.strip())
    return list_name

def get_relation_list(dict_relations):
    list_relation=[]
    for relation, freq in dict_relations.items():
        list_relation.append([relation[0], relation[1], freq])
    list_relation.sort(key=lambda item: item[2], reverse=True)
    max_relation = list_relation[0][2]
    for item in list_relation:
        item[2] = item[2] / max_relation
    return list_relation
def relation_figure_config():
    split_name=FILE_PATH.rsplit('.',1)
    title=split_name[0]+'_人物关系网络图'
    plt.switch_backend('TkAgg')
    plt.subplots_adjust(left=0,right=1,bottom=0,top=0.95)
    plt.axis('off')
    plt.figure(num=title)
    plt.title(title,fontfamily='Microsoft Yahei',fontsize=20,color='blue',fontweight=1000,pad=-10,)
def node_size(G):
    list_totle_relation=[]
    for nodex in G.nodes():
        relation=0
        for nodey in G.neighbors(nodex):
            relation+=G[nodex][nodey]['weight']
        list_totle_relation.append(relation**0.5)
    max_relation=max(list_totle_relation)
    min_relation = min(list_totle_relation)
    relation_range=max_relation-min_relation
    size_range=MAX_NODE_SIZE-MIN_NODE_SIZE
    list_node_size=[]
    for relation in list_totle_relation:
        size=size_range*(relation-min_relation)/relation_range#+MIN_NODE_SIZE
        list_node_size.append(size)
    return list_node_size

def draw_nodes(G,position,list_node_size):
    list_node_color=node_color(G)
    nx.draw_networkx_nodes(G,
                           pos=position,
                           node_size=list_node_size,
                           node_color=list_node_color,
                           cmap=plt.get_cmap('hsv'),
                           edgecolors='white',
                           linewidths=1,)
def draw_edges(G,positon):
    list_edge_width,list_edge_color,list_edge_style=edge_config(G)
    nx.draw_networkx_edges(G,
                           pos=positon,
                           width=list_edge_width,
                           style=list_edge_style,
                           edge_color=list_edge_color)
def node_color(G):
    list_node_color=[]
    for i in range(G.order()):
        list_node_color.append(i)
    random.shuffle(list_node_color)
    return  list_node_color
def edge_config(G):
    list_edge_width=[]
    list_edge_style=[]
    list_edge_color=[]
    for nodex,nodey in G.edges():
        if G[nodex][nodey]['weight']==1.0:
            list_edge_width.append(4)
            list_edge_style.append('solid')
            list_edge_color.append('red')###错误：style和color颠倒
        elif 0.6<=G[nodex][nodey]['weight']<1.0:
            list_edge_width.append(4)
            list_edge_style.append('dotted')
            list_edge_color.append('red')
        elif 0.3 <= G[nodex][nodey]['weight'] < 0.6:
            list_edge_width.append(4)
            list_edge_style.append('dotted')
            list_edge_color.append('red')
        elif 0.1 <= G[nodex][nodey]['weight'] < 0.3:
            list_edge_width.append(3)
            list_edge_style.append('solid')
            list_edge_color.append('red')
        elif 0.05 <= G[nodex][nodey]['weight'] < 0.1:
            list_edge_width.append(2)
            list_edge_style.append('solid')
            list_edge_color.append('blue')
        elif 0.01 <= G[nodex][nodey]['weight'] < 0.05:
            list_edge_width.append(1)
            list_edge_style.append('solid')
            list_edge_color.append('yellow')
        else:
            list_edge_width.append(1)
            list_edge_style.append('dotted')
            list_edge_color.append('darkgrey')
    return  list_edge_width,list_edge_color,list_edge_style
def draw_labels(G,position,list_node_size):
    dict_bbox={'facecolor':'white',
               'edgecolor':'None',
               'alpha':0.5,
               'boxstyle':'Round,pad=0.1'}
    i=0
    for node in G.nodes():
        size=list_node_size[i]**0.3*2
        i+=1
        nx.draw_networkx_labels(G,
                               pos=position,
                               labels={node:node},
                               font_size=size,
                               bbox=dict_bbox,
                               font_weight=1000,)
def draw(list_section):
    G=nx.Graph()
    dict_relations=is_name_in_section(list_section)
    list_relation=get_relation_list(dict_relations)
    G.add_weighted_edges_from(list_relation)
    position=nx.spring_layout(G)
    relation_figure_config()
    list_node_size=node_size(G)
    draw_nodes(G,position,list_node_size)
    draw_edges(G,position)
    draw_labels(G,position,list_node_size)
    plt.show(block=True)

if __name__=='__main__':
    plt.rcParams['font.sans-serif']=['dengxian']
    plt.rcParams['font.serif']=['dengxian']
    list_words,list_section=read_file()
    list_count=word_freq(list_words)
    make_cloud(list_count[:OUTPUT_FREQ_WORD_NUM])
    draw(list_section)
