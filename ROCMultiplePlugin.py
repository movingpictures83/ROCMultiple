
# matplotlib
import matplotlib.pyplot as plt
import matplotlib
plt.style.use('ggplot')
import pandas
from sklearn import metrics
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

colors = matplotlib.cm.Set1(range(10))


def plot_ROC(df, score_name, label_name, model_name, ax, color, pos_label):
    fpr, tpr, thresh = roc_curve(df[label_name], df[score_name], pos_label=pos_label)
    AUC = metrics.auc(fpr, tpr)
    ax.plot(fpr, tpr, linestyle='-',color=color, label=f'{model_name} (AUC={int(AUC*10000)/100})')

import PyIO
import PyPluMA
import pickle

class ROCMultiplePlugin:
    def input(self, inputfile):
       self.parameters = PyIO.readParameters(inputfile)
    def run(self):
        pass
    def output(self, outputfile):
        # At the moment this takes four files: Three datasets, and a set of other
        # Future will be to make that part flexible
        fig, ax = plt.subplots()
        if ("file1" in self.parameters):
           scores_df = pandas.read_csv(PyPluMA.prefix()+"/"+self.parameters["file1"])
           plot_ROC(scores_df, 'score', 'label', self.parameters["label1"], ax, colors[0], pos_label=0)
        if ("file2" in self.parameters):
           SCORES_MASIF=PyPluMA.prefix()+"/"+self.parameters["file2"]#"data/masif_test/MaSIF-Search_scores.csv"
           scores_masif = pandas.read_csv(SCORES_MASIF)
           plot_ROC(scores_masif, 'score', 'label', self.parameters["label2"], ax, colors[8], pos_label=0)
        if ("file3" in self.parameters):
           dMASIF_SCORES=PyPluMA.prefix()+"/"+self.parameters["file3"]#"data/masif_test/dmasif_out.csv"
           scores_dmasif = pandas.read_csv(dMASIF_SCORES)
           plot_ROC(scores_dmasif, 'avg_score', 'label', self.parameters["label3"], ax, colors[1], pos_label=1)
        OTHER_SCORES=PyPluMA.prefix()+"/"+self.parameters["other"]#"data/masif_test/Other_tools_SCORES.csv"

        other_labels = PyIO.readSequential(PyPluMA.prefix()+"/"+self.parameters["other_labels"])
        #scores_df = pandas.read_csv("PIsToN_scores.csv")

        if (OTHER_SCORES.endswith('csv')):
           scores_other = pandas.read_csv(OTHER_SCORES)
        else:
           oscore = open(OTHER_SCORES, "rb")
           scores_other = pickle.load(oscore)
           for mylabel in other_labels:
             scores_other[mylabel] = scores_other[mylabel].astype(float)

        #other_labels = ['FIREDOCK', 'AP_PISA', 'CP_PIE', 'PYDOCK_TOT', 'ZRANK2', 'ROSETTADOCK', 'SIPPER']
        pos_label = PyIO.readSequential(PyPluMA.prefix()+"/"+self.parameters["pos_label"])
        for j in range(len(pos_label)):
            pos_label[j] = int(pos_label[j])
        #pos_label = [0,0,1,0,0,0,1]
        colors_array = ['r', 'c', 'm', 'y', 'black', 'orange', 'tan']
        scores_other.to_csv("trevor.csv")
        for i in range(len(other_labels)):
          plot_ROC(scores_other, other_labels[i], 'Label', other_labels[i], ax, colors[i+2], pos_label=pos_label[i])



        # # title
        plt.title('AUC ROC curve')
        # x label
        plt.xlabel('False Positive Rate')
        # y label
        plt.ylabel('True Positive rate')

        plt.legend(loc='best')
        plt.savefig(outputfile,dpi=600)
        plt.show();

