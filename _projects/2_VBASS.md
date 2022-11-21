---
layout: page
title: VBASS
description: A Bayesian Mixture model with learnable prior to integrate single cell gene expression data in rare variants association analysis. 
img: assets/img/VBASS.jpg
importance: 2
category: work
---

This is my first PhD project in <a href="http://www.columbia.edu/~ys2411/">Dr. Yufeng Shen's lab</a>. 

Rare or de novo variants have substantial contribution to human diseases, but the statistical power to identify risk genes by rare variants is generally low due to rarity of genotype data. Previous studies have shown that risk genes usually have high expression in relevant cell types, although for many conditions the identity of these cell types are largely unknown. Recent efforts in single cell atlas in human and model organisms produced large amount of gene expression data. Here we present VBASS, a Bayesian method that integrates single-cell expression and de novo variant (DNV) data to improve power of disease risk gene discovery. VBASS models disease risk prior as a function of expression profiles, approximated by deep neural networks. It learns the weights of neural networks and parameters of Gamma-Poisson likelihood models of DNV counts jointly from expression and genetics data. On simulated data, VBASS shows proper error rate control and better power than state-of-the-art methods. We applied VBASS to published datasets and identified more candidate risk genes with supports from literature or data from independent cohorts. 

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/VBASS.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/VBASS_2.jpg" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Demonstration of the model. Left is the graphic model. Right is a example demonstration of information flow.
</div>

