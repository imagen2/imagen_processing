TH = load('/neurospin/tmp/frouin/benchmark/thyreau/000095300616/SPM.mat' ,'SPM')
CAPS = load('/neurospin/tmp/frouin/capsul/ft1level/out/BL000095300616/6-EstimateContrast/SPM.mat' ,'SPM')
figure
subplot(1,2,1)
image(TH.SPM.xX.X(:,1:11), 'CDataMapping', 'scaled')
title=('Thyreau')
subplot(1,2,2)
image(CAPS.SPM.xX.X(:,1:11), 'CDataMapping', 'scaled')
title=('Caps')

figure
subplot(1,2,1)
image(TH.SPM.xX.X, 'CDataMapping', 'scaled')
title=('Thyreau')
subplot(1,2,2)
image(CAPS.SPM.xX.X, 'CDataMapping', 'scaled')
title=('Caps')
