import matplotlib.pyplot as plt

fig = plt.figure(figsize=(8, 5))
ax = fig.gca()
ax.set_title('Time', fontsize=16)
ax.set_xlabel('Samples')
ax.set_ylabel('Voltage')
ax.grid(True, which='both')
l2d=ax.plot([0,1,4,9,16,25],'r')

fig2 = plt.figure(figsize=(8, 5))
ax2 = fig2.gca()
ax2.set_title('Init Figure', fontsize=16)
ax2.grid(True, which='both')
ax2.plot([0,1,2,3,4,5])
ax2.clear()
fig2.gca().add_line(ax2)

plt.show()