
# QuickDNN

An implementation sklearn-like of FeedForward Neural Networks for quick applications. It can handle categorical
variables with one-hot-encoding(OHE) method batch-wise as well as continuous variables.

## Example

```python
from quickdnn import QuickDNN

# load X_train, X_test, y_train, y_test

qdnn = QuickDNN(list_neurons=[100, 100, 1]) # two hidden layers with 100 neurons each and 1 output neuron. 
qdnn.fit(X_train, y_train) # training phase
y_pred = qdnn.predict(X_test) # predicting phase
```

## Installing

```bash
$ pip install quickdnn
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](License.md) file for details.
