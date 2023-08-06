.. vim: set fileencoding=utf-8 :
.. Thu Feb 22 11:30:16 CET 2018

.. image:: https://img.shields.io/badge/docs-v1.0.1-yellow.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.hobpad2.chapter19/v1.0.1/index.html
.. image:: https://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/bob/bob.hobpad2.chapter19/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.hobpad2.chapter19/badges/v1.0.1/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.hobpad2.chapter19/commits/v1.0.1
.. image:: https://gitlab.idiap.ch/bob/bob.hobpad2.chapter19/badges/v1.0.1/coverage.svg
   :target: https://gitlab.idiap.ch/bob/bob.hobpad2.chapter19/commits/v1.0.1
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.hobpad2.chapter19
.. image:: https://img.shields.io/pypi/v/bob.hobpad2.chapter19.svg
   :target: https://pypi.python.org/pypi/bob.hobpad2.chapter19


===============================================================
 A Cross-database Study of Voice Presentation Attack Detection
===============================================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It is a software package to reproduce "A Cross-database Study of Voice Presentation Attack Detection" Chapter 19 of "Handbook of Biometric
Anti-Spoofing: Presentation Attack Detection 2nd Edition"


We use conda_ to manage the software stack installation. To install this
package and all dependencies, first install conda_, and then run the
following command on your shell::

  $ conda create --name hobpad2-chapter19 --override-channels -c https://www.idiap.ch/software/bob/conda -c defaults python=3 bob.hobpad2.chapter19
  $ conda activate hobpad2-chapter19
  (hobpad2-chapter19) $ #type all commands inside this "activated" environment


.. note::

   At the present time, Bob_ only offers support to Linux and MacOS operating
   systems. Windows installations are **not** supported.


Score files to reproduce the results of the chapter
===================================================

Due to the large number and size of score files, some of them need to be downloaded and the rest were archived and need to be unzipped. Please follow these steps to prepare the scores, so that error rates and figures used in the chapter can be computed:

* Unzip `pad_handcrafted.zip` and `pad_megafusion.zip` files locate in the `scores' folder into respective `pad_handcrafted` and `pad_megafusion` subfolders.

* Download and unarchive some of the scores of handcrafted features-based PAD systems:

    $ cd scores
    $ wget http://www.idiap.ch/resource/biometric/data/interspeech_2016.tar.gz
    $ tar -xzvf interspeech_2016.tar.gz  
    $ Add these score files inside `pad_handcrafted` folder

* Download and unarchive scores for CNN-based PAD systems:

    $ cd scores
    $ wget http://www.idiap.ch/resource/biometric/data/isba2018-pad-dnn.tar.gz
    $ tar -xzvf isba2018-pad-dnn.tar.gz  
    $ Rename the obtained scores folder into `pad_cnn` folder


Reproducing the results of the chapter
======================================

To compute error rates presented in Tables 5 and 6 of the chapter on performance of PAD systems based on handcrafted features, the following script should be used:


    $ ./compute_handcrafted_results.sh

The script will create a folder for each configuration of PAD system and datasets. The folders contain DET curves for each given configuration, histograms of score distributions, and error rates. The script also creates a text file 'latex_table_handcrafed_stats_eer.txt' which contains a LaTeX formatted table with the results from Table 6 and 6.

To compute error rates presented in Table 7, run the script that is installed with bob.measure using the following:


    $ bob_eval_threshold.py -c eer ../scores/pad_megafusion/corresponding_folder/scores-dev

To compute error rates presented in Tables 10 and 11 and Figure 6 of the chapter on performance of CNN-based PAD systems, the following script should be used:


    $ ./compute_cnn_results.sh

The script will create a folder for each configuration of PAD system and datasets. The folders contain DET curves for each given configuration (subset of these plots are shown in Figure 6 of the chapter), histograms of score distributions, and error rates. The script also creates a text file 'latex_table_cnn_stats_eer.txt' which contains a LaTeX formatted table with the results from Table 10 and 11.

To compute error rates for different types of attack as presented in Table 12, please execute the following script:


    $ ./compute_results_cnn_per_attack.sh

The script will compute error rates for each type of attack of voicePA and BioCPqD-PA databases used in the paper and produce 'latex_table_cnn_per_attack_stats_eer.txt' file with LaTeX formatted table that has results from Table 12.


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _conda: https://conda.io/
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
