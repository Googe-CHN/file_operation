import matplotlib.pyplot as plt
import numpy as np
 
 
iter_loss = []
Loss = []

Loss_box_reg = []

Loss_classifier = []

Loss_pkp = []

Loss_mask = []

Loss_mty = []

Loss_objectness = []

Loss_rpn_box_reg = []
with open('/home/birl/Data/PoleDet/results/1104-keypoint/log-1.txt','r') as file:  #打开文件
    for line in file.readlines():    #文件内容分析成一个行的列表
        line = line.strip().split(" ")   #按照空格进行切分
        #print(line)
        itera, loss, loss_box_reg, loss_classifier, loss_pkp, loss_mask, loss_objectness, loss_rpn_box_reg = \
            line[8], line[11], line[15], line[19], line[23], line[27], line[31], line[35]    #一行拆分为三行
        itera = int(itera)  #保留itera参数
        iter_loss.append(itera)    #保存在数组中

        loss = float(loss)
        Loss.append(loss)

        loss_box_reg = float(loss_box_reg)
        Loss_box_reg.append(loss_box_reg)

        loss_classifier = float(loss_classifier)
        Loss_classifier.append(loss_classifier)

        loss_pkp = float(loss_pkp)
        Loss_pkp.append(loss_pkp)

        loss_mask = float(loss_mask)
        Loss_mask.append(loss_mask)

        loss_objectness = float(loss_objectness)
        Loss_objectness.append(loss_objectness)


        loss_rpn_box_reg = float(loss_rpn_box_reg)
        Loss_rpn_box_reg.append(loss_rpn_box_reg)

#画图
plt.title('Loss')  #标题
#plt.plot(x,y)
#常见线的属性有：color,label,linewidth,linestyle,marker等
plt.plot(iter_loss, Loss, color='cyan', label='Loss')
plt.plot(iter_loss, Loss_box_reg, color='blue', label='Loss_box_reg')
plt.plot(iter_loss, Loss_classifier, color='darkgreen', label='Loss_classifier')
plt.plot(iter_loss, Loss_pkp, color='deeppink', label='Loss_pke')
plt.plot(iter_loss, Loss_mask, color='firebrick', label='Loss_mask')
plt.plot(iter_loss, Loss_objectness, color='mediumaquamarine', label='Loss_objectness')
plt.plot(iter_loss, Loss_rpn_box_reg, color='olive', label='Loss_rpn_box_reg')
 
plt.legend()  #显示上面的label
plt.xlabel('Iteration')
plt.ylabel('loss')
 
#plt.ylim(-1,1)#仅设置y轴坐标范围
plt.show()