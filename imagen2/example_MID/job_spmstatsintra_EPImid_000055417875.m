% Onsets names:
cond = struct('name',  { 'anticip_hit_largewin', 'anticip_hit_smallwin', 'anticip_hit_nowin', 'anticip_missed_largewin', 'anticip_missed_smallwin', 'anticip_missed_nowin', 'anticip_noresp', 'feedback_hit_largewin', 'feedback_hit_smallwin', 'feedback_hit_nowin', 'feedback_missed_largewin', 'feedback_missed_smallwin', 'feedback_missed_nowin', 'feedback_noresp', 'pressleft', 'pressright' }, ...
'onset', { [20.2790 40.2990 80.2930 120.2830 180.2730 220.3010 240.3030 260.3020 300.2710 320.3070 350.3050 380.3040 400.2950 500.3050 520.2980 540.2930 560.2980 580.3080 610.3060 630.2710 640.2730],
[10.2920 60.2830 100.2880 130.2880 150.2860 170.2710 210.3040 230.2880 270.2850 310.2690 340.2890 370.2970 410.2740 440.2740 460.2860 480.2800 510.2830 550.3000 570.2980 590.2940 650.2870],
nan,
nan,
[190.2980],
nan,
[0.3000 30.3020 50.2990 70.2850 90.2760 110.3050 140.2700 160.2950 200.3010 250.2720 280.2900 290.2890 330.3060 360.2830 390.2740 420.2780 430.2780 450.2810 470.2870 490.2760 530.3070 600.3040 620.3030],
[24.6570 44.9380 84.8940 124.7980 184.6930 225.0670 245.1000 265.0870 304.6640 325.1520 355.1220 385.1150 404.9890 505.1220 525.0270 544.9650 565.0330 585.1480 615.1340 634.6680 644.6910],
[14.8230 64.7340 104.8470 134.8780 154.8640 174.6700 215.1050 234.9000 274.8490 314.6380 344.9040 375.0190 414.7070 444.7020 464.8730 484.7810 514.8240 555.0560 575.0250 594.9810 654.8770],
nan,
nan,
[195.0300],
nan,
[4.8760 34.9690 54.9380 74.7750 94.6760 115.0900 144.6310 164.9950 205.0730 254.6850 284.9190 294.9130 335.1380 364.8270 394.7080 424.7610 434.7460 454.8060 474.8860 494.7270 535.1470 605.1080 625.0950],
[14.7990 24.6310 84.8390 124.7030 154.7190 174.5660 194.6540 214.9660 244.9980 264.9500 274.7500 314.5490 354.9970 404.8930 414.6930 444.5810 514.7480 524.9480 554.9720 585.0680 634.6270],
[44.8870 64.6870 104.7430 134.7750 184.5820 224.9500 234.7740 304.5260 325.0370 344.7970 374.8930 385.0610 464.8690 484.7080 504.9960 544.8680 564.9320 574.9080 594.8280 614.9880 644.6350 654.7790] }', ...
'duration', { [4.0], [4.0], nan, nan, [4.0], nan, [4.0], [1.45], [1.45], nan, nan, [1.45], nan, [1.45], [0.], [0.] })

