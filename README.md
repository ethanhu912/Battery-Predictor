# Battery-Predictor

Predicts how much battery life your phone has left. It uses univariate linear regression trained with **batch gradient descent that I wrote by hand**: no scikit-learn, just NumPy.

## How it works

The model fits battery % as a linear function of minutes elapsed:

```
f(x) = w·x + b
```

- **Cost:** mean squared error, `J(w,b) = (1/2m) Σ (f(xᵢ) − yᵢ)²`
- **Gradients:** `∂J/∂w = (1/m) Σ (f(xᵢ) − yᵢ)·xᵢ` and `∂J/∂b = (1/m) Σ (f(xᵢ) − yᵢ)`
- **Update:** `w` and `b` are updated together on every iteration using the full dataset, which makes it *batch* GD. Training stops when the cost changes by less than `1e-7`.

## Data

`battery_data.csv` has 21 readings of my phone's battery %, taken every 15 minutes over 5 hours (100% → 22%).

## Results

| | w (%/min) | b (%) |
|---|---|---|
| My gradient descent | −0.2555 | 99.90 |
| `np.polyfit` (check) | −0.2562 | 100.05 |

So the phone drains about **15% per hour**, and a full charge lasts about **6.5 hours**.
To estimate the time left at battery level `p`: `minutes_left = p / |w|`. For example, at 50% that's about 3h 15m.

## Run it

```bash
pip install -r requirements.txt
python linear_regression.py
```

`training.ipynb` is the original notebook version, which includes plots of the data and of the fit converging.

## Planned

A small CLI script: you enter your current battery %, and it tells you how much time you have left.

## Limitations

- Real battery drain isn't perfectly linear, especially near 0% and 100%.
- The drain rate depends on usage (screen time, apps), so adding features like these would turn this into multivariate regression.
