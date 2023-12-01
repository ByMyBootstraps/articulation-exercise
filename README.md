Most of my data is recorded in semi-readable form in the reports folder.

The generate_reports.ipynb file is contains the code behind both my predictivity and faithfulness experiments.

Everything is deterministic except GPT-4's outputs, which are cached and reused whenever GPT-4 is prompted with a prompt that has been used before.