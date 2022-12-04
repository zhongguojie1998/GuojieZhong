---
layout: page
title: RESCVE
description: A deep learning model to represent the modes of action of missense variants. 
img: assets/img/RESCVE.jpg
importance: 2
category: work
---

This is my second PhD project in <a href="http://www.columbia.edu/~ys2411/">Dr. Yufeng Shen's lab</a>. 

Accurate prediction of functional impact for missense variants is fundamental for genetic analysis and clinical applications. Current methods focused on generating an overall pathogenicity prediction score while overlooking the fact that variant effect should be multi-dimensional via different modes of action, such as gain or loss of function, and loss of folding stability or enzymatic activity. Recent breakthrough of high-capacity language models enabled ab initio prediction of protein structures as well as self-supervised representation learning of protein sequence and functions. Here we present RESCVE, a method to learn universal representation of sequence variation from protein context. We demonstrated the utility of the method predicting a range of modes of action for missense variants through transfer learning.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/RESCVE.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Demonstration of the model. Arrows and nodes show information flow, colors show parameter updates during training and transfer learning.
</div>

For details, please check our <a href="https://www.mlsb.io/papers_2022/Representation_of_missense_variants_for_predicting_modes_of_action.pdf">manuscript</a> and <a href="https://github.com/ShenLab/rescve">GitHub repository</a>.