consess{1}.tcon.name = 'unestimable (was anticip) replaced by dummy';
consess{1}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{2}.tcon.name = 'unestimable (was anticip_hit) replaced by dummy';
consess{2}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{3}.tcon.name = 'unestimable (was anticip_missed) replaced by dummy';
consess{3}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{4}.tcon.name = 'anticip_noresp';
consess{4}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{5}.tcon.name = 'unestimable (was anticip_hit-missed) replaced by dummy';
consess{5}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{6}.tcon.name = 'unestimable (was anticip_missed-hit) replaced by dummy';
consess{6}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{7}.tcon.name = 'unestimable (was anticip_hit-noresp) replaced by dummy';
consess{7}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{8}.tcon.name = 'unestimable (was anticip_noresp-hit) replaced by dummy';
consess{8}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{9}.tcon.name = 'anticip_hit_largewin - smallwin';
consess{9}.tcon.convec = [1.0 -1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{10}.tcon.name = 'unestimable (was anticip_hit_largewin - nowin) replaced by dummy';
consess{10}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{11}.tcon.name = 'unestimable (was anticip_hit_smallwin - nowin) replaced by dummy';
consess{11}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{12}.tcon.name = 'unestimable (was anticip_missed_largewin - smallwin) replaced by dummy';
consess{12}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{13}.tcon.name = 'unestimable (was anticip_missed_largewin - nowin) replaced by dummy';
consess{13}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{14}.tcon.name = 'unestimable (was anticip_missed_smallwin - nowin) replaced by dummy';
consess{14}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{15}.tcon.name = 'unestimable (was anticip - anticip_noresp) replaced by dummy';
consess{15}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{16}.tcon.name = 'unestimable (was feedback) replaced by dummy';
consess{16}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{17}.tcon.name = 'unestimable (was feedback_hit) replaced by dummy';
consess{17}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{18}.tcon.name = 'unestimable (was feedback_missed) replaced by dummy';
consess{18}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{19}.tcon.name = 'unestimable (was feedback_hit-missed) replaced by dummy';
consess{19}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{20}.tcon.name = 'unestimable (was feedback_missed-hit) replaced by dummy';
consess{20}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{21}.tcon.name = 'feedback_hit_largewin - smallwin';
consess{21}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 -1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{22}.tcon.name = 'unestimable (was feedback_hit_largewin - nowin) replaced by dummy';
consess{22}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{23}.tcon.name = 'unestimable (was feedback_hit_smallwin - nowin) replaced by dummy';
consess{23}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{24}.tcon.name = 'unestimable (was feedback_missed_largewin - smallwin) replaced by dummy';
consess{24}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{25}.tcon.name = 'unestimable (was feedback_missed_largewin - nowin) replaced by dummy';
consess{25}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{26}.tcon.name = 'unestimable (was feedback_missed_smallwin - nowin) replaced by dummy';
consess{26}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{27}.tcon.name = 'press L + R';
consess{27}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.5 0.5 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{28}.tcon.name = 'press L - R';
consess{28}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 -1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{29}.tcon.name = 'press R - L';
consess{29}.tcon.convec = [-0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -1.0 1.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0 -0.0];
consess{30}.tcon.name = 'unestimable (was anticip_hit_somewin - nowin) replaced by dummy';
consess{30}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{31}.tcon.name = 'unestimable (was anticip_missed_somewin - nowin) replaced by dummy';
consess{31}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{32}.tcon.name = 'unestimable (was feedback_hit_somewin - nowin) replaced by dummy';
consess{32}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{33}.tcon.name = 'unestimable (was feedback_missed_somewin - nowin) replaced by dummy';
consess{33}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{34}.tcon.name = 'unestimable (was feedback_somewin_hit - missed) replaced by dummy';
consess{34}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{35}.tcon.name = 'unestimable (was feedback_somewin_missed - hit) replaced by dummy';
consess{35}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{36}.tcon.name = 'unestimable (was feedback_somewin - nowin) replaced by dummy';
consess{36}.tcon.convec = [0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0];
consess{37}.fcon.name = 'unestimable (was Effect of interest) replaced by dummy';
consess{37}.fcon.convec = {[0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000]}';
consess{38}.fcon.name = 'unestimable (was Anticip_hit_GainEffect) replaced by dummy';
consess{38}.fcon.convec = {[0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000]}';
consess{39}.fcon.name = 'unestimable (was Anticip_missed_GainEffect) replaced by dummy';
consess{39}.fcon.convec = {[0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000]}';
consess{40}.fcon.name = 'unestimable (was Feedback_hit_GainEffect) replaced by dummy';
consess{40}.fcon.convec = {[0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000]}';
consess{41}.fcon.name = 'unestimable (was Feedback_missed_GainEffect) replaced by dummy';
consess{41}.fcon.convec = {[0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 1.0000]}';
consess{42}.fcon.name = 'Effect of rp';
consess{42}.fcon.convec = {[0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000]}';
consess{43}.fcon.name = 'Effect of rp high';
consess{43}.fcon.convec = {[0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000]}';
% % Onsets time definition exemple %
% cond(1).name = 'Auditory_math';
% cond(1).onset = [35.40599823 44.70899963 48.00500107 83.41600037 108.01599884 135.01199341 137.70599365 173.70700073 191.70599365 251.70599365];
% cond(1).duration = [0 0 0 0 0 0 0 0 0 0];
% %cond(1).tmod = 0;
% %cond(1).pmod = struct('name', {}, 'param', {}, 'poly', {});

% % Contrasts Definition exemple %
% consess{1}.tcon.name = 'Auditory_math';
% consess{1}.tcon.convec = [1 0 0    0 0 0 0 0 0 0];
% % %consess{1}.tcon.sessrep = 'none';

spm()
spm_jobman('initcfg')

%-----------------------------------------------------------------------
% Job configuration created by cfg_util (rev $Rev: 2787 $)
%-----------------------------------------------------------------------
matlabbatch{1}.cfg_basicio.cfg_cd.dir = {'/volatile/thyreau/dataimagen/tmp/fmri_model_000055417875/SessionB/EPI_short_MID'};
matlabbatch{2}.cfg_basicio.cfg_named_file.name = 'orig';
matlabbatch{2}.cfg_basicio.cfg_named_file.files = {
                                                   {'wea000055417875s005a1001.nii'}
                                                   {'rpL_a000055417875s005a1001.txt'}
                                                   }';
	matlabbatch{3}.spm.spatial.smooth.data(1) = cfg_dep;
	matlabbatch{3}.spm.spatial.smooth.data(1).tname = 'Images to Smooth';
	matlabbatch{3}.spm.spatial.smooth.data(1).tgt_spec = {};
	matlabbatch{3}.spm.spatial.smooth.data(1).sname = 'Named File Selector: orig(1) - Files';
	matlabbatch{3}.spm.spatial.smooth.data(1).src_exbranch = substruct('.','val', '{}',{2}, '.','val', '{}',{1});
	matlabbatch{3}.spm.spatial.smooth.data(1).src_output = substruct('.','files', '{}',{1});
	matlabbatch{3}.spm.spatial.smooth.fwhm = [5 5 5];
	matlabbatch{3}.spm.spatial.smooth.dtype = 0;
	matlabbatch{3}.spm.spatial.smooth.prefix = 's';

%NOSMOOTH%matlabbatch{3}.cfg_basicio.cfg_named_input.name = 'dummy';
%NOSMOOTH%matlabbatch{3}.cfg_basicio.cfg_named_input.input = 'dummy';

matlabbatch{4}.cfg_basicio.cfg_named_file.name = 'vol4Dselected';
matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1) = cfg_dep;
matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).tname = 'File Set';

