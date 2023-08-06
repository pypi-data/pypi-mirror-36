Python pydecisions Library

Copyright (c) 2018 Balamurali M
Author: Balamurali M
Gmail: balamurali9m@gmail.com
License: MIT

This library includes of some of the techniques employed in making high level management decisions.
The following examples illustrate how to use this library.

1. Earned Value Management
Example:
a = evm(100,0.5,0.4,45)
print(a.result())
(where arg1 - Budget at Completion, arg2 - work planned to be completed at that point against the total work planned, arg3 - actual work completed at that point against the total work planned, arg4 - Actual Cost incurred till that point)

2. Financial functions
(a) Net Present Value
Example:
a = finance()
print(a.npv(.3,[-100,50,30,20,10]))
(where arg1 - rate, arg2 - yearly cash flows)

(b) Future Value
Example:
a = finance()
print(a.fv(0.10, 9, 300, 400))
(where arg1 - rate, arg2 - nos of years, arg3 - payment, arg4 - present value)

(c) Present Value
Example:
a = finance()
print(a.pv(0.05, 10, 100, 30000)) 
(where arg1 - rate, arg2 - no of years, arg3-payment, arg4 - future value)

(d) Internal Rate of Return
Example:
a = finance()
print(a.irr([-100,30,90,75,20]))
(where arg1 - cash flows yearly)

3. Simple Linear Regression
Example:
a = slr()
print(a.result([1,2,3,4],[1.5,2.5,3.3,4.2],3))
(where arg1 - training X, arg2 - training Y and arg3 - test X)

4. Statistical tests
(a)  T-test (mean of one group of scores)
Example:
a = statistics()
print(a.tt1([20,44,50,70,30],45)) 
(where arg1 - sample observations, arg2 - population mean)

(b) T-test (means of two independent samples of scores)
Example:
a = statistics()
print(a.ttind([50,40,90,30,40], [60,40,20,10,70]))
(where arg1 -  sample 1 observations, arg2 - sample 2 observations)

(c) T-test (2 related samples of data).
Example:
a = statistics()
print(a.ttrel([55,20,23,12,12], [22,48,11,17,12])) 
(where arg1 - sample 1 observations, arg2 - sample 2 observations)

5. Decision Analysis and Resolution
Example:
a = dar()
print(a.result([8,9],[7,6])) 
(where arg1 - criteria scores for Alternative 1 and arg2 - criteria scores for Alternative 2) 

6. Markov Chain
Example:
a = mc()
matrx = np.matrix([[0.7, 0.3],
                 [0.6, 0.4]]) 
I = np.matrix([[0.5, 0.5]])    
print(a.result(matrx,I,3))
(where matrx - the transition matrix, I - the current state matrix)

7. Bayes Rule
Example:
(For calculating P(A|B))
a = bayes()
print(a.result(0.6,0.4,0.2))
(where arg1 - P(A), arg2 - P(B), arg3 - P(B/A))

8. Linear Programming
Example:
Minimize: cost = -2*x[0] + 5*x[1], Subject to: -2*x[0] + 3*x[1] <= 7, 2*x[0] + 1*x[1] <= 5
x[1] >= -4 (where: -infinity <= x[0] <= infinity)

a = linprg()
c = [-2, 5]
A = [[-2, 3], [2, 1]]
b = [7, 5]
lp_x0b = (None, None)
lp_x1b = (-4, None)
print(a.result(c,A,b,lp_x0b,lp_x1b))

9.  Decision Trees – Regression
Example:
a = DTr()
x = [[1, 1.5, 7, 9, 10], [2, 2, 8, 9, 6]]
y = [1.5, 4.5]
z = [[1,6,8,4,2]]
a.result(x,y,z)
(where arg1 - training x, arg2 - training y and arg3 - test x)
Tree Image will be generated in the folder. When re-running, remember to delete the previously generated docs in the folder else you may get an error.

10. Decision Trees – Classification
Example:
a = DTc()
x = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 12]]
y = [1, 0]
z = [[1,6,8,4,2]]
a.result(x,y,z)
(where arg1 - training x, arg2 - training y and arg3 - test x)
Tree Image will be generated in the folder. When re-running, remember to delete the previously generated docs in the folder else you may get an error.

Some of the are completely written from scratch and some functions are built on the top of the existing standard library functions. 

Dependencies - numpy, scipy, sklearn and graphviz libraries