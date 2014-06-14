function [z] = rescale(x)

if std(x) == 0
    z = zeros(size(x));
else
    z = (x - mean(x))/std(x);
end

end

