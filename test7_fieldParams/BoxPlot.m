%% Build bar graph with thaw outputs from ATS
close all;
njobs = 32
clear all;
clc;

R = cd;

meanThaw = [ 0.50805435  0.54417167  0.50596259  0.48899556  0.45070933  0.53581258 0.57789567  0.5271125   0.42424125         nan];

stdThaw = [ 0.06410917  0.06892987  0.0763477   0.09416707  0.04938312  0.05648336 0.0555088   0.08101877  0.04001936         nan]

runPrefixList = {'DwarfShrubsHi','DwarfShrubsLo','WoodyShrubsHillslope','WoodyShrubsRiparianHi','WoodyShrubsRiparianLo','TussockTundraHi','TussockTundraLo','WaterTrack','SedgeHi','SedgeLo'}

figure;
bar([1:length(meanThaw)],meanThaw);
hold all;
errorbar([1:length(meanThaw)],meanThaw,stdThaw);
