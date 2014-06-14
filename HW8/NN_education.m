clear all
clc

arglist = argv();
training_file = arglist{1};
development_file = arglist{2};

% Number of units in each layer
s1 = 5;
s2 = 5;
s3 = 1;

%% Reading from files
[a,b,c,d,e,f]=textread(training_file,'%f%f%f%f%f%f','headerlines',1,'delimiter',',');

max_value = 100;
min_value = 0;

a_norm = ((a - min_value)./(max_value - min_value) - 0.5)*2;
b_norm = ((b - min_value)./(max_value - min_value) - 0.5)*2;
c_norm = ((c - min_value)./(max_value - min_value) - 0.5)*2;
d_norm = ((d - min_value)./(max_value - min_value) - 0.5)*2;
e_norm = ((e - min_value)./(max_value - min_value) - 0.5)*2;
f_norm = ((f - min_value)./(max_value - min_value) - 0.5)*2;

data = [a_norm b_norm c_norm d_norm e_norm f];
xinput = data(:,1:end-1);
output = data(:,end);
epsilon1 = 0.1;
epsilon2 = 0.1;
size_input = size(xinput,1);

%% Randomly Initializing Thetas
Theta1 = rand(s2,(s1+1))*(2*epsilon1) - epsilon1;
Theta2 = rand(s3,(s2+1))*(2*epsilon2) - epsilon2;
%% BackPropagation Algorithm
alpha = 0.05;
num_iter = 3000;
lambda = 0.01;
% Batch Gradient Descent
for j = 1:num_iter
    Square_error = 0;
    DELTA1 = 0;
    DELTA2 = 0;
    Jtheta = 0;
    for i = 1:size_input
        a1 = [1 xinput(i,:)];
        z2 = a1*Theta1';
        a2 = 1.0 ./ (1.0 + 1.0*exp(-z2));
        a2 = [1 a2];
        z3 = a2*Theta2';
        a3 = z3;
        %Jtheta = Jtheta - ((output(i)'*log(a3) + (1 - output(i))'*log(1 - a3))./size_input);  
        Square_error = Square_error + (a3 - output(i)).^2;
        delta3(i,:) = a3 - output(i);
        delta2(i,:) = Theta2'*delta3(i,:).*(a2'.*(1-a2)');
        DELTA1 = DELTA1 + delta2(i,:)'*a1;
        DELTA2 = DELTA2 + delta3(i,:)'*a2;
    end 
    %Reg_J = sum(sum(Theta1(:,2:end).^2)).*(lambda./(2*size_input)) + sum(sum(Theta2(:,2:end).^2)).*(lambda./(2*size_input));
    if mod(j,10) == 0
        disp(Square_error./2)
    end
    DELTA1 = DELTA1(2:end,:);
    Theta1_Unreg = DELTA1./size_input;
    Theta2_Unreg = DELTA2./size_input;
    Theta1_Gradient = Theta1_Unreg + Theta1.*(lambda./size_input); 
    Theta2_Gradient = Theta2_Unreg + Theta2.*(lambda./size_input);
    Theta1_Gradient(:,1) = Theta1_Unreg(:,1);
    Theta2_Gradient(:,1) = Theta2_Unreg(:,1);
    Theta1 = Theta1 - alpha*Theta1_Gradient;
    Theta2 = Theta2 - alpha*Theta2_Gradient;
    %Jtheta = Jtheta + Reg_J;
end
%% Testing
[at,bt,ct,dt,et]=textread(development_file,'%f%f%f%f%f','headerlines',1,'delimiter',',');
%[ft]=textread('education_dev_keys.txt','%f','delimiter',',');

at_norm = ((at - min_value)./(max_value - min_value) - 0.5)*2;
bt_norm = ((bt - min_value)./(max_value - min_value) - 0.5)*2;
ct_norm = ((ct - min_value)./(max_value - min_value) - 0.5)*2;
dt_norm = ((dt - min_value)./(max_value - min_value) - 0.5)*2;
et_norm = ((et - min_value)./(max_value - min_value) - 0.5)*2;

%datat = [at_norm bt_norm ct_norm dt_norm et_norm ft];
datat = [at_norm bt_norm ct_norm dt_norm et_norm];
%xtinput = datat(:,1:end-1);
xtinput = datat;
otutput = datat(:,end);

size_testing = size(xtinput,1);

predicted = [];
%Square_error = 0;

% Predicting
for i = 1:size_testing
        at1 = [1 xtinput(i,:)];
        zt2 = at1*Theta1';
        at2 = 1.0 ./ (1.0 + 1.0*exp(-zt2));
        at2 = [1 at2];
        zt3 = at2*Theta2';
        at3 = zt3;
        %Square_error = Square_error + (at3 - otutput(i)).^2;
        predicted = [predicted;round(at3)*1.0];
end
disp('TRAINING COMPLETED! NOW PREDICTING.')
disp(predicted);
%output = otutput;
%Square_error = Square_error;
%C = sum(predicted == output)

