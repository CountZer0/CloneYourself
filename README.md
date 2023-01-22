# ConeYourself
All the dataset, config and libraries needed to clone yourself.

https://medium.com/@rioharper/cloneyourself-c4a0b1793997

## Installation
``` python pip install -r requirements.txt```

``` python pip install --upgrade openai wandb```

```python pip install python-dotenv```
## Setup
add these lines to your .env file in the project

#Environment variable:
WANDB_API_KEY=<YOUR_WANDB_API_KEY>
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>

## Weights & Balances
Setup account: https://wandb.ai/home
Authorize: https://wandb.ai/authorize

```wandb login --relogin```

```openai wandb sync```


## Train
```python ./datasetgenerator.py```

Choose (1) and enter data

Choose (2) to format model.json ->