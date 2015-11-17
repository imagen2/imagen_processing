% Onsets names:
cond = struct('name',  { 'go_success', 'go_toolate', 'go_wrong', 'stop_success', 'stop_failure' }, ...
'onset', { [1.97 3.85 5.73 7.77 9.50 11.46 15.43 17.22 18.93 20.67 24.57 26.50 28.45 32.19 34.28 36.27 40.10 43.75 45.58 47.42 49.39 51.33 57.05 58.97 60.91 62.87 64.90 66.82 70.59 72.67 74.74 76.63 78.51 80.59 82.48 86.16 87.96 89.90 91.75 93.54 95.53 97.45 101.54 103.39 105.11 107.05 110.86 112.77 114.62 116.34 118.42 122.28 124.17 126.07 130.19 131.90 133.94 135.66 137.64 141.15 142.86 144.82 146.77 150.23 151.97 153.70 155.49 157.46 159.32 161.41 165.39 167.20 169.20 171.28 173.32 175.04 178.83 180.70 182.60 184.49 186.51 188.59 190.60 194.43 196.27 198.11 200.08 202.12 204.20 207.94 209.80 211.90 217.51 219.33 221.37 223.17 224.89 228.95 230.90 232.88 236.32 238.25 240.13 241.94 243.84 245.86 247.77 249.54 253.34 255.14 257.18 258.98 261.03 262.86 266.61 268.55 270.41 272.47 276.40 278.12 280.20 283.71 285.65 287.44 289.32 292.75 294.52 296.43 300.26 302.09 304.07 305.99 307.87 309.84 311.88 315.43 317.37 319.42 321.33 323.06 327.23 329.04 330.98 332.81 336.62 340.33 342.42 345.93 347.74 349.52 351.33 353.33 357.10 358.83 360.65 362.54 366.57 368.29 370.22 371.98 375.70 377.44 379.47 381.35 383.09 384.99 388.70 390.52 392.28 394.18 396.14 400.22 401.95 403.73 405.58 409.36 411.13 413.02 414.95 416.84 420.57 422.60 424.38 428.17 430.26 432.05 434.15 435.93 437.83 441.75 443.57 445.46 447.54 449.55 453.22 455.31 457.25 459.05 460.96 462.70 464.63 468.34 470.29 472.15 473.96 476.05 477.85 479.75 483.56 485.28 487.09 488.90 490.84 492.63 498.43 500.32 502.20 503.90 505.80 507.86 511.90 513.82 515.54 517.61 521.59 523.36 525.42 527.40 529.35 531.13 534.67 536.70 538.69 540.48 542.28 544.07 546.15 548.21 550.60 552.36 554.06 555.85 557.69 559.65 563.62 565.34 567.31 571.29 575.17 579.15 581.22 583.04 587.11 588.90 590.67 592.60 594.55 598.20 600.30 602.02 604.04 605.84 607.61 611.55 613.26 615.14 616.86 620.49 624.50 626.27 628.14 630.17 633.62 635.44 637.35 639.31 641.06 644.97 647.05 650.65 652.61 656.16 658.19 659.94 661.69 665.60 667.69 669.71 671.59 673.59 677.33 679.13 681.09 683.06 684.93 686.91 690.54 692.56 694.39 696.30 698.23 701.94 703.79 705.86 707.89 711.76 713.68 715.51 719.12 722.99 724.84 726.73 730.46 732.35 734.07 737.83 739.90 742.08 743.75 745.45 747.18 749.23 751.03 752.83 754.07 755.27 757.08 758.93 762.66 764.37 766.25 768.06 770.04 771.80 773.83 776.42 778.03 779.60 781.20 784.59 786.47 789.98 791.97 794.07 797.72 799.80 801.60 805.31 807.01 808.89 810.80 812.53 814.62 816.45 820.29 822.09 823.94 826.03 827.87 833.32 835.14 836.93 840.51 842.56 844.64 846.46 848.47 850.51 852.55 856.55 858.53 860.44 864.35 866.06 868.10 870.14 871.94 873.74 877.69 879.51 881.57 883.43 885.39 887.42 891.14 893.11 894.91 896.89 898.65 902.08 904.04 905.79],
[0.00 41.83 496.53 573.18 622.42 648.85 721.20 736.00 829.58],
[55.14 213.91 234.60 338.60 782.77],
[13.49 22.63 84.34 99.55 109.11 120.30 148.52 192.40 206.10 226.87 264.85 281.92 298.44 325.15 334.60 344.13 373.97 418.71 439.82 451.29 466.49 481.70 494.46 509.92 585.12 596.41 618.58 631.89 663.65 675.44 688.62 709.98 717.34 774.78 838.76 854.65 862.40 875.70 889.25 900.37],
[30.24 38.15 53.39 68.82 128.17 139.36 163.33 176.91 215.65 237.23 251.57 274.31 291.05 313.67 355.33 364.47 386.75 398.22 407.54 426.32 519.54 532.83 549.26 561.63 569.23 577.15 609.64 643.15 654.42 699.97 728.54 740.75 760.85 788.18 795.91 803.37 818.40 831.28 907.61] }', ...
'duration', { [0], [0], [0], [0], [0] })

consess{1}.tcon.name = 'go_success';
consess{1}.tcon.convec = [1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{2}.tcon.name = 'go_toolate';
consess{2}.tcon.convec = [0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{3}.tcon.name = 'go_wrong';
consess{3}.tcon.convec = [0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{4}.tcon.name = 'stop_success';
consess{4}.tcon.convec = [0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{5}.tcon.name = 'stop_failure';
consess{5}.tcon.convec = [0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{6}.tcon.name = 'stop_success - go_success';
consess{6}.tcon.convec = [-1.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{7}.tcon.name = 'go_success - stop_success';
consess{7}.tcon.convec = [1.0 0.0 0.0 -1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{8}.tcon.name = 'stop_success - stop_failure';
consess{8}.tcon.convec = [0.0 0.0 0.0 1.0 -1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{9}.tcon.name = 'stop_failure - stop_success';
consess{9}.tcon.convec = [0.0 0.0 0.0 -1.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{10}.tcon.name = 'go_success - stop_failure';
consess{10}.tcon.convec = [1.0 0.0 0.0 0.0 -1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{11}.tcon.name = 'stop_failure - go_success';
consess{11}.tcon.convec = [-1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{12}.tcon.name = 'go_wrong - go_success';
consess{12}.tcon.convec = [-1.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{13}.tcon.name = 'go_success - go_wrong';
consess{13}.tcon.convec = [1.0 0.0 -1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0];
consess{14}.fcon.name = 'Effect of interest';
consess{14}.fcon.convec = {[0.2000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.2000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.2000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.2000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.2000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000]}';
consess{15}.fcon.name = 'Effect of rp';
consess{15}.fcon.convec = {[0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0556 0.0000]}';
consess{16}.fcon.name = 'Effect of rp high';
consess{16}.fcon.convec = {[0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000 0.0000;
 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0000 0.0833 0.0000]}';