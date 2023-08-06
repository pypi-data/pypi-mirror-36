
# QuickNN

An implementation of Feedforward Neural Networks for quick applications.

* The training phase can be stopped, some parameters on fit method can be changed and then the training can be resumed
with the same weights of the last interruption.
* If feed with pandas objects it can handle categorical variables with one-hot-encoding(OHE) method batch-wise as well
as continuous variables.
* Easy visualization in [Tensorboard](https://www.tensorflow.org/guide/summaries_and_tensorboard) of the metrics provided.
* Inner management of the validation set in the training phase.

## Example

```python
from quicknn import QuickNN
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

X, y = load_boston(return_X_y=True)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25)

qnn = QuickNN(list_neurons=[100, 200, 1])
qnn.fit(X_train, y_train, n_epochs=10) ## In IPython session you can stop-change-resume the training
qnn.fit(X_train, y_train, n_epochs=20) ## just increasing the n_epochs.
qnn.fit(X_train, y_train, learning_rate=0.01) ## you can change e.g., the learning_rate param while training
y_pred = qnn.predict(X_val)

score = mean_squared_error(y_val, y_pred)

```

## Installing
The dependencies are showed in [requirements.txt](requirements.txt), which can be installed with the command:
```bash
$ pip install -r requirements.txt
```
Then the library can easily downloaded through pip:
```bash
$ pip install quicknn
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Reference
* [IPython](https://ipython.org/)
* [Tensor](https://www.tensorflow.org/)
* [pandas](https://pandas.pydata.org/)
* [scikit-learn](http://scikit-learn.org/stable/)
* [path.py](https://github.com/jaraco/path.py)
