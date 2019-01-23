%% Build the geometry for the 3D Hummock mesh
% Created by Mike O'Connor on 1.3.19 at 23:18

close all;
clear all;
clc;

A = 0.15; % m, height of hummock amplitude (from origin, max height = 2*A)
k1 = pi();
k2 = pi();
lenX = 6; % m of domain--each hummock is 1 m wide and long, so 3 m shows 3 hummocks
lenY = 2;
lenXDomain = 500; % m of the entire hillslope
nx = 40; % number of nodes in x dimension
ny = 40; % number of nodes in y dimension
m = 0.05; % slope 

x = linspace(0,lenX,nx);
y = linspace(0,lenY,ny);

% Test in 2D
z = A.*sin(k1.*x) + m.*x;

figure;
plot(x,z);
title('2D Cross-Section of the unit cell boundary');

% Expand to 3D
[X,Y] = meshgrid(x,y);
Z = A*sin(k1*X).*sin(k2*Y) + m.*X;
%Z = A*sin(k1*X).*sin(k2*Y);

figure;
surf(X,Y,Z);
axis equal;

% % Insert this unit cell into the domain
% x2 = linspace(lenX,lenXDomain,40);
% y2 = linspace(0,lenY,40);
% 
% % Test in 2D
% z2 = m.*x2;
% figure(1);
% hold all;
% plot(x2,z2);
% 
% % Test in 3D
% [X2,Y2] = meshgrid(x2,y2);
% Z2 = m.*X2;
% figure(2);
% hold all;
% surf(X2,Y2,Z2);
% xlim([0 10])
% zlim([-0.5 2]);
% %axis equal;

