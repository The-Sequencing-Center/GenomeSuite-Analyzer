# GenomeSuite Analyzer
GenomeSuite Analyzer is a fast human genome structural variant (SV) caller for Nanopore long-read sequencing datasets. It accurately detects SVs in germline and somatic sequencing data.

<br>

## Table of Contents
[Features](#features)  
[Usage](#usage)  
[AWS](#aws)  
[Documentation](#documentation)  
[Citation](#citation)  
[License](#license)  
[Contact](#contact)  

<br>

## Features
|                                 |                                                                                                   |
| :------------------------------ | ------------------------------------------------------------------------------------------------- |    
| High Sensitivity                | Accurately detects complex SVs, including repeat-rich regions                                     |  
| Long-read analysis              | Works with Oxford Nanopore sequencer long-read datasets                                           |
| Precision                       | Capable of read-based phasing and accurate breakpoint detection                                   |                                   
| Automatic Filtering             | Filters out false positive events automatically                                                   |
| Low-Coverage Data Compatibility | Operates effectively on low-coverage datasets, making it cost-efficient                           |
| Discovery of Novel Variants     | Has uncovered thousands of novel variants in various genomic datasets                             |

<br>

GenomeSuite Analyzer detects a wide variety of human SVs:

- Deletions
- Duplications
- Insertions
- Inversions
- Translocations
- Copy Number Variants (CNVs)
- Tandem Duplications
- Segmental Duplications
- Complex Rearrangements
- Chromothripsis
- Chromoplexy
- Balanced Translocations
- Unbalanced Translocations
- Ring Chromosomes
- Dicentric Chromosomes
- Large Insertions (Transposable Elements)
- Subtelomeric Rearrangements
- Telomere Shortening
- Telomere Elongation
- Polymorphic Inversions
- Microsatellite Expansions
- Variable Number Tandem Repeats (VNTRs)
- Heterochromatic Variations
- Chromosomal Fusions
- Chromosomal Fissions
- Large-scale Structural Polymorphisms
- Intra-chromosomal Translocations
- Inter-chromosomal Translocations
- Structural Variants involving Repetitive Elements
- Chromosomal Duplication/Amplifications
- Gene Fusions
- Large Segmental Duplications
- Mobile Element Insertions
- Non-allelic Homologous Recombination (NAHR) Variants
- Chromosomal Aneuploidy
- Isochromosomes
- Gene Conversion Events

<br>

## Usage
GenomeSuite Analyzer is hosted on The SeqCenter Cloud on AWS (Amazon Web Services).  The GenomeSuite Analyzer Users Guide (see [Documentation](#documentation)) explains how to access and use the application.  
- If you already have an AWS account, you can start using GenomeSuite Analyzer by following instructions in the Users Guide.  
- If you do not have an AWS account, the Users Guide explains how to create one, and then start using the application.  

<br>

## AWS  
GenomeSuite Analyzer is hosted on The SeqCenter Cloud on AWS (Amazon Web Services) EC2 instances that support Nvidia GPU's.  The Nvidia GPU's are required for GenomeSuite Analyzer.  There are several instance types that run GenomeSuite Analyzer.  The instances are listed in order of increasing performance.  The "p3" instances are most appropriate for human <b>whole exome</b>.  The "p4" and "p5" instances are most appropriate for human <b>whole genome</b>. In all cases the architecture is x86_64.  

| Instance type | # vCPU's | Clock speed (GHz) | CPU Memory (GiB)  | Storage (GB) | Storage type | Network Performance (Gbit/sec.) | GPU name | # GPU's | GPU memory (GiB) | Price (USD/hr.) |  
| :-----------: | -------: | ----------------: | ----------------: | -----------: | -----------: | ------------------------------: | -------: | ------: | ---------------: | --------------: |   
|   p3.2xlarge  |     8    |      2.7          |           61      |    ---       | ---          | Up to 10                        | V100     | 1       | 16               |  3.06           |  
|   p3.8xlarge  |    32    |      2.7          |          244      |    ---       | ---          | 10                              | V100     | 4       | 16               | 12.24           |  
|   p3.16xlarge |    64    |      2.7          |          488      |    ---       | ---          | 25                              | V100     | 8       | 16               | 24.48           |
| p3dn.24xlarge |    96    |      2.5          |          768      |  1,800       | SSD          | 100                             | V100     | 8       | 32               | 31.21           |
|  p4d.24xlarge |    96    |      3.0          |        1,152      |  8,000       | SSD          | 4x 100                          | A100     | 8       | 40               | 32.77           |  
|   p5.48xlarge |   192    |      3.6          |        2,048      | 30,400       | SSD          | 3,200                           | H100     | 8       | 80               | 98.32           |  

<br>

## Documentation
The [GenomeSuite Analyzer Users Guide](https://github.com/TheSequencingCenter/GenomeSuite Analyzer/wiki) describes how to access and run the application.  

<br>

## Citation
If you use Snffles in publications or reports, please cite these papers:  
[Sniffles v2](https://www.nature.com/articles/s41587-023-02024-y)  
[Sniffles Analyzer v1](https://www.nature.com/articles/s41592-018-0001-7) 

<br>

## License
This application is licensed under the [MIT LICENSE](LICENSE).

<br>

## Contact
Richard Casey, PhD  
The Sequencing Center  
Fort Collins, CO  80524  
USA  
877-425-2235  
970-980-5975  
info@thesequencingcenter.com  
support@thesequencingcenter.com  
richard@thesequencingcenter.com  
www.thesequencingcenter.com  
https://www.linkedin.com/in/richardcaseyhpc/
