---
layout: page
title: EpiBRAIN
description: A sequence-to-function deep learning model predicting cell-type-specific chromatin states, gene expression, and variant effects in the human brain.
img: assets/img/EpiBRAIN.png
importance: 2
category: Research
---

This is my first postdoc project in <a href="https://www.nygenome.org/lab/bing-ren/">Dr. Bing Ren's lab</a> at the New York Genome Center, developed as part of the BICAN human basal ganglia single-cell multiome atlas.

Deep-learning sequence-to-function models such as Borzoi and AlphaGenome predict epigenomic states and gene expression from DNA sequence, but they are trained mostly on bulk tissue data and lack cell-type resolution. Using our Droplet Paired-Tag atlas (joint transcriptome and H3K27ac, H3K27me3 or H3K9me3 profiles) together with single-nucleus chromatin accessibility data, we developed EpiBRAIN (Epigenomics-based Brain Regulation Attention Inference Network). Starting from a 524 kb hg38 sequence, EpiBRAIN predicts cell-type-specific ATAC-seq, H3K27ac, H3K27me3, H3K9me3, and strand-specific RNA-seq tracks at 32 bp resolution for 37 brain cell types from the basal ganglia, cerebral cortex, cerebellum, and pons. Instead of one output track per cell type and modality, EpiBRAIN projects shared sequence embeddings into a compact cell-type-specific chromatin embedding, which shared chromatin profile heads then decode into each modality. This lets the model learn relationships between tracks within each cell type, and it outperforms the default Borzoi head on these data.

EpiBRAIN reaches average Pearson correlations above 0.80 for chromatin accessibility and gene expression and around 0.70 for histone modifications on held-out regions. Removing the histone modification data lowers gene expression accuracy in every cell type. For a Parkinson's disease risk variant, rs6581593, EpiBRAIN predicts that the risk allele disrupts a ZEB2 repressor motif in a microglia-specific enhancer, which leads to microglial upregulation of LRRK2. This agrees with published CRISPRi and iPSC-derived microglia experiments. EpiBRAIN also outperforms Borzoi and AlphaGenome at separating fine-mapped causal from non-causal basal ganglia eQTLs, especially distal ones. In schizophrenia, the top 5% of variants ranked by predicted H3K27ac effects in medium spiny neurons explain about 25% of disease heritability.

<div class="row justify-content-sm-center">
    <div class="col-sm-8 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/EpiBRAIN.png" title="EpiBRAIN model" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    EpiBRAIN architecture. A 524 kb reference DNA sequence passes through convolutional blocks (7x) and transformer blocks (8x) at 128 bp resolution, then convolutional up-sampling (2x) to 32 bp resolution. Cell type embedding heads project the shared sequence embeddings into cell-type-specific chromatin embeddings, and shared chromatin profile heads decode them into ATAC, H3K27ac, H3K27me3, H3K9me3, and RNA coverage tracks for each cell type. Blue shows data and outputs; green shows learned parameters.
</div>

For details, please check our <a href="https://doi.org/10.64898/2026.02.03.703645">manuscript</a> and <a href="https://github.com/zhongguojie1998/EpiBRAIN">GitHub repository</a>.
