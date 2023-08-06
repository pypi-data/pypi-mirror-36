
# QuickNN

An implementation sklearn-like of FeedForward Neural Networks for quick applications. It can handle categorical
variables with one-hot-encoding(OHE) method batch-wise as well as continuous variables.

## Example

```python
from quicknn import QuickNN

# load X_train, X_test, y_train, y_test

qdnn = QuickNN(list_neurons=[100, 100, 1])
qnn.fit(X_train, y_train)
y_pred = qnn.predict(X_test)
```

## Installing

```bash
$ pip install quicknn
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](License.md) file for details.
