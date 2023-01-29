# ConeYourself
All the dataset, config and libraries needed to clone yourself.

https://medium.com/@rioharper/cloneyourself-c4a0b1793997

## Installation
```pip install -r requirements.txt```

```pip install --upgrade openai wandb```

```pip install python-dotenv```
## Setup
Set these in your System-User environment variables

#Environment variable:
WANDB_API_KEY=<YOUR_WANDB_API_KEY>
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
WANDB_MODE=online

## Weights & Balances
Setup account: https://wandb.ai/home
Authorize: https://wandb.ai/authorize

```wandb login --relogin```

```openai wandb sync```


## Train
```python ./datasetgenerator.py```

Choose (1) and enter data

Choose (2) to format model.json ->