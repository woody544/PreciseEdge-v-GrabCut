#!/usr/MJ/gcvpe_venv python3
# March 4, 2022
# MJ WOODWARD-GREENE

# imports

# data in/out, wrangling
import pandas as pd
import os

# GUIs, user input, warnings
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

# Statistics and Visualizations
from scipy.stats import kstest
from scipy.stats import ks_2samp
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns


def main():

    root = tk.Tk()
    root.title('ROOT')
    root.overrideredirect(0)
    root.attributes('-topmost', True)
    root.withdraw()

    return None

        

class Correlate_within_one_PEoutput_csv(tk.Frame):    
 
    '''
    PreciseEdge csv Output data Statistical Analyses:
    COMPARES VALUES WITHIN ONE PRECISE-EDGE CSV OUTPUT FILE WITH MANUAL DATA COLUMNS ADDED. CONVERTS TO DF.
    Correlate selected variables within a df to each other.
    Data file in repo is 'AdaptMapReport-GC-with-manualMeasures.csv' OR 'AdaptMapReport-PE-with-manualMeasures.csv'.
    '''

    def __init__(self,):

        super().__init__()

        # User select csv file, make df
        self.file_path = os.path.abspath(filedialog.askopenfilename())
        print(self.file_path)
        
        self.head, tail = os.path.split(self.file_path)
        self.head = os.path.sep.join([self.head, 'plots-stats'])
        self.outstrokes = os.path.sep.join([self.head, 'GCvsPEtests.txt'])
        print('outstrokes', self.outstrokes)

        self.df = pd.read_csv(self.file_path, header=0)
        self.df_columns = list(self.df.columns)

        nocorrs = ['sampleID', 'allphotos','crosschk']

        try: 
            for val in nocorrs:
                self.df_columns.remove(val)
        except (ValueError, KeyError):
            messagebox.showerror(title='WRONG FILE', message='You must select a csv output from PE software, \nwith manual measure columns added.')
            print('you must select a csv output from PE software, \nwith manual measure columns added.')
            quit()

        self.initUI()

        ###################

    def initUI(self,):
        # set up GUI windows
        self.master.title('The NEW window')
        self.pack(fill=tk.BOTH, expand=1)

        # Data, parameters required
        try:
            # manual body measures desired for correlations [make this a check boxes option?]
            self.tape = self.df['tape']
            self.weight = self.df['weight']
            self.chest = self.df['chest']
            self.ht = self.df['ht']
            self.lenHW = self.df['len']

            # automated body measures
            self.calsidelength = self.df['calsidelength']
            self.calsidewither = self.df['calsidewither']
            self.girth = self.df['girth']
    ##        self.ADAPTMapKGS = self.df['ADAPTMapKGS']
    ##        self.ADAPTMapLBS = self.df['ADAPTMapLBS']

            self.dfred = self.df[['ht', 'len', 'chest', 'tape', 'sidewither', 'sidelength', 'girth' ]]

        except KeyError:
            messagebox.showerror(title='WRONG FILE', message='You must select a csv output from PE software, \nwith manual measure columns added.')
            print('you must select a csv output from PE software, \nwith manual measure columns added.')
            quit()

        print('self.dfred.head\n', self.dfred.head())
        print('\nself.df.head\n', self.df.head())

        self.correlation_df = self.dfred.corr(method='pearson')
        print(self.correlation_df)
        fig, ax = plt.subplots()
        label_format = '{:,.0f}'

        # Set up graph, user input for graph title, xticks, save, show
        self.master.deiconify()
        self.master.attributes('-topmost', True)
        self.master.focus_force()
    

        if 'AdaptMapReport-GC-with-manualMeasures.csv' in self.file_path:
            suggest = 'GC vs Manual Pearson Correlations'
            self.outcorr = os.path.sep.join([self.head, 'GC-digital-v-manual-correlations.csv'])
            self.outcorrpng = os.path.sep.join([self.head, 'GC-digital-v-manual-correlations.png'])

        elif 'AdaptMapReport-PE-with-manualMeasures.csv' in self.file_path:
            suggest = 'PE vs Manual Pearson Correlations'
            self.outcorr = os.path.sep.join([self.head, 'PE-digital-v-manual-correlations.csv'])
            self.outcorrpng = os.path.sep.join([self.head, 'PE-digital-v-manual-correlations.png'])

        else:
            suggest = 'Pearson Correlations'
            self.outcorr = os.path.sep.join([self.head, 'digital-v-manual-correlations.csv'])
            self.outcorrpng = os.path.sep.join([self.head, 'digital-v-manual-correlations.png'])

        print('\nout to: ', self.outcorr)
        
        title = simpledialog.askstring(title='Heatmap Graph Title', prompt='Enter the Heatmap Graph Title you would like.\n\n Suggest, "Pearson Correlations".', initialvalue=suggest, parent=self.master)
        self.master.focus_force()
        self.master.destroy()
    
        sns.heatmap(self.correlation_df, annot=True, fmt='.4f', cmap=plt.get_cmap('coolwarm'), cbar=False, ax=ax)
        plt.yticks(rotation=45)
        plt.xticks(rotation=45)
        plt.title(title)
        plt.savefig(self.outcorrpng, dpi=300)
        plt.show()

        # save correlation table to csv file
        self.correlation_df.to_csv(self.outcorr)
        
        return None



