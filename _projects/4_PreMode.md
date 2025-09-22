---
layout: page
title: PreMode
description: Predicting mode-of-action of missense variants by deep graph representation learning of protein sequence and structural context
img: assets/img/PreMode.png
importance: 2
category: Research
---

This is my second and main PhD project in <a href="http://www.columbia.edu/~ys2411/">Dr. Yufeng Shen's lab</a>. It is the upgraded version of RESCVE.

Accurate prediction of the functional impact of missense variants is important for disease gene discovery, clinical genetic diagnostics, therapeutic strategies, and protein engineering. Previous efforts have focused on predicting a binary pathogenicity classification, but the functional impact of missense variants is multi-dimensional. Pathogenic missense variants in the same gene may act through different modes of action (i.e., gain/loss-of-function) by affecting different aspects of protein function. They may result in distinct clinical conditions that require different treatments. We developed a new method, PreMode, to perform gene-specific mode-of-action predictions. PreMode models effects of coding sequence variants using SE(3)-equivariant graph neural networks on protein sequences and structures. Using the largest-to-date set of missense variants with known modes of action, we showed that PreMode reached state-of-the-art performance in multiple types of mode-of-action predictions by efficient transfer-learning. Additionally, PreMode's prediction of G/LoF variants in a kinase is validated with inactive-active conformation transition energy changes. Finally, we show that PreMode enables efficient study design of deep mutational scans and optimization in protein engineering.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/PreMode.png" title="example image" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Mode-of-action definition and PreMode framework. A) Mode-of-action definition at molecular level and genetic levels. Variant effects could be quantified by two parameters: "distance from wildtype", r, and "direction of change", θ, all current methods focus on predicting the r, that reflects pathogenicity, but cannot predict θ, which is mode-of-action. Mode-of-action is protein/gene specific that depend on its original functions. B) PreMode framework. Blue arrows show the data flow and at pretrain stage for pathogenicity prediction, green arrows show transfer-learning stage for mode-of-action prediction.
</div>

For details, please check our <a href="https://www.nature.com/articles/s41467-025-62318-4">manuscript</a> and <a href="https://github.com/ShenLab/PreMode">GitHub repository</a>.
