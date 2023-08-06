# Copter

A library for codon optimization

### Installation

```
pip install copter
```

### Quick Start

```
def eval_codons_gc_ratio(codons):
  gene = ''.join(codons)
  gc_ratio = (gene.count('G') + gene.count('C')) / float(len(gene))
  return gc_ratio,
protein = 'NAMALGLMET'
validation_func = lambda gene: calc_gc_ratio(gene) < 0.65
optimized_genes = optimize(aa_seq,
                           self.eval_codons_gc_ratio,
                           (1.0,),
                           indpb=0.05,
                           population_size=20,
                           generation_size=100,
                           surviver_amount=10,
                           validation_func=validation_func)
```