class Correlation_btw_two_PEoutput_csvs(tk.Frame):

    '''
    PreciseEdge csv Output data Statistical Analyses:
    COMPARES TWO PRECISE-EDGE CSV OUTPUT FILES WITH MANUAL DATA COLUMNS ADDED. CONVERTS TO TWO DFs.
    Correlate selected variables within a ONE df to the same variables within the A SECOND df.
    Data files in repo ARE 'AdaptMapReport-GC-with-manualMeasures.csv' AND 'AdaptMapReport-PE-with-manualMeasures.csv'.
    '''

    def __init__(self, ):

        super().__init__() #invokes the Frame class

        # user selects the GC and PE files (two csv files) to correlate GC vs PE
        file_path1 = os.path.abspath(filedialog.askopenfilename())
        print(file_path1)
        
        head1, tail1 = os.path.split(file_path1)
        head1 = os.path.sep.join([head1, 'plots-stats'])
        print('HEAD1', head1)
        self.outcorr1 = os.path.sep.join([head1, 'correlations1.csv'])
        print('outcorr1', self.outcorr1)
        self.outcorrpng1 = os.path.sep.join([head1, 'correlations1.png'])
        self.df1 = pd.read_csv(file_path1, header=0)

        try:
            self.df1red = self.df1[['ht', 'len', 'chest', 'tape', 'sidewither', 'sidelength', 'girth' ]]
        except KeyError:
            messagebox.showerror(title='WRONG FILE', message='You must select csv output from PE software, \nwith manual measure columns added.')
            print('you must select a csv output from PE software, \nwith manual measure columns added.')
            quit()            


        file_path2 = os.path.abspath(filedialog.askopenfilename())
        print(file_path2)

        head2, tail2 = os.path.split(file_path2)
        head2= os.path.sep.join([head2, 'plots-stats'])
        print("HEAD2", head2)
        self.outcorr2 = os.path.sep.join([head2, 'correlations2.csv'])
        #self.outcorr2 = os.path.sep.join(['plots-stats', self.outcorr2])
        self.outcorrpng2 = os.path.sep.join([head2, 'correlations2.png'])
        #self.outcorrpng2 = os.path.sep.join(['plots-stats', self.outcorrpng2])
        self.df2 = pd.read_csv(file_path2, header=0)

        try:
            self.df2red = self.df2[['ht', 'len', 'chest', 'tape', 'sidewither', 'sidelength', 'girth' ]]
        except KeyError:
            messagebox.showerror(title='WRONG FILE', message='You must select csv output from PE software, \nwith manual measure columns added.')
            print('you must select a csv output from PE software, \nwith manual measure columns added.')
            quit() 

        self.run_df1_df2_correlation()

    def run_df1_df2_correlation(self,):

        # set up GUI windows
        self.master.title('The NEW window')
        self.pack(fill=tk.BOTH, expand=1)
        
        self.df1vdf2corr = self.df2red.corrwith(other=self.df1red, axis=0, method="pearson", )
        print('self.df1vdf2corr\n', self.df1vdf2corr)

        # save correlation table to csv file
        headf, tailf = os.path.split(self.outcorr1)
        self.saveCorrGCvPE = os.path.sep.join([headf, 'GCvPE-correlations.txt' ])
        self.df1vdf2corr.to_csv(self.saveCorrGCvPE)
        print('saveCorrGCvPE\n', self.saveCorrGCvPE)

        self.master.destroy()
        
        return None



