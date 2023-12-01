Most of my data is recorded in semi-readable form in the reports folder.

The generate_reports.ipynb file is contains the code behind both my predictivity and faithfulness experiments.

Everything is deterministic except GPT-4's outputs, which are cached and reused whenever GPT-4 is prompted with a prompt that has been used before.

To understand this codebase, I'd suggest:
- reading the header of utils.rules.generateBalanced 
- reading the headers of the 2 big functions at the top of generate_reports.ipynb 
- picking a rule you like and reading a report for that rule
- finding where that rule's reports are generated in generate_reports, and reading the implementations of its sample generator and scoring rule