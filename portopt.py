import pandas as pd
import numpy as np
from data.data import Dataloader
import datetime as dt

from qpsolvers import solve_qp

port = {"AAPL":(140.5, 1000),
		"META": (110.2, 300),
		"KO":(56.3, 400),
		"GOOGL":(95.35, 300)}
n_stocks = len(port)

start = dt.datetime(2022, 9, 1)
end = dt.datetime.today()

data = Dataloader(start=start, end=end, stocks=port)
r = data.calc_return()

C = r.cov().to_numpy()
expected_return = r.mean().to_numpy()
min_return = np.array([0.05])
A = np.ones((1, n_stocks))
b = np.ones((1))
ub, lb = np.ones((n_stocks)), np.zeros((n_stocks))
x = solve_qp(P=C, q=np.zeros((n_stocks)), G=-expected_return, h=-min_return, A=A, b=b, lb=lb, ub=ub, verbose=True, solver="quadprog")

print("Allocate...")
for idx, s in enumerate(port.keys()):
	print(f"	{s}: {x[idx]*100} %")