class Compare_tworuns_strokecount_cols_in_one_csv(tk.Frame):
    
    '''
    STROKE COUNT DATA Statistical Analyses:
    COMPARES TWO RUNS OF STROKE COUNTS ONE SROKE DATA SET PER COLUMN IN ONE CSV. CONVERTS TO TWO DFs.
    Correlate each variable within a ONE df to every variable within the A SECOND df.
    Data file in repo is 'strokes-GC-PE.csv'.
    '''

    def __init__(self, ):

        super().__init__() #invokes the Frame class

        # User select csv file, make df
        file_path = os.path.abspath(filedialog.askopenfilename())
        print(file_path)
        self.headstrokes, tail = os.path.split(file_path)
        self.headstrokes = os.path.sep.join([self.headstrokes, 'plots-stats'])
        self.out = os.path.sep.join([self.headstrokes, 'GCvsPEtests.txt'])
        #self.out = os.path.sep.join(['plots-stats', self.out])
        print('output to', self.out)

        self.df = pd.read_csv(file_path, header=0)

        ###################
        # Data, parameters required
        # get GC and PE strokes data from the csv file, set alpha
        try:
            self.gcdata = self.df['GCstrokes']
            self.pedata = self.df['PEstrokes']

        except KeyError:
            messagebox.showerror(title='WRONG FILE', message='You must select a csv output with columns of stroke count runs, \nand select two columns (runs) to compare.')
            print('You must select a csv output with columns of stroke count runs, \nand select two columns (runs) to compare.')
            quit()
            
        self.descriptive = self.df.describe()

        self.headers = list(self.df.columns)
        print('column headers:')
        for h in self.headers:
            print(h)

        self.initUI()

    def initUI(self,):
        # Set up graph, user input for graph title, xticks, save, show
        # set up GUI windows
        self.master.title('The NEW window')
        self.pack(fill=tk.BOTH, expand=1)
        self.master.deiconify()
        self.master.attributes('-topmost', True)
        self.master.focus_force()

##        self.master.focus_set()
##        self.data1_name = simpledialog.askstring(title='DATA-1 Key', prompt='Enter exact column name for dataset 1: ', parent=self.master)
        self.data1_name = self.headers[2]

