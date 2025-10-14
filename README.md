# agentG

Thoughts:
Certainly can add gpt module which takes text as input and runs all given scripts on defaults, but...
- Can we have it make informed decisions on setting input parameters, and to what extent?
  - Do we have a different gpt module(s) which knows literature well which it discusses with?
  - Do we train it on the parameters and their outcomes? How much is needed? For instance, ChatGPT on its own already understands well enough to make suggestions, but can we tune that with biological knowledge so it takes the next step and says in this specific situation, where I am working with a polyploid from genus X with a genome length of blah, GC content of blah, etc., which parameters make the most sense?
  - Can we have it adapt further steps based on what it learned in previous steps? Example, it runs iwgc-circos, notices GC content at a certain level, so in a different program further down the pipeline it adjusts a parameter to account for that?
