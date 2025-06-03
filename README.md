# Case Study: Anomaly Detection in Smart Grids with TREs
This repository contains the datasets and scripts for reproducing the experiments that are published in the conference paper.
Particularly, this folder contains:
- The daily electricity consumption records of user ID 1153 (day\_\<first_day\>\_\<last_day\>\_user\_\<id\>.zip).
- The timed regular expressions in TXT files (TRE subfolder).
- The bash-shell and Python scripts for running the evaluation of the TREs against the electricity consumption recordings.

## Installation of dependencies
We recommend you to install [pyenv](https://github.com/pyenv/pyenv) for managing virtual environments in Python.
Previously, you must install the [pyenv dependencies] (https://github.com/pyenv/pyenv/wiki#suggested-build-environment).

Then, just run the following command for installing the Python libraries that are required for the experimental case study.

``
pip install -r requirements.txt --user
``

[ParetoLib](https://gricad-gitlab.univ-grenoble-alpes.fr/verimag/tempo/multidimensional_search), version 2.5.1, must be installed
manually following the installation procedure in the Git website.
Shortly speaking, you must download the *.whl file from the [release assets](https://gricad-gitlab.univ-grenoble-alpes.fr/verimag/tempo/multidimensional_search/-/jobs/artifacts/v2.5.1/download?job=build), and run:

``
pip install *.whl
``

Additionally, you must install [QueryTRE 0.1.0](https://github.com/nachorequeno/querytre/releases/tag/v0.1.0) following the same procedure.

## Digesting several time series into a single probabilistic signal with 95% interval of confidence
In order to summarize the electricity consumption recordings of several days, you can run the following command:

``
python ./signals2prsignal.py ./output_prsignal ./input_signal_1.csv ... ./input_signal_n.csv
``

As output, it will generate a CSV file (named output_prsignal.csv) and a SVG picture (named output_prsignal.svg).
For instance, the next figure shows the average electricity consumption of user ID 1153 in a regular day.
The upper/lower bands are the 95% interval of confidence which includes the 95% of the samples.

![Alt Text](/svg/normal.svg)

You can generate the pictures of conference paper running the `plot_pictures.sh` script. 
The CSV file contains the time serie information the picture was generated from.
Particularly, it has three columns: 1) the timestamp, 2) the average electricity consumption, and 3) the standard deviation.
As the smart meters register the information every half an hour, the CSV file should consist of 48 entries.

## How to run the experiments
In order to run the experiments, you must firstly install [ParetoLib](https://gricad-gitlab.univ-grenoble-alpes.fr/verimag/tempo/multidimensional_search), version 2.5.1.
Then, you can run the analysis for one of the anomaly scenarios in [fdi50, fdi150, avg, max\_avg, min\_avg, normal, rsa01\_08, rsa2\_5, swap].

``
python experiments.py <attack> ./day_0_360_user_1143/<attack>/days_*
``

For instance, the following command will run the FDI scenario where the data is scaled by 50%.

``
python experiments.py fdi50 ./day_0_360_user_1143/fdi50/days_*
``

As output, the Python script will show the temporal zones that return the execution of the TRE expression agains the electricity consumption record.

![img1](/svg/const50_zones.svg)

Additionally, the Python script will overlay the information of the temporal zones on top of the electricity consumption record.
Green lines represent the time instants when the TRE starts to become true, and the red lines corresponds to the time instants when the TRE ends. 

![img2](/svg/const50_signal_and_zones.svg)

Green lines indicate the time instants when the pattern matching of the TRE may begin (b < t < b'); 
the red lines are the time instants when the pattern recognition may end (e < t < e'), and blue lines represent the duration (b + d < e, b' + d' < e').

In [Figure 1](#img1), dashed (solid) lines indicate whether the time constraints are strict (b < t) or not (b <= t).
In [Figure 2](#img2), solid (dashed) lines indicate the loosest (tighest) time instants when the TRE should start (b, b') or end (e, e').

For the sake of simplicity, blue lines are not printed in the [second picture](#img2). 
The time windows where the TRE is satisfied are colored in grey. 
The intensity of the grey color indicates overlapping time windows.
[Figure 1](#img1) can be understood as [Figure 2](#img2) seen from bird's-eye perspective. 

**Remark:**
RSA scenarios require `lower` and `higher` propositions in TRE. Therefore, you should run `experiments_for_rsa.py` instead of `experiments.py`.  
