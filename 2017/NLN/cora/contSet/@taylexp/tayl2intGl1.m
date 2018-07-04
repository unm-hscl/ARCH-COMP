function res = tayl2intGl1(obj, var1, eps)
% tayl2intGl1 - convert a taylor expression to an interval (object, var1, var2, eps)
% using the global optimization
%
% Syntax:  
%    res = tayl2intGl1(obj)
%
% Inputs:
%    obj - (input value) a taylor expression object
%    var1 - intput variable
%    eps - precision
%    
%
% Outputs:
%    res - an interval object
%
% Example: 
%
% Other m-files required: none
% Subfunctions: none
% MAT-files required: none
%

% Author:       Dmitry Grebenyuk
% Written:      22-July-2016
% Last update:  ---
% Last revision:---


%------------- BEGIN CODE --------------
res = interval();

%obj = varargin{1};

for j = 1:obj.numberOfCells_j
    for i = 1:obj.numberOfCells_i
         
        

        % change the ^'s to the .^'s to preserve work in vector
        % case
        claim = char(obj.pol_syms{i, j});
        new_claim = strrep(claim, '^', '.^');
        new_claim = strrep(new_claim, '*', '.*');
        new_claim = strrep(new_claim, '/', './');
        new_claim = strrep(new_claim, char(inputname(2)), 'x');
                
        rem11 = GInt1(var1, new_claim, eps);
        rem1 = rem11(i,j);

        
        rem2 = obj.remainder(i,j);

        res(i,j) = rem1 + rem2;
    
    end
end



%------------- END OF CODE --------------