%NOSMOOTH%matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).tgt_spec = {};
%NOSMOOTH%matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).sname = 'Named File Selector: orig(1) - Files';
%NOSMOOTH%matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).src_exbranch = substruct('.','val', '{}',{2}, '.','val', '{}',{1});
%NOSMOOTH%matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).src_output = substruct('.','files', '{}',{1});

	matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).tgt_spec{1}(1).name = 'filter';
	matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).tgt_spec{1}(1).value = 'image';
	matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).tgt_spec{1}(2).name = 'strtype';
	matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).tgt_spec{1}(2).value = 'e';
	matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).sname = 'Smooth: Smoothed Images';
	matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).src_exbranch = substruct('.','val', '{}',{3}, '.','val', '{}',{1}, '.','val', '{}',{1});
	matlabbatch{4}.cfg_basicio.cfg_named_file.files{1}(1).src_output = substruct('.','files');

matlabbatch{5}.spm.util.exp_frames.files(1) = cfg_dep;
matlabbatch{5}.spm.util.exp_frames.files(1).tname = 'NIfTI file(s)';
matlabbatch{5}.spm.util.exp_frames.files(1).tgt_spec = {};
matlabbatch{5}.spm.util.exp_frames.files(1).sname = 'Named File Selector: vol4Dselected(1) - Files';
matlabbatch{5}.spm.util.exp_frames.files(1).src_exbranch = substruct('.','val', '{}',{4}, '.','val', '{}',{1});
matlabbatch{5}.spm.util.exp_frames.files(1).src_output = substruct('.','files', '{}',{1});
matlabbatch{5}.spm.util.exp_frames.frames = Inf;
matlabbatch{6}.spm.stats.fmri_spec.dir = {'/volatile/thyreau/dataimagen/tmp/fmri_model_000055417875/SessionB/EPI_short_MID'};
matlabbatch{6}.spm.stats.fmri_spec.timing.units = 'secs';
matlabbatch{6}.spm.stats.fmri_spec.timing.RT = 2.2;
matlabbatch{6}.spm.stats.fmri_spec.timing.fmri_t = 16;
matlabbatch{6}.spm.stats.fmri_spec.timing.fmri_t0 = 1;
matlabbatch{6}.spm.stats.fmri_spec.sess.scans(1) = cfg_dep;
matlabbatch{6}.spm.stats.fmri_spec.sess.scans(1).tname = 'Scans';
matlabbatch{6}.spm.stats.fmri_spec.sess.scans(1).tgt_spec = {};
matlabbatch{6}.spm.stats.fmri_spec.sess.scans(1).sname = 'Expand image frames: Expanded filename list.';
matlabbatch{6}.spm.stats.fmri_spec.sess.scans(1).src_exbranch = substruct('.','val', '{}',{5}, '.','val', '{}',{1}, '.','val', '{}',{1});
matlabbatch{6}.spm.stats.fmri_spec.sess.scans(1).src_output = substruct('.','files');

matlabbatch{6}.spm.stats.fmri_spec.sess.cond = cond;

