
CLOUDSENTINEL AI
MULTICLASS MODEL EVALUATION REPORT
==================================

Model: Random Forest
Dataset: CIC-IDS2017
Evaluation: Stratified random test split

Test samples: 22452
Features: 78
Classes: 15

Accuracy: 0.9915
Accuracy percentage: 99.15%

CLASSIFICATION REPORT
=====================
                            precision    recall  f1-score   support

                    BENIGN       1.00      1.00      1.00      4000
                       Bot       0.99      1.00      1.00       390
                      DDoS       1.00      1.00      1.00      4000
             DoS GoldenEye       1.00      1.00      1.00      2057
                  DoS Hulk       1.00      1.00      1.00      4000
          DoS Slowhttptest       1.00      0.99      0.99      1046
             DoS slowloris       1.00      0.99      0.99      1077
               FTP-Patator       1.00      1.00      1.00      1186
                Heartbleed       1.00      0.50      0.67         2
              Infiltration       1.00      1.00      1.00         7
                  PortScan       1.00      1.00      1.00      3615
               SSH-Patator       1.00      1.00      1.00       644
  Web Attack � Brute Force       0.72      0.73      0.73       294
Web Attack � Sql Injection       1.00      0.75      0.86         4
          Web Attack � XSS       0.38      0.37      0.37       130

                  accuracy                           0.99     22452
                 macro avg       0.94      0.89      0.91     22452
              weighted avg       0.99      0.99      0.99     22452


CONFUSION MATRIX
================
Class order:
['BENIGN', 'Bot', 'DDoS', 'DoS GoldenEye', 'DoS Hulk', 'DoS Slowhttptest', 'DoS slowloris', 'FTP-Patator', 'Heartbleed', 'Infiltration', 'PortScan', 'SSH-Patator', 'Web Attack � Brute Force', 'Web Attack � Sql Injection', 'Web Attack � XSS']

[[3992    2    1    0    0    0    0    1    0    0    0    2    0    0
     2]
 [   0  390    0    0    0    0    0    0    0    0    0    0    0    0
     0]
 [   6    0 3994    0    0    0    0    0    0    0    0    0    0    0
     0]
 [   0    0    0 2057    0    0    0    0    0    0    0    0    0    0
     0]
 [   1    0    0    0 3999    0    0    0    0    0    0    0    0    0
     0]
 [   2    0    0    0    0 1040    4    0    0    0    0    0    0    0
     0]
 [   2    0    0    1    0    5 1069    0    0    0    0    0    0    0
     0]
 [   0    0    0    0    0    0    0 1186    0    0    0    0    0    0
     0]
 [   1    0    0    0    0    0    0    0    1    0    0    0    0    0
     0]
 [   0    0    0    0    0    0    0    0    0    7    0    0    0    0
     0]
 [   0    0    0    0    0    0    0    0    0    0 3615    0    0    0
     0]
 [   0    0    0    0    0    0    0    0    0    0    0  644    0    0
     0]
 [   1    0    0    0    0    0    0    0    0    0    0    0  216    0
    77]
 [   0    0    0    0    0    0    0    0    0    0    0    0    1    3
     0]
 [   1    0    0    0    0    0    0    0    0    0    0    0   81    0
    48]]

LIMITATIONS
===========
1. This is a random-split evaluation, not a cross-day test.
2. Rare attack classes have very few test samples.
3. Results may not represent performance on unseen network traffic.
4. The separate binary cross-day evaluation achieved 73.36%
   accuracy and should be reported independently.
