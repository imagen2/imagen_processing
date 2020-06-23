import scipy.io
import matplotlib.pyplot as plt
import numpy as np


th_path = '/volatile/rc244162/SPM.mat'
caps_path = '/volatile/rc244162/capsul/ft1level/out/BL000012029891/3-Level1Design/SPM.mat'

TH = scipy.io.loadmat(th_path)
CAPS = scipy.io.loadmat(caps_path)

th_names = [name[0] for name in TH['SPM']['xX'][0, 0]['name'][0, 0][0]]
caps_names = [name[0] for name in CAPS['SPM']['xX'][0, 0]['name'][0, 0][0]]
new_caps_names = []
for name in caps_names:
    new_caps_names.append(name.replace('Realign', 'R').replace('faces_', ''))

assert set(new_caps_names) == set(th_names)

TH_X = TH['SPM']['xX'][0, 0]['X'][0, 0]
CAPS_X = CAPS['SPM']['xX'][0, 0]['X'][0, 0]

new_CAPS_X = np.zeros_like(CAPS_X)
for th_idx, th_name in enumerate(th_names):
    caps_idx = new_caps_names.index(th_name)
    new_CAPS_X[:, th_idx] = CAPS_X[:, caps_idx]

print (TH_X - new_CAPS_X).max()

plt.figure()
plt.grid()
plt.subplot(1, 2, 1)
plt.imshow(TH_X[:, :11], aspect='auto', interpolation='nearest', )
plt.title('Thyreau')
plt.subplot(1, 2, 2)
plt.imshow(new_CAPS_X[:, :11], aspect='auto', interpolation='nearest')
plt.title('CAPS')

plt.figure()
plt.grid()
plt.subplot(1, 2, 1)
plt.imshow(TH_X, aspect='auto', interpolation='nearest')
plt.title('Thyreau')
plt.subplot(1, 2, 2)
plt.imshow(new_CAPS_X, aspect='auto', interpolation='nearest')
plt.title('CAPS')

plt.figure()
plt.grid()
plt.imshow(TH_X - new_CAPS_X, aspect='auto', interpolation='nearest')
plt.title('Difference')
# plt.show()

plt.figure()
plt.grid()
plt.imshow(TH_X[:, :11] - new_CAPS_X[:, :11], aspect='auto', interpolation='nearest')
plt.title('Difference')
plt.show()