matlabbatch{6}.spm.stats.fmri_spec.sess.multi = {''};
matlabbatch{6}.spm.stats.fmri_spec.sess.regress = struct('name', {}, 'val', {});
matlabbatch{6}.spm.stats.fmri_spec.sess.multi_reg(1) = cfg_dep;
matlabbatch{6}.spm.stats.fmri_spec.sess.multi_reg(1).tname = 'Multiple regressors';
matlabbatch{6}.spm.stats.fmri_spec.sess.multi_reg(1).tgt_spec = {};
matlabbatch{6}.spm.stats.fmri_spec.sess.multi_reg(1).sname = 'Named File Selector: orig(2) - Files';
matlabbatch{6}.spm.stats.fmri_spec.sess.multi_reg(1).src_exbranch = substruct('.','val', '{}',{2}, '.','val', '{}',{1});
matlabbatch{6}.spm.stats.fmri_spec.sess.multi_reg(1).src_output = substruct('.','files', '{}',{2});
matlabbatch{6}.spm.stats.fmri_spec.sess.hpf = 128;
matlabbatch{6}.spm.stats.fmri_spec.fact = struct('name', {}, 'levels', {});
matlabbatch{6}.spm.stats.fmri_spec.bases.hrf.derivs = [0 0];
matlabbatch{6}.spm.stats.fmri_spec.volt = 1;
matlabbatch{6}.spm.stats.fmri_spec.global = 'None';
matlabbatch{6}.spm.stats.fmri_spec.mask = {'/neurospin/imagen/workspace/fmri/scripts/mask_dilated.nii,1'}; % spm brainmask.nii prior at > 0.01
matlabbatch{6}.spm.stats.fmri_spec.cvi = 'AR(1)';
matlabbatch{7}.spm.stats.fmri_est.spmmat(1) = cfg_dep;
matlabbatch{7}.spm.stats.fmri_est.spmmat(1).tname = 'Select SPM.mat';
matlabbatch{7}.spm.stats.fmri_est.spmmat(1).tgt_spec = {};
matlabbatch{7}.spm.stats.fmri_est.spmmat(1).sname = 'fMRI model specification: SPM.mat File';
matlabbatch{7}.spm.stats.fmri_est.spmmat(1).src_exbranch = substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1});
matlabbatch{7}.spm.stats.fmri_est.spmmat(1).src_output = substruct('.','spmmat');
matlabbatch{7}.spm.stats.fmri_est.method.Classical = 1;
matlabbatch{8}.spm.stats.con.spmmat(1) = cfg_dep;
matlabbatch{8}.spm.stats.con.spmmat(1).tname = 'Select SPM.mat';
matlabbatch{8}.spm.stats.con.spmmat(1).tgt_spec = {};
matlabbatch{8}.spm.stats.con.spmmat(1).sname = 'Model estimation: SPM.mat File';
matlabbatch{8}.spm.stats.con.spmmat(1).src_exbranch = substruct('.','val', '{}',{6}, '.','val', '{}',{1}, '.','val', '{}',{1});
matlabbatch{8}.spm.stats.con.spmmat(1).src_output = substruct('.','spmmat');

matlabbatch{8}.spm.stats.con.consess = consess ;

matlabbatch{8}.spm.stats.con.delete = 1;

%matlabbatch{9}.spm.stats.results.spmmat(1) = cfg_dep;
%matlabbatch{9}.spm.stats.results.spmmat(1).tname = 'Select SPM.mat';
%matlabbatch{9}.spm.stats.results.spmmat(1).tgt_spec{1}(1).name = 'filter';
%matlabbatch{9}.spm.stats.results.spmmat(1).tgt_spec{1}(1).value = 'mat';
%matlabbatch{9}.spm.stats.results.spmmat(1).tgt_spec{1}(2).name = 'strtype';
%matlabbatch{9}.spm.stats.results.spmmat(1).tgt_spec{1}(2).value = 'e';
%matlabbatch{9}.spm.stats.results.spmmat(1).sname = 'Contrast Manager: SPM.mat File';
%matlabbatch{9}.spm.stats.results.spmmat(1).src_exbranch = substruct('.','val', '{}',{8}, '.','val', '{}',{1}, '.','val', '{}',{1});
%matlabbatch{9}.spm.stats.results.spmmat(1).src_output = substruct('.','spmmat');
%matlabbatch{9}.spm.stats.results.conspec.titlestr = '';
%matlabbatch{9}.spm.stats.results.conspec.contrasts = Inf;
%matlabbatch{9}.spm.stats.results.conspec.threshdesc = 'none';
%matlabbatch{9}.spm.stats.results.conspec.thresh = 0.001;
%matlabbatch{9}.spm.stats.results.conspec.extent = 0;
%matlabbatch{9}.spm.stats.results.conspec.mask = struct('contrasts', {}, 'thresh', {}, 'mtype', {});
%matlabbatch{9}.spm.stats.results.print = true;
%
spm_jobman('run_nogui', matlabbatch)