##        self.master.focus_set()
##        self.data2_name = simpledialog.askstring(title='DATA-2 Key', prompt='Enter exact column name for dataset 2: ', parent=self.master)
        self.data2_name = self.headers[3]
        print('data1', self.data1_name)
        print('data1 name type', type(self.data1_name))



        self.data1 = self.df[self.data1_name]
        self.data2 = self.df[self.data2_name]
        print('shapes ==?', self.data1.shape == self.data2.shape)

        if 'GC' in self.data1_name:
            self.data1_pubname = 'GrabCut'
        if 'PE' in self.data1_name:
            self.data1_pubname = 'PreciseEdge'
            
        if 'GC' in self.data2_name:
            self.data1_pubname = 'GrabCut'
        if 'PE' in self.data2_name:
            self.data2_pubname = 'PreciseEdge'

        if 'GC' in self.data1_name and 'GC' in self.data2_name:
            self.data1_pubname = 'GrabCut1'
            self.data2_pubname = 'GrabCut2'

        if 'PE' in self.data1_name and 'PE' in self.data2_name:
            self.data1_pubname = 'PreciseEdge1'
            self.data2_pubname = 'PreciseEdge2'  
        
        try:      
            self.master.focus_set()
            
            self.alpha = float(simpledialog.askstring(title='Set Alpha Value', prompt='Enter an alpha value: ', parent=self.master))
            # print('alpha ', type(alpha), alpha)
            if self.alpha > 1.0:
                raise TypeError
            if self.alpha < 1.0:
                self.alpha = self.alpha
            
        except (ValueError, TypeError):
            self.alpha = 0.001
            messagebox.showwarning('ALPHA ERROR!', 'Alpha must be a float, less than 1, defaulting to 0.001')

        self.master.destroy()
        
        self.correlation_df1 = self.data1.corr(other=self.data2, method='pearson')
        print('correlation of GC strokes to PE strokes: ', self.correlation_df1)

        self.descriptivestr = self.descriptive.to_string(header=True, index=True)

        self.output_fn = str(self.out)

        with open(self.out, '+w') as self.out:
            self.out.write('Descriptive Statistics\n')
            self.out.write(self.descriptivestr)
            line = ' '.join(['\n\n alpha =', str(self.alpha), '\n', self.data1_name, 'N =', str(len(self.data1)),
                             '\n', self.data2_name, 'N =', str(len(self.data2)), '\n'])
            print(line)
            self.out.write(line)

            self.run()

        return None

    def run(self,):
        
        # Kolmogorov–Smirnov test for identical distributions
        self.out.write('\n=====================================================\n')
        line = ' '.join(['Kolmogorov–Smirnov test if', self.data1_name, 'and', self.data2_name,
                         'are from identical distributions\nRESULTS:\n'])
        print(line)
        self.out.write(line)
        ks2sampstat, ks2sampp = ks_2samp(self.data1, self.data2, alternative='two-sided')
        if ks2sampp < self.alpha:
            line = ' '.join([str(ks_2samp(self.data1, self.data2, alternative='two-sided')),
                            '\np <', str(self.alpha), ' ', self.data1_name, 'and', self.data2_name,
                             'have different distributions\n'])
            print(line)
            self.out.write(line)
        else:
            line = ' '.join([str(ks_2samp(self.data1, self.data2, alternative='two-sided')),
                            '\np >', str(self.alpha), ' ', self.data1_name, 'and', self.data2_name,
                             'have the same distribution\n'])
            print(line)
            self.out.write(line)

        self.out.write('\n=====================================================\n')
        import math
        # Kolmogorov–Smirnov test for normality for each dataset
        line = ' '.join(['Kolmogorov–Smirnov test for normality for each dataset\nRESULTS:\n'])
        print(line)
        self.out.write(line)
        gcksteststat, gckstestp = kstest(self.data1, 'norm')
        peksteststat, pekstestp =  kstest(self.data2, 'norm')
        print('GCstat', gcksteststat, gckstestp)
        print('PEstat', peksteststat, pekstestp)
        modes = ['exact', 'approx', 'asymp']
        
        if math.isclose(gcksteststat, 1.0, rel_tol=1e-02) and gckstestp == 0:
            for mode in modes: 
                line = ' '.join([self.data1_name, 'is normal distribution test is inconclusive, alpha is', str(self.alpha), '(p =', str(gckstestp), ')\nRunning in', mode, 'mode.'])
                self.out.write(line)
                print(line)
                gcksteststat, gckstestp = kstest(self.data1, 'norm', mode='async')
                print('GCstat2', gcksteststat, gckstestp)
                self.out.write(str(kstest(self.data1, 'norm', mode='async'))+'\n\n')


        if math.isclose(peksteststat, 1.0, rel_tol=1e-02)  and pekstestp == 0:
            for mode in modes: 
                line = ' '.join([self.data1_name, 'is normal distribution test is inconclusive, alpha is', str(self.alpha), '(p =', str(gckstestp), ')\nRunning in', mode, 'mode.'])
                self.out.write(line)
                print(line)
                peksteststat, pekstestp =  kstest(self.data2, 'norm', mode='async')
                print('PEstat2', peksteststat, pekstestp)
                self.out.write(str(kstest(self.data1, 'norm', mode='async'))+'\n\n')            

        if gckstestp < self.alpha:
            line = ' '.join([self.data1_name, 'is not normally distributed, p <', str(self.alpha), '(p =', str(gckstestp), ')\n'])
            print(line)
            self.out.write(line)
            gcnormal = False
        else:
            line = ' '.join([self.data1_name, 'is normally distributed, p >', str(self.alpha), '(p =', str(gckstestp), ')\n'])
            print(line)
            self.out.write(line)
            gcnormal = True

        if pekstestp < self.alpha:
            line = ' '.join([self.data2_name, 'is not normally distributed, p <', str(self.alpha), ' (p =', str(pekstestp), ')\n'])
            print(line)
            self.out.write(line)
            penormal = False
        else:
            line = ' '.join([self.data2_name, 'is normally distributed, p >', str(self.alpha), ' (p =', str(pekstestp), ')\n'])
            print(line)
            self.out.write(line)
            penormal = True

        if gcnormal is True and penormal is True:
            # Ttests: both distributions are normal, ttest can be used to test H0 that data1 = data2
            from scipy.stats import ttest_rel
            line = ' '.join([self.data1_name, 'and', self.data2_name, '\nare normally distributed, using parametric T-tests\n',
                             'RESULTS:'])
            print(line)
            self.out.write(line)
            #print('Performing t-tests...')
            # Dependant paired t-test (assumes normal distributions)
            '''
            This is a two-sided and one-sided tests for the null hypothesis that 2 related or
            repeated samples have identical average (expected) values.
            '''
            line1 = ' '.join(['\nT-test for \n',self.data1_name, 'and', self.data2_name, 'are the same\n',
                              str(ttest_rel(self.data1, self.data2, alternative='two-sided'))])
            line2 = ' '.join(['T-test if \n',self.data1_name, 'is less than', self.data2_name, '\n',
                              str(ttest_rel(self.data1, self.data2, alternative='less'))])
            line3 = ' '.join(['T-test if \n',self.data1_name, 'is greater than', self.data2_name, '\n',
                              str(ttest_rel(self.data1, self.data2, alternative='greater'))])
            
            #print(line1)
            #print(line2)
            #print(line3)

            self.out.write(line1)
            self.out.write(line2)
            self.out.write(line2)

            self.out.write('\n=====================================================\n')

        else:
            # Wilcoxon tests: both distributions are not normal, nonparametric test can be used to test H0 that data1 = data2
            from scipy.stats import wilcoxon
            self.out.write('\n=====================================================\n')
            line = ' '.join([self.data1_name, 'and', self.data2_name, 'are not normally distributed, using Wilcoxon',
                             'nonparametric tests\nRESULTS:'])
            print(line)
            self.out.write(line)
            #print('Performing Wilcoxon nonparametric tests for non-normal distributions...')
            '''
            The Wilcoxon signed-rank test tests the null hypothesis that two
            related paired samples come from the same distribution. In particular,
            it tests whether the distribution of the differences x - y is symmetric
            about zero. It is a non-parametric version of the paired T-test.
            '''
            line = ' '.join(['\nWilcoxon nonparametric test that', self.data1_name, 'is the same as', self.data2_name, '\n',
                  str(wilcoxon(self.data1, self.data2, alternative='two-sided')),'\n'])
            print(line)
            self.out.write(line)
            
            eqwlcxstat, eqwilcxp = wilcoxon(self.data1, self.data2, alternative='two-sided')
            
            if eqwilcxp < self.alpha:
                line = ' '.join(['p <', str(self.alpha), self.data1_name, 'is different from', self.data2_name, '\n'])
                print(line)
                self.out.write(line)
            else:
                line = ' '.join(['p >', str(self.alpha), self.data1_name, 'is the same as', self.data2_name, '\n'])
                print(line)
                self.out.write(line)

            line = ' '.join(['\nWilcoxon nonparametric test', self.data1_name, 'is less than', self.data2_name, '\n',
                  str(wilcoxon(self.data1, self.data2, alternative='less')),'\n'])
            print(line)
            self.out.write(line)
            
            ltwlcxstat, ltwilcxp = wilcoxon(self.data1, self.data2, alternative='less')
            
            if ltwilcxp < self.alpha:
                line = ' '.join(['p <', str(self.alpha), self.data1_name, 'is less than', self.data2_name, '\n'])
                print(line)
                self.out.write(line)
            else:
                line = ' '.join(['p >', str(self.alpha), self.data1_name, 'is not less than', self.data2_name, '\n'])
                print(line)
                self.out.write(line)

            line = ' '.join(['\nWilcoxon nonparametric test that', self.data1_name, 'is greater', self.data2_name, '\n',
                  str(wilcoxon(self.data1, self.data2, alternative='greater')),'\n'])
            print(line)
            self.out.write(line)
            
            gtwlcxstat, gtwilcxp = wilcoxon(self.data1, self.data2, alternative='greater')
            
            if gtwilcxp < self.alpha:
                line = ' '.join(['p <', str(self.alpha), ' ', self.data1_name, 'is greater than', self.data2_name, '\n'])
                print(line)
                self.out.write(line)
            else:
                line = ' '.join(['p >', str(self.alpha), ' ', self.data1_name, 'is not greater than', self.data2_name, '\n'])
                print(line)
                self.out.write(line)

        self.out.write('\n=====================================================\n')

        self.out.close()
        print('\noutput file is here:\n', self.output_fn)
