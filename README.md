# Battery-Predictor

Predicts how much battery life your laptop has left. It uses univariate linear regression trained with **batch gradient descent that I wrote by hand**: no scikit-learn, just NumPy.

The repo includes a model trained on my laptop, plus a logger script, so you can collect data from your own laptop and train the model on that.

## How it works

The model fits battery % as a linear function of hours elapsed:

```
f(x) = w·x + b
```

- **Cost:** mean squared error, `J(w,b) = (1/2m) Σ (f(xᵢ) − yᵢ)²`
- **Gradients:** `∂J/∂w = (1/m) Σ (f(xᵢ) − yᵢ)·xᵢ` and `∂J/∂b = (1/m) Σ (f(xᵢ) − yᵢ)`
- **Update:** `w` and `b` are updated together on every iteration using the full dataset, which makes it *batch* GD. Training stops when the cost changes by less than `1e-7`.

`w` is the drain rate in % per hour (negative, since the battery goes down) and `b` is the starting battery %. To get the time left at battery level `p`, work out how long until the battery reaches 0%:

```
hours_left = −p / w
```

## Files

| File | What it does |
|---|---|
| `battery_logger.py` | Logs your battery % once a minute to a CSV |
| `linear_regression.py` | Trains the model on `data/battery_data.csv` and saves it to `model.json` |
| `predict.py` | Uses `model.json` to predict how much time you have left |
| `training.ipynb` | The notebook version of training, with plots of the data and of the fit converging |
| `model.json` | The trained model (`w` and `b`) from my laptop |
| `data/battery_data.csv` | The session the included model was trained on |
| `data/session_*.csv` | Raw logging sessions |

## Quick start

```bash
pip install -r requirements.txt
python predict.py
```

`predict.py` asks for your current battery %, then prints how much time the model predicts you have left, next to your operating system's own estimate.

> The included `model.json` is trained on **my** laptop. Drain rate depends on the battery, screen and how the laptop is used, so the prediction may be off for yours. To get accurate predictions, collect your own data and retrain (see below).

## Collect data from your own laptop

`battery_logger.py` uses [`psutil`](https://psutil.readthedocs.io/) to read your battery % once a minute and saves it to a CSV file.

### 1. Get ready

- **Charge to 100%, then unplug before starting the logger.** The model only covers draining, so the logger stops as soon as it detects the charger. If you start it while plugged in, it will exit immediately.
- **Stop your laptop from sleeping.** Logging pauses while the laptop is asleep, which leaves gaps in the data.
  - **Windows:** Settings → System → Power & battery → Screen and sleep → set "When on battery power, put my device to sleep after" to **Never**.
  - **macOS:** run the logger with `caffeinate -i` (see below), which keeps the Mac awake for as long as the script is running.
  - **Linux:** run the logger with `systemd-inhibit` (see below), or turn off automatic suspend in your power settings.
- **Optional:** turn off battery saver / Low Power Mode so it doesn't kick in partway through and change how fast the battery drains.
- **Use the laptop normally.** The data reflects how you use it, so a session of watching videos will drain faster than one of writing notes.

### 2. Start logging

```bash
# Windows
python battery_logger.py

# macOS
caffeinate -i python3 battery_logger.py

# Linux
systemd-inhibit python3 battery_logger.py
```

The script writes one row per minute to a new file named `data/session_YYYY-MM-DD-HH-MM.csv`:

```
hours,battery_pct
0.0,100
0.0167,100
0.0333,99
...
```

Each row is saved as soon as it's written, so you won't lose data if the script stops unexpectedly.

### 3. Stop logging

Press **Ctrl+C** when you're done, ideally once the battery is low (around 10–20%), or plug the charger back in. Longer sessions give the model more to learn from.

> Desktop PCs don't have a battery, so the logger only works on laptops.

## Train the model

`linear_regression.py` trains on `data/battery_data.csv`. To train on your own session, copy it over that file:

```bash
cp data/session_2026-11-05-14-30.csv data/battery_data.csv
python linear_regression.py
```

This overwrites `model.json` with your model, so `predict.py` will use your laptop's data from then on.

**If the cost blows up to `inf` or `nan`:** lower the learning rate (`alpha`, the `0.1` near the end of the script). How large a learning rate gradient descent can handle depends on how long the session is. `0.1` works for sessions up to about 7 hours, and `0.05` for sessions up to about 10 hours.

## Results

Trained on TODO readings from my laptop, taken once a minute over TODO hours (100% → TODO%).

| | w (%/hour) | b (%) |
|---|---|---|
| My gradient descent | TODO | TODO |
| `np.polyfit` (check) | TODO | TODO |

So my laptop drains about **TODO% per hour**, and a full charge lasts about **TODO hours** (`100 / |w|`).

## Limitations

- Real battery drain isn't perfectly linear, especially near 0% and 100%.
- The drain rate depends on usage (screen brightness, apps, CPU load), so adding features like these would turn this into multivariate regression. `psutil` can also log things like CPU usage, which could be a good next step.
