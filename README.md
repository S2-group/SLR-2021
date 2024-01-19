# Software Engineering Research on the Robot Operating System: A Systematic Literature Review

This repository contains the replication package of the systematic literature review on software engineering research on the Robot Operating System (ROS). 
The contents of this repository can be used to:

- Replicate the steps to obtain the potentially relevant studies.
- Replicate the steps to filter the potentially relevent studies to the selected studies.
- Produce the plots presented in the paper.
- Further searches on DBLP snapshots.

This study has been designed, performed, and reported by the following researchers:

- Michel Albonico (Federal University of Technology, Paraná - Brazil)
- Milica Dordevic (Vrije Universiteit Amsterdam - The Netherlands)
- Engel Hamer (Vrije Universiteit Amsterdam - The Netherlands)
- Ivano Malavolta (Vrije Universiteit Amsterdam - The Netherlands)

For any information, interested researchers can contact us by sending an email to any of the investigators listed above.

## How to cite the dataset
If the dataset or the results of our study are helping your research, consider citing our study as follows, thanks!

```
@article{JSS_ROS_2022,
title = {Software engineering research on the Robot Operating System: A systematic mapping study},
journal = {Journal of Systems and Software},
pages = {111574},
year = {2022},
issn = {0164-1212},
doi = {https://doi.org/10.1016/j.jss.2022.111574},
url = {https://www.sciencedirect.com/science/article/pii/S0164121222002503},
author = {Michel Albonico and Milica Đorđević and Engel Hamer and Ivano Malavolta},
}
```

### Overview of the replication package
---

This replication package is structured as follows:

```
./scripts                The scripts used for automating the search process.
./data_analysis          The Jupyter notebooks are used for producing all figures in the paper.
./data                   All the spreadsheets with the data points and the manual selection.
```


### Studies Classification

The complete list of studies classification is available [here](https://github.com/S2-group/SLR_SE_ROS_2022/blob/main/data_analysis/studies_classification.pdf).


### Crawling Papers

If you are interested in replicating our papers' crawling, here are a few details that can help you.

You must be in the `scripts` folder:

```bash
$ cd scripts/
```

Then, you must download the last [DBLP snapshot](https://dblp.org/xml/release/) and extract it in the `scripts` folder (it's a big file > 4GB), and download the compatible document type definition (DTD) file - usually the first one after the downloaded XML file.

Now, it is time to set everything (snapshot file, year range, etc.) at the beginning of the `dblp_search.py` file. We plan to use a properties file for this shortly.

Once everything is set, you run the `dblp_search.py` script, and the papers should be selected (it will be a bit long given the file size).

```bash
$ python3 dblp_search.py > papers.csv
```

Finally, you can download all the PDFs for posterior paper analysis:

```bash
$ python3 retrive_pdfs.py papers.csv
```