##        self.master.destroy()

        GOF_distribution(self.data1, self.data2, self.data1_name, self.data2_name, self.data1_pubname, self.data2_pubname, self.headstrokes,)

        return self.data1, self.data2, self.data1_name, self.data2_name, self.data1_pubname, self.data2_pubname
            

class GOF_distribution(Compare_tworuns_strokecount_cols_in_one_csv):

    def __init__(self, data1, data2, data1_name, data2_name, data1_pubname, data2_pubname, outdir, ):

        self.data1 = data1
        self.data2 = data2
        self.data1_name = data1_name
        self.data2_name = data2_name
        self.data1_pubname = data1_pubname
        self.data2_pubname = data2_pubname
        self.headstrokes = outdir

        # data1
        fig = sm.qqplot(self.data1, line='45')
        fname = '-'.join([self.data1_name,'QQ.png'])
        fname = os.path.sep.join([self.headstrokes, fname])
        plt.title(self.data1_name)
        plt.savefig(fname)
        plt.show()

        # data2
        fig = sm.qqplot(self.data2, line='45')
        fname = '-'.join([self.data2_name,'QQ.png'])
        fname = os.path.sep.join([self.headstrokes, fname])
        plt.title(self.data2_name)
        plt.savefig(fname)
        plt.show()

        # histograms
        # data1
        fig = sns.histplot(data=self.data1, x=self.data1, binrange=(0,1400), binwidth=50)
        plt.ylim(0, 50)
        plt.ylabel("Number of Images")
        plt.title(self.data1_name)
        fname = '-'.join([self.data1_name,'Histogram.png'])
        fname = os.path.sep.join([self.headstrokes, fname])
        plt.savefig(fname)
        plt.show()

        # data2
        fig = sns.histplot(data=self.data2, x=self.data2, binrange=(0,1400), binwidth=50)
        plt.ylim(0, 50)
        plt.ylabel("Number of Images")
        plt.title(self.data2_name)
        fname = '-'.join([self.data2_name,'Histogram.png'])
        fname = os.path.sep.join([self.headstrokes, fname])
        plt.savefig(fname)
        plt.show()

        # potential distributions
        dists = ['kde', 'ecdf', ]
        
        # distribution graphical probability plots
        for dist_type in dists:
            
##            print('\nDISTRIBUTION PROBABILITY PLOTS\n')
##            print('distribution', dist_type)
            sns.set_style('white')
            sns.set_context('paper', font_scale = 2)

            # data1
            fig = sns.displot(data=self.data1, x=self.data1, kind=dist_type, aspect=1.5)
            fname = '-'.join([dist_type, self.data1_name, '.png'])
            fname = os.path.sep.join([self.headstrokes, fname])
            plt.title(dist_type)
            plt.xlabel(self.data1_pubname)
            plt.xlim(0, 1400)
            plt.savefig(fname=fname, dpi=300, )
            plt.show()

            # data2
            sns.set_style('white')
            sns.set_context('paper', font_scale = 2)
            fig = sns.displot(data=self.data2, x= self.data2, kind=dist_type, aspect=1.5)
            plt.title(dist_type)
            plt.xlabel(self.data2_pubname)
            plt.xlim(0, 1400)
            fname = '-'.join([dist_type, self.data2_name, '.png'])
            fname = os.path.sep.join([self.headstrokes, fname])
            plt.savefig(fname=fname, dpi=300, )
            plt.show()

        for dist_type in ['hist', 'kde']:
##            print('\nBIVARIATE PLOTS\n')
##            print('distribution', dist_type)
##            print('\n', data1_name, ' vs. ', data2_name)

            name = '-'.join([self.data1_pubname, 'vs', self.data2_pubname])
            sns.set_style('white')
            sns.set_context('paper', font_scale = 2)
            sns.displot(data=self.data1, x=self.data1, y=self.data2, kind=dist_type, rug=True, aspect=1.5)
            plt.title(name)
            plt.xlabel(self.data1_pubname)
            plt.ylabel(self.data2_pubname)
            plt.xlim(0, 1400)
            plt.ylim(0, 1400)

            fname = '-'.join([dist_type, name, '.png'])
            fname = os.path.sep.join([self.headstrokes, fname])
            plt.savefig(fname=fname, dpi=300, )
            plt.show()

        return None

        quit()


if __name__ == '__main__':
    if not os.path.exists('plots-stats',):
        os.makedirs(r'plots-stats',)
        
    print('running main')
    main()
   
