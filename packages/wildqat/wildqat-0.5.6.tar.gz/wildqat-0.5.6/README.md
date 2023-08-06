Wildqat Python SDK
--------
Python Framework for QUBO 

Version
--------
0.5.6

Install
--------------------

```
$ pip3 install wildqat
```

or

```
$ git clone https://github.com/mdrft/Wildqat.git
$ python setup.py install
```

Example
-------

```python
import wildqat as wq
a = wq.opt()
a.qubo = [[4,-4,-4],[0,4,-4],[0,0,4]]
a.sa() #=> [1, 1, 1]
print(a.E[-1]) #=>[0.0]
```

Energy Function
-------
Energy function of the calculation is stored in attribute E as an array.
```python

print(a.E[-1]) #=>[0.0]

#if you want to check the time evolution
a.plot()
```

Functions
-------

sel(N,K,array)  
Automatically create QUBO which select K qubits from N qubits
```python
print(wq.sel(5,2))
#=>
[[-3  2  2  2  2]
 [ 0 -3  2  2  2]
 [ 0  0 -3  2  2]
 [ 0  0  0 -3  2]
 [ 0  0  0  0 -3]]
```

if you set array on the 3rd params, the result likely to choose the nth qubit in the array
```python
print(wq.sel(5,2,[0,2]))
#=>
[[-3.5  2.   2.   2.   2. ]
 [ 0.  -3.   2.   2.   2. ]
 [ 0.   0.  -3.5  2.   2. ]
 [ 0.   0.   0.  -3.   2. ]
 [ 0.   0.   0.   0.  -3. ]]
```

net(arr,N)  
Automatically create QUBO which has value 1 for all connectivity defined by array of edges and graph size N
```python
print(wq.net([[0,1],[1,2]],4))
#=>
[[0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 0.]
 [0. 0. 0. 0.]]
```
this create 4*4 QUBO and put value 1 on connection between 0th and 1st qubit, 1st and 2nd qubit  

zeros(N)
Create QUBO with all element value as 0
```python
print(wq.zeros(3))
#=>
[[0. 0. 0.]
 [0. 0. 0.]
 [0. 0. 0.]]
```

diag(list)
Create QUBO with diag from list
```python
print(wq.diag([1,2,1]))
#=>
[[1 0 0]
 [0 2 0]
 [0 0 1]]
```

Tutorial
----------

日本語  
https://github.com/mdrft/Wildqat/tree/master/examples_ja

Authors
----------
<a href="https://github.com/minatoyuichiro">Yuichiro Minato</a>(MDR), <a href="https://github.com/Morning777">Asa Eagle</a>(MDR), [Satoshi Takezawa](https://github.com/takebozu)(TerraSky), [Seiya Sugo](https://github.com/seiya-sugo)(TerraSky)

Disclaimer
----------
Copyright 2018 The Wildqat Developers.

