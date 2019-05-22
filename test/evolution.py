import matplotlib.pyplot as plt
import numpy as np
import hanabi
import hanabi.ai as ai

data=[10.91,17.578]

fig=plt.figure()
x=[1,2,3]
height=[10.91,17.578,18.819]
width=0.05
BarName=['Version 1', 'Version 2','Version 3']
plt.xticks(x, BarName, rotation=40)
plt.bar(x,height,width, color='b')
plt.savefig('SimpleBar.png')
plt.title('Evolution of our AI')
plt.show()
