import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import jieba
from wordcloud import WordCloud

def cloud(data, number, picture):
    path_of_font = './word/DroidSansFallbackFull.ttf'
    outfile = open('./word/ciyun.txt', 'w', encoding='utf-8')
    for eachline in [i for i in data[:, number]]:
        outfile.write(eachline)

    outfile.close()
    text_from_file_with_path = open('./word/ciyun.txt', encoding='utf-8').read()
    wordlist_after_jieba = jieba.cut(text_from_file_with_path, cut_all=True)
    wl_space_split = ' '.join(wordlist_after_jieba)
    if picture == 1:
        mask = np.array(Image.open('./picture/男人.jpg'))
    else:
        mask = np.array(Image.open('./picture/女人.jpg'))
    my_wordcloud = WordCloud(font_path=path_of_font, mask=mask, background_color='white', max_font_size=60).generate(wl_space_split)
    plt.figure(num='网易云课堂数据分析助手', figsize=(7, 6))
    plt.imshow(my_wordcloud)
    plt.axis('off')
    plt.show()
