clc
clear all
close all

N = [.5]
D = [1 2 1 0]
figure(1)
L = tf(N,D)
bode(L)
grid on
