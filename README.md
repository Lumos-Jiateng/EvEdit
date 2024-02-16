# EvEdit
This is the official code repository for our paper: EvEdit: Event-based Knowledge Editing with Deductive Editing Boundaries

#### We Identify a Fallacy with Current Knowledge Editing Appraoches.
![Current KE approaches, which typically operate on (subject, relation, object) triples, ignore the contextual information and the relation among different knowledge. Such editing methods could thus encounter an uncertain editing boundary, leaving a lot of relevant knowledge in ambiguity: Queries that could be answered pre-edit cannot be reliably answered afterward.](https://github.com/Lumos-Jiateng/EvEdit/blob/main/Images/fallacy.drawio.pdf)Current KE approaches, which typically operate on (subject, relation, object) triples, ignore the contextual information and the relation among different knowledge. Such editing methods could thus encounter an uncertain editing boundary, leaving a lot of relevant knowledge in ambiguity: Queries that could be answered pre-edit cannot be reliably answered afterward.

### Catalog 
#### Version-1.0 Update:
  1. We release the benchmark EvEdit
  2. We release the Scripts to generate custom event-based-editing datasets.

### EvEdit Benchmark
The EvEdit dataset is derived from the [CounterFactual](https://rome.baulab.info/) dataset. We use GPT-3.5-turbo to filter out edits that is not supported by any event in the future, and then further augment the remaining edits into events. 

### Acknowledgement 

The implementation our code repository relies on resources from EasyLM and EasyEdit. We thank the original authors for their open-sourcing.




