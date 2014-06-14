clear all
clc

arglist = argv();
% Number of units in each layer
s1 = 4;
s2 = 4;
s3 = 1;

%% Reading from files
training_file = arglist{1};
development_file = arglist{2};
[a,b,c,d,e]=textread(training_file,'%f%f%s%s%s','headerlines',1,'delimiter',',');

max_a = 2000; 
min_a = 1900; 
max_b = 7;
min_b = 0;

a_norm = ((a - min_a)./(max_a - min_a) - 0.5)*2;
b_norm = ((b - min_b)./(max_b - min_b) - 0.5)*2;

c = strcmp(c,'yes');
c = double(c);
d = strcmp(d,'yes');
d = double(d);
e = strcmp(e,'yes');

for i=1:length(c)
    if c(i) == 0
        c(i) = -1;
    end
    if d(i) == 0
        d(i) = -1;
    end
end

data = [a_norm b_norm c d e];

xinput = data(:,1:end-1);
output = data(:,end);
numberofones = sum(output == 1);

epsilon1 = 0.1;
epsilon2 = 0.1;

size_input = size(xinput,1);

%% Randomly Initializing Thetas
Theta1 = rand(s2,(s1+1))*(2*epsilon1) - epsilon1;
Theta2 = rand(s3,(s2+1))*(2*epsilon2) - epsilon2;

%% BackPropagation Algorithm
alpha = 0.1;
num_iter = 3000;
lambda = 0.01;
Thresh = 0.5;
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
        a3 = 1.0 ./ (1.0 + 1.0*exp(-z3));   
        %Jtheta = Jtheta - ((output(i)'*log(a3) + (1 - output(i))'*log(1 - a3))./size_input);  
        Square_error = Square_error + (a3 - output(i)).^2;
        delta3(i,:) = (a3 - output(i)); 
        delta2(i,:) = Theta2'*delta3(i,:).*(a2'.*(1-a2)');
        DELTA1 = DELTA1 + delta2(i,:)'*a1;
        DELTA2 = DELTA2 + delta3(i,:)'*a2;
    end
    %Reg_J = (sum(sum(Theta1(:,2:end).^2)) + sum(sum(Theta2(:,2:end).^2))).*(lambda./(2*size_input));
    if mod(j,10) == 0
        disp(Square_error./2)
    end
    DELTA1 = DELTA1(2:end,:);
    Theta1_Unreg = DELTA1./(1.0*size_input);
    Theta2_Unreg = DELTA2./(1.0*size_input);
    Theta1_Gradient = Theta1_Unreg + Theta1.*(lambda./size_input); 
    Theta2_Gradient = Theta2_Unreg + Theta2.*(lambda./size_input);
    Theta1_Gradient(:,1) = Theta1_Unreg(:,1);
    Theta2_Gradient(:,1) = Theta2_Unreg(:,1);
    Theta1 = Theta1 - alpha*Theta1_Gradient;
    Theta2 = Theta2 - alpha*Theta2_Gradient;
    
    %Jtheta = Jtheta + Reg_J;
end
%% Testing
[at,bt,ct,dt]=textread(development_file,'%f%f%s%s','headerlines',1,'delimiter',',');
%[et]=textread('music_dev_keys.txt','%s','delimiter',',');

at_norm = ((at - min_a)./(max_a - min_a) - 0.5)*2;
bt_norm = ((bt - min_b)./(max_b - min_b) - 0.5)*2;

ct = strcmp(ct,'yes');
ct = double(ct);
dt = strcmp(dt,'yes');
dt = double(dt);
%et = strcmp(et,'yes');

for i=1:length(ct)
    if ct(i) == 0
        ct(i) = -1;
    end
    if dt(i) == 0
        dt(i) = -1;
    end
end

%datat = [at_norm bt_norm ct dt et];
datat = [at_norm bt_norm ct dt];
%xtinput = datat(:,1:end-1);
xtinput = datat;
otutput = datat(:,end);

size_testing = size(xtinput,1);

predicted = [];
labels = [];
%Square_error = 0;
% Predicting
for i = 1:size_testing
        at1 = [1 xtinput(i,:)];
        zt2 = at1*Theta1';
        at2 = 1.0 ./ (1.0 + 1.0*exp(-zt2));
        at2 = [1 at2];
        zt3 = at2*Theta2';
        at3 = 1.0 ./ (1.0 + 1.0*exp(-zt3));
        %Square_error = Square_error + (at3 - otutput(i)).^2;
        if at3 >= Thresh
            at3 = 1;
            at33 = 'yes';
        else
            at3 = 0;
            at33 = 'no';
        end
        predicted = [predicted;at3];
        labels = [labels;at33];
end
%predicted = predicted;
%output = otutput;
%Square_error = Square_error;
disp('TRAINING COMPLETED! NOW PREDICTING.')
%C = (predicted == output)
disp(labels)


